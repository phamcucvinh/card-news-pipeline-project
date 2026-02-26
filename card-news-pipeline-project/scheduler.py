"""
slide_scheduler.py — APScheduler 기반 슬라이드 자동 생성기

topics.json 에 등록된 주제를 지정한 시간에 자동 실행:
  1. Claude API → HTML 슬라이드 생성
  2. Playwright → PNG 변환
  3. output/slides/, output/images/ 에 저장
"""

import os, json, logging, re, sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import anthropic
from playwright.sync_api import sync_playwright

# ─── 경로 설정 ──────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
TOPICS_FILE = BASE_DIR / "topics.json"
SLIDES_DIR  = BASE_DIR / "output" / "slides"
IMAGES_DIR  = BASE_DIR / "output" / "images"
LOG_FILE    = BASE_DIR / "output" / "scheduler.log"
ENV_FILE    = BASE_DIR.parent / ".env"

SLIDES_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# ─── 로그 설정 ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("slide-scheduler")

# ─── 환경변수 로드 ───────────────────────────────────────────────
load_dotenv(ENV_FILE, override=True)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_API_KEY:
    log.error("ANTHROPIC_API_KEY 가 없습니다. .env 파일을 확인해주세요.")
    sys.exit(1)

# ─── 시리즈별 CSS (템플릿) ───────────────────────────────────────
SERIES_A_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
* { margin:0;padding:0;box-sizing:border-box; }
.slide { width:1080px;height:1080px;background:#0d1117;color:#e6edf3;font-family:'Noto Sans KR',sans-serif;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;padding:80px; }
.slide.cover { background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);justify-content:center;align-items:flex-start; }
.cover-badge { display:inline-block;padding:8px 20px;background:rgba(88,166,255,0.12);border:1px solid rgba(88,166,255,0.3);border-radius:20px;color:#58a6ff;font-size:24px;font-weight:500;letter-spacing:1px;margin-bottom:40px; }
.cover-title { font-size:72px;font-weight:900;line-height:1.15;color:#fff;letter-spacing:-1px;margin-bottom:32px;word-break:keep-all; }
.cover-title span { color:#58a6ff; }
.cover-subtitle { font-size:30px;color:#8b949e;font-weight:400;line-height:1.5;word-break:keep-all; }
.slide.content { background:#0d1117; }
.slide-num { font-size:20px;color:#30363d;font-weight:500;letter-spacing:2px;text-transform:uppercase; }
.section-label { display:inline-block;padding:6px 16px;background:rgba(88,166,255,0.08);border-left:3px solid #58a6ff;color:#58a6ff;font-size:22px;font-weight:600;margin-bottom:24px; }
.content-title { font-size:52px;font-weight:800;color:#fff;line-height:1.2;margin-bottom:32px;word-break:keep-all; }
.content-body { font-size:30px;color:#8b949e;line-height:1.8;word-break:keep-all;flex:1; }
.content-body strong { color:#e6edf3;font-weight:700; }
.content-body .highlight { color:#f0883e;font-weight:700; }
.slide.point { background:linear-gradient(135deg,#0d1117,#161b22);justify-content:center;align-items:center;text-align:center; }
.big-number { font-size:180px;font-weight:900;color:#58a6ff;line-height:1;opacity:0.15;position:absolute;top:50%;left:50%;transform:translate(-50%,-55%); }
.point-text { font-size:48px;font-weight:700;color:#fff;line-height:1.4;position:relative;z-index:1;word-break:keep-all;max-width:800px; }
.slide.outro { background:linear-gradient(135deg,#161b22 0%,#0d1117 100%);justify-content:space-between; }
.outro-quote { font-size:42px;font-weight:300;color:#e6edf3;line-height:1.6;border-left:4px solid #58a6ff;padding-left:40px;word-break:keep-all;flex:1;display:flex;align-items:center; }
.outro-footer { display:flex;justify-content:space-between;align-items:center;border-top:1px solid #21262d;padding-top:32px; }
.author-name { font-size:28px;font-weight:700;color:#e6edf3; }
.author-handle { font-size:24px;color:#58a6ff;margin-top:6px; }
.cta-text { font-size:26px;color:#8b949e;text-align:right; }
.slide-footer { display:flex;justify-content:space-between;align-items:center;border-top:1px solid #21262d;padding-top:28px;margin-top:28px; }
.brand { font-size:22px;font-weight:700;color:#30363d;letter-spacing:1px; }
.progress-dots { display:flex;gap:8px; }
.dot { width:8px;height:8px;border-radius:50%;background:#21262d; }
.dot.active { background:#58a6ff; }
.deco-line { position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#58a6ff,#7c8cf8,#58a6ff); }
.list-item { display:flex;align-items:flex-start;gap:24px;padding:24px 0;border-bottom:1px solid #21262d; }
.list-item:last-child { border-bottom:none; }
.list-num { width:48px;height:48px;border-radius:12px;background:rgba(88,166,255,0.12);color:#58a6ff;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;flex-shrink:0;margin-top:4px; }
.list-title { font-size:32px;font-weight:700;color:#e6edf3;margin-bottom:8px;word-break:keep-all; }
.list-desc { font-size:26px;color:#8b949e;line-height:1.6;word-break:keep-all; }
"""

SERIES_B_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
* { margin:0;padding:0;box-sizing:border-box; }
.slide { width:1080px;height:1080px;font-family:'Noto Sans KR',sans-serif;position:relative;overflow:hidden; }
.slide.cover-B { background:#0a0a0f;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center; }
.cover-B .series-tag { font-size:20px;font-weight:500;color:#6366f1;letter-spacing:3px;text-transform:uppercase;margin-bottom:32px; }
.cover-B .main-term { font-size:140px;font-weight:900;color:#fff;line-height:1;letter-spacing:-4px;margin-bottom:16px;position:relative;display:inline-block; }
.cursor { display:inline-block;width:8px;height:120px;background:#6366f1;margin-left:8px;vertical-align:bottom;animation:blink 1s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1}50%{opacity:0} }
.cover-B .term-def { font-size:32px;color:#888;font-weight:400; }
.cover-B .bottom-bar { position:absolute;bottom:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#6366f1,#818cf8,#a5b4fc); }
.slide.definition { background:#13131b;display:flex;flex-direction:column;padding:70px 80px; }
.def-label { font-size:20px;font-weight:600;color:#6366f1;letter-spacing:2px;text-transform:uppercase;margin-bottom:48px; }
.def-icon { font-size:100px;margin-bottom:40px;line-height:1; }
.def-title { font-size:56px;font-weight:900;color:#fff;margin-bottom:28px;word-break:keep-all; }
.def-body { font-size:32px;color:#aaa;line-height:1.7;word-break:keep-all;flex:1; }
.def-body strong { color:#fff; }
.def-body .accent { color:#818cf8;font-weight:700; }
.slide.analogy { background:linear-gradient(135deg,#0f0f1a,#1a1a2e);display:flex;flex-direction:column;padding:70px 80px;justify-content:center; }
.analogy-label { font-size:20px;color:#10b981;letter-spacing:2px;text-transform:uppercase;margin-bottom:48px;font-weight:600; }
.analogy-main { display:flex;align-items:center;gap:48px;margin-bottom:48px; }
.analogy-emoji { font-size:120px;flex-shrink:0;line-height:1; }
.analogy-text { font-size:40px;color:#e0e0e0;line-height:1.5;word-break:keep-all; }
.analogy-text .keyword { color:#34d399;font-weight:800; }
.analogy-sub { background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);border-radius:16px;padding:28px 36px;font-size:28px;color:#888;line-height:1.6;word-break:keep-all; }
.slide.marketer-view { background:#0a0a0f;display:flex;flex-direction:column;padding:70px 80px; }
.mv-label { font-size:20px;color:#f59e0b;letter-spacing:2px;text-transform:uppercase;margin-bottom:48px;font-weight:600; }
.mv-title { font-size:52px;font-weight:900;color:#fff;margin-bottom:48px;word-break:keep-all; }
.mv-cards { display:flex;flex-direction:column;gap:20px;flex:1; }
.mv-card { background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.15);border-radius:16px;padding:24px 28px;display:flex;align-items:center;gap:20px; }
.mv-card-icon { font-size:36px;flex-shrink:0; }
.mv-card-text { font-size:28px;color:#ccc;line-height:1.5;word-break:keep-all; }
.mv-card-text strong { color:#fcd34d; }
.slide.summary-B { background:#13131b;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:70px 80px; }
.summary-badge { font-size:20px;font-weight:600;color:#6366f1;letter-spacing:2px;text-transform:uppercase;margin-bottom:40px; }
.summary-title { font-size:60px;font-weight:900;color:#fff;margin-bottom:48px;word-break:keep-all; }
.summary-points { display:flex;flex-direction:column;gap:20px;width:100%;text-align:left; }
.summary-point { display:flex;align-items:center;gap:20px;background:rgba(99,102,241,0.06);border-radius:14px;padding:22px 28px; }
.sp-check { font-size:28px;flex-shrink:0; }
.sp-text { font-size:28px;color:#ddd;word-break:keep-all; }
.sp-text strong { color:#a5b4fc; }
.follow-cta { margin-top:48px;font-size:26px;color:#555; }
.follow-cta span { color:#6366f1; }
"""

CSS_MAP = {"A": SERIES_A_CSS, "B": SERIES_B_CSS}

# ─── Claude API 호출 ─────────────────────────────────────────────
SYSTEM_PROMPT = """
당신은 1080×1080 HTML 카드뉴스 슬라이드를 생성하는 전문가입니다.

규칙:
- 반드시 완전한 HTML 파일 하나를 출력합니다 (<!DOCTYPE html> 포함)
- 모든 슬라이드는 한 HTML 파일 내에 <br><br>로 구분하여 나열
- 1080×1080px 고정 (절대 변경 금지)
- 외부 이미지 URL 사용 금지
- word-break: keep-all 적용
- CSS는 <style> 태그 안에 반드시 포함
- HTML 코드만 출력 (설명 텍스트 없이)
"""

def build_user_prompt(job: dict, css: str) -> str:
    series  = job.get("series", "A")
    topic   = job["topic"]
    count   = job.get("slide_count", 7)
    account = job.get("account", "@claudecode.kr")
    badge   = job.get("badge", "코딩하는 마케터")

    structures = {
        "A": f"표지(cover) + 본문(content) {count-3}장 + 리스트(list) 1장 + 포인트(point) 1장 + 마무리(outro) 1장",
        "B": "표지(cover-B) + 정의(definition) + 비유(analogy) + 활용(marketer-view) + 정리(summary-B)",
    }

    return f"""
주제: {topic}
시리즈: {series}시리즈
슬라이드 수: {count}장
계정: {account}
배지: {badge}
구성: {structures.get(series, structures['A'])}

아래 CSS를 <style> 태그 안에 그대로 사용하세요:

{css}

위 CSS와 HTML 패턴을 사용해 "{topic}" 주제로
완성된 HTML 슬라이드를 생성하세요.
HTML 코드만 출력하세요.
""".strip()


def call_claude(job: dict) -> str:
    series = job.get("series", "A")
    css    = CSS_MAP.get(series, SERIES_A_CSS)

    client  = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(job, css)}],
    )
    return message.content[0].text


def extract_html(raw: str) -> str:
    """마크다운 코드펜스 제거"""
    m = re.search(r"```(?:html)?\s*(<!DOCTYPE[\s\S]+?)</body>\s*</html>", raw, re.IGNORECASE)
    if m:
        return m.group(1) + "</body>\n</html>"
    if "<!DOCTYPE" in raw:
        return raw
    return raw


# ─── HTML → PNG 변환 ────────────────────────────────────────────
def html_to_png(html_path: Path, out_dir: Path, job_id: str) -> list[Path]:
    png_files = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 8000})
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.wait_for_timeout(1500)

        slides = page.query_selector_all(".slide")
        for i, slide in enumerate(slides, 1):
            out = out_dir / f"{job_id}-{i:02d}.png"
            slide.screenshot(path=str(out))
            png_files.append(out)
            log.info(f"    PNG {i:02d}/{len(slides)} → {out.name}")

        browser.close()
    return png_files


# ─── 메인 잡 실행 함수 ───────────────────────────────────────────
def run_job(job: dict) -> None:
    job_id  = job.get("id", "unknown")
    topic   = job.get("topic", "")
    series  = job.get("series", "A")
    do_png  = job.get("png", True)
    today   = datetime.now().strftime("%Y%m%d-%H%M")

    log.info(f"━━━ 잡 시작: [{job_id}] '{topic}' ({series}시리즈) ━━━")

    try:
        # 1. Claude API → HTML
        log.info("  ① Claude API 호출 중...")
        raw_html = call_claude(job)
        html_str = extract_html(raw_html)

        # 2. HTML 저장
        slug     = re.sub(r"[^\w가-힣-]", "", topic.replace(" ", "-"))[:30]
        html_out = SLIDES_DIR / f"slide-{slug}-{today}.html"
        html_out.write_text(html_str, encoding="utf-8")
        log.info(f"  ② HTML 저장: {html_out.name}")

        # 3. PNG 변환
        if do_png:
            log.info("  ③ PNG 변환 중...")
            png_files = html_to_png(html_out, IMAGES_DIR, f"slide-{slug}-{today}")
            log.info(f"  ③ PNG {len(png_files)}장 저장 완료")

        log.info(f"━━━ 잡 완료: [{job_id}] ━━━\n")

    except Exception as e:
        log.error(f"잡 오류 [{job_id}]: {e}", exc_info=True)


# ─── 스케줄 등록 ────────────────────────────────────────────────
def load_topics() -> list[dict]:
    if not TOPICS_FILE.exists():
        log.warning(f"topics.json 없음 — 기본 예시로 생성합니다: {TOPICS_FILE}")
        default = {
            "jobs": [
                {
                    "id": "weekly-tech",
                    "topic": "ChatGPT vs Claude 차이점",
                    "series": "B",
                    "slide_count": 5,
                    "badge": "알쓸IT잡",
                    "account": "@claudecode.kr",
                    "png": True,
                    "schedule": {"type": "cron", "day_of_week": "mon", "hour": 9, "minute": 0}
                },
                {
                    "id": "daily-tip",
                    "topic": "생산성을 높이는 AI 활용 5가지 방법",
                    "series": "A",
                    "slide_count": 7,
                    "badge": "코딩하는 마케터",
                    "account": "@claudecode.kr",
                    "png": True,
                    "schedule": {"type": "cron", "day_of_week": "wed", "hour": 9, "minute": 0}
                }
            ]
        }
        TOPICS_FILE.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(TOPICS_FILE, encoding="utf-8") as f:
        return json.load(f).get("jobs", [])


def make_trigger(sched: dict):
    t = sched.get("type", "cron")
    if t == "cron":
        return CronTrigger(
            day_of_week=sched.get("day_of_week", "*"),
            hour=sched.get("hour", 9),
            minute=sched.get("minute", 0),
        )
    elif t == "interval":
        return IntervalTrigger(
            hours=sched.get("hours", 0),
            minutes=sched.get("minutes", 0),
            seconds=sched.get("seconds", 0),
        )
    raise ValueError(f"알 수 없는 스케줄 타입: {t}")


def main():
    log.info("=" * 56)
    log.info("  슬라이드 스케줄러 시작")
    log.info("=" * 56)

    jobs = load_topics()
    if not jobs:
        log.error("topics.json 에 등록된 잡이 없습니다.")
        sys.exit(1)

    scheduler = BlockingScheduler(timezone="Asia/Seoul")

    for job in jobs:
        sched = job.get("schedule", {"type": "cron", "hour": 9, "minute": 0})
        trigger = make_trigger(sched)
        scheduler.add_job(
            run_job,
            trigger=trigger,
            args=[job],
            id=job["id"],
            name=job["topic"],
            misfire_grace_time=600,
        )
        log.info(f"  등록: [{job['id']}] '{job['topic']}' — {sched}")

    log.info(f"\n총 {len(jobs)}개 잡 등록 완료. 스케줄러 실행 중...\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("스케줄러 종료.")


if __name__ == "__main__":
    # --now 플래그: 즉시 테스트 실행
    # --offline 플래그: Claude API 없이 PNG 변환만 실행
    if "--now" in sys.argv:
        idx = sys.argv.index("--now")
        job_id = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else None
        jobs = load_topics()
        targets = [j for j in jobs if j["id"] == job_id] if job_id else jobs[:1]
        for j in targets:
            run_job(j)
    else:
        main()


def run_offline(html_file: str) -> None:
    """Claude API 없이 기존 HTML → PNG 변환만 실행"""
    path = Path(html_file)
    if not path.exists():
        log.error(f"파일 없음: {html_file}")
        return
    log.info(f"오프라인 변환: {path.name}")
    today = datetime.now().strftime("%Y%m%d-%H%M")
    slug  = path.stem
    pngs  = html_to_png(path, IMAGES_DIR, f"{slug}-{today}")
    log.info(f"완료: PNG {len(pngs)}장 → {IMAGES_DIR}")
