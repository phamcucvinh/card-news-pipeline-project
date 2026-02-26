#!/usr/bin/env python3
"""
validate_slide.py — 카드뉴스 슬라이드 HTML 자동 검증 스크립트
사용: python scripts/validate_slide.py output/slides/
"""

import os
import sys
import re
from pathlib import Path

# ── 색상 출력 ──
class C:
    RED    = '\033[91m'
    YELLOW = '\033[93m'
    GREEN  = '\033[92m'
    CYAN   = '\033[96m'
    RESET  = '\033[0m'
    BOLD   = '\033[1m'

def check_slides(slides_dir: str) -> dict:
    """슬라이드 폴더 전체 검증"""
    path = Path(slides_dir)
    if not path.exists():
        print(f"{C.RED}❌ 폴더 없음: {slides_dir}{C.RESET}")
        sys.exit(1)

    html_files = sorted(path.glob("slide-*.html"))
    if not html_files:
        print(f"{C.YELLOW}⚠️ 슬라이드 파일 없음 (slide-*.html){C.RESET}")
        return {}

    results = {}
    for f in html_files:
        results[f.name] = check_single_slide(f)

    return results

def check_single_slide(filepath: Path) -> dict:
    """단일 슬라이드 검증"""
    issues = {"high": [], "medium": [], "low": []}

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        issues["high"].append(f"파일 읽기 실패: {e}")
        return issues

    # ── 🔴 고(High) 결함 검사 ──

    # 1. 슬라이드 크기 (1080x1080)
    width_match = re.search(r'width\s*:\s*(\d+)px', content)
    height_match = re.search(r'height\s*:\s*(\d+)px', content)
    if width_match:
        w = int(width_match.group(1))
        if w != 1080:
            issues["high"].append(f"슬라이드 너비 {w}px (1080px 필요)")
    else:
        issues["medium"].append("width 속성 없음")

    if height_match:
        h = int(height_match.group(1))
        if h != 1080:
            issues["high"].append(f"슬라이드 높이 {h}px (1080px 필요)")
    else:
        issues["medium"].append("height 속성 없음")

    # 2. HTML 파싱 가능 여부 (간단 체크)
    if not content.strip().startswith("<!"):
        issues["high"].append("DOCTYPE 없음 (HTML 유효성 문제)")

    # 3. 외부 리소스 URL 체크 (src=http, href=http 단 fonts.googleapis.com 제외)
    external_urls = re.findall(
        r'(?:src|href)\s*=\s*["\']?(https?://(?!fonts\.googleapis|fonts\.gstatic)[^\s"\']+)',
        content
    )
    if external_urls:
        for url in external_urls[:3]:  # 최대 3개만 표시
            issues["high"].append(f"외부 리소스: {url[:60]}...")

    # ── 🟡 중(Medium) 결함 검사 ──

    # 4. Pretendard 또는 Noto Sans KR 폰트
    if "Pretendard" not in content and "Noto Sans KR" not in content:
        issues["medium"].append("Pretendard/Noto Sans KR 폰트 없음")

    # 5. 텍스트 내용 존재 여부
    text_content = re.sub(r'<[^>]+>', '', content)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    if len(text_content) < 20:
        issues["medium"].append(f"텍스트 내용 너무 적음 ({len(text_content)}자)")

    # 6. .slide 클래스 존재 여부
    if 'class="slide' not in content and "class='slide" not in content:
        issues["medium"].append(".slide 클래스 없음")

    # ── 🟢 저(Low) 결함 검사 ──

    # 7. 이모지 과다 사용 (한 슬라이드에 5개 이상)
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0]"
    )
    emoji_count = len(emoji_pattern.findall(content))
    if emoji_count > 5:
        issues["low"].append(f"이모지 {emoji_count}개 (슬라이드당 5개 권장)")

    # 8. 파일명 형식 체크
    name = filepath.name
    if not re.match(r'^slide-\d{2}-', name):
        issues["low"].append(f"파일명 형식 권장: slide-XX-주제.html")

    return issues

def print_report(results: dict):
    """검증 결과 출력"""
    total = len(results)
    high_total = sum(len(v["high"]) for v in results.values())
    medium_total = sum(len(v["medium"]) for v in results.values())
    low_total = sum(len(v["low"]) for v in results.values())

    print(f"\n{C.BOLD}{'━'*50}")
    print(f"🔍 슬라이드 QA 검증 결과")
    print(f"{'━'*50}{C.RESET}")
    print(f"검증 파일: {total}개")
    print()

    for filename, issues in results.items():
        has_issues = any(issues[k] for k in ["high", "medium", "low"])
        if not has_issues:
            print(f"{C.GREEN}✅ {filename}{C.RESET}")
            continue

        print(f"{C.CYAN}📄 {filename}{C.RESET}")
        for issue in issues["high"]:
            print(f"  {C.RED}🔴 [HIGH] {issue}{C.RESET}")
        for issue in issues["medium"]:
            print(f"  {C.YELLOW}🟡 [MED]  {issue}{C.RESET}")
        for issue in issues["low"]:
            print(f"  ⬜ [LOW]  {issue}")
        print()

    # 최종 판정
    print(f"{'━'*50}")
    print(f"🔴 고 결함: {high_total}개  🟡 중 결함: {medium_total}개  ⬜ 저 결함: {low_total}개")
    print()

    if high_total > 0:
        print(f"{C.RED}❌ 판정: 수정 필요 (고 결함 {high_total}개 발견){C.RESET}")
        return False
    elif medium_total > 0:
        print(f"{C.YELLOW}⚠️  판정: 수정 권장 (중 결함 {medium_total}개 발견){C.RESET}")
        return True
    else:
        print(f"{C.GREEN}✅ 판정: 통과 (중대 결함 없음){C.RESET}")
        return True

def main():
    if len(sys.argv) < 2:
        print("사용법: python validate_slide.py [슬라이드 폴더]")
        print("예시:   python validate_slide.py output/slides/")
        sys.exit(1)

    slides_dir = sys.argv[1]
    results = check_slides(slides_dir)
    if results:
        passed = print_report(results)
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
