---
name: slide-creator
description: >
  1080×1080 HTML 카드뉴스 슬라이드를 생성하는 스킬.
  주제와 시리즈를 받아 완성된 HTML 파일을 출력한다.
  트리거: "슬라이드 만들어줘", "카드뉴스 만들어줘", "A/B/C시리즈로 만들어줘",
          "slide 생성", "HTML 카드뉴스"
---

# Slide Creator — 1080×1080 HTML 카드뉴스 생성기

## 역할
주제·내용·시리즈 지정을 받아 **완성된 HTML 슬라이드 파일** 1개를 출력한다.
모든 슬라이드는 동일 HTML 파일 내에 `<br><br>`로 구분하여 나열한다.

---

## 1. 시리즈 선택 가이드

| 시리즈 | 이름 | 특징 | 추천 주제 |
|--------|------|------|-----------|
| **A** | 칼럼 기반 | GitHub Dark 테마, 텍스트 중심, 장식선 | 마케팅 칼럼, 경험담, 조언 |
| **B** | 비주얼 네이티브 | 인디고 다크, 이모지 활용, 용어 설명 | IT 단어 설명, 개념 설명 |
| **C** | 시네마틱 | 필름 느낌, 따뜻한 오렌지, 감성 텍스트 | 스토리, 인터뷰, 감성 콘텐츠 |

시리즈 미지정 시: 주제를 분석해 자동 선택

---

## 2. 공통 규칙

```
- 크기: 1080×1080px (고정, 변경 불가)
- 폰트: Noto Sans KR (Google Fonts)
- 슬라이드 수: A=7-9장, B=5-6장, C=6-8장
- 파일명: slide-[주제키워드]-YYYYMMDD.html
- 저장 경로: output/slides/ (없으면 현재 디렉터리)
- 외부 이미지 URL 사용 금지 (CSS만으로 시각 처리)
- word-break: keep-all (한국어 줄바꿈 보호)
```

---

## 3. A시리즈 — 칼럼 기반 (GitHub Dark)

### CSS (완전본)
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
.slide {
  width: 1080px; height: 1080px;
  background: #0d1117; color: #e6edf3;
  font-family: 'Noto Sans KR', sans-serif;
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
  justify-content: space-between; padding: 80px;
}
/* 표지 */
.slide.cover {
  background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
  justify-content: center; align-items: flex-start;
}
.cover-badge {
  display: inline-block; padding: 8px 20px;
  background: rgba(88,166,255,0.12); border: 1px solid rgba(88,166,255,0.3);
  border-radius: 20px; color: #58a6ff; font-size: 24px; font-weight: 500;
  letter-spacing: 1px; margin-bottom: 40px;
}
.cover-title {
  font-size: 72px; font-weight: 900; line-height: 1.15; color: #fff;
  letter-spacing: -1px; margin-bottom: 32px; word-break: keep-all;
}
.cover-title span { color: #58a6ff; }
.cover-subtitle { font-size: 30px; color: #8b949e; font-weight: 400; line-height: 1.5; word-break: keep-all; }
/* 본문 */
.slide.content { background: #0d1117; }
.slide-num { font-size: 20px; color: #30363d; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; }
.section-label {
  display: inline-block; padding: 6px 16px;
  background: rgba(88,166,255,0.08); border-left: 3px solid #58a6ff;
  color: #58a6ff; font-size: 22px; font-weight: 600; margin-bottom: 24px;
}
.content-title { font-size: 52px; font-weight: 800; color: #fff; line-height: 1.2; margin-bottom: 32px; word-break: keep-all; }
.content-body { font-size: 30px; color: #8b949e; line-height: 1.8; word-break: keep-all; flex: 1; }
.content-body strong { color: #e6edf3; font-weight: 700; }
.content-body .highlight { color: #f0883e; font-weight: 700; }
/* 포인트 (숫자 강조) */
.slide.point {
  background: linear-gradient(135deg, #0d1117, #161b22);
  justify-content: center; align-items: center; text-align: center;
}
.big-number {
  font-size: 180px; font-weight: 900; color: #58a6ff; line-height: 1; opacity: 0.15;
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -55%);
}
.point-text { font-size: 48px; font-weight: 700; color: #fff; line-height: 1.4; position: relative; z-index: 1; word-break: keep-all; max-width: 800px; }
/* 마무리 */
.slide.outro {
  background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
  justify-content: space-between;
}
.outro-quote { font-size: 42px; font-weight: 300; color: #e6edf3; line-height: 1.6; border-left: 4px solid #58a6ff; padding-left: 40px; word-break: keep-all; flex: 1; display: flex; align-items: center; }
.outro-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #21262d; padding-top: 32px; }
.author-name { font-size: 28px; font-weight: 700; color: #e6edf3; }
.author-handle { font-size: 24px; color: #58a6ff; margin-top: 6px; }
.cta-text { font-size: 26px; color: #8b949e; text-align: right; }
/* 공통 푸터 */
.slide-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #21262d; padding-top: 28px; margin-top: 28px; }
.brand { font-size: 22px; font-weight: 700; color: #30363d; letter-spacing: 1px; }
.progress-dots { display: flex; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #21262d; }
.dot.active { background: #58a6ff; }
/* 장식 */
.deco-line { position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #58a6ff, #7c8cf8, #58a6ff); }
/* 리스트 */
.list-item { display: flex; align-items: flex-start; gap: 24px; padding: 28px 0; border-bottom: 1px solid #21262d; }
.list-item:last-child { border-bottom: none; }
.list-num { width: 48px; height: 48px; border-radius: 12px; background: rgba(88,166,255,0.12); color: #58a6ff; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800; flex-shrink: 0; margin-top: 4px; }
.list-title { font-size: 32px; font-weight: 700; color: #e6edf3; margin-bottom: 8px; word-break: keep-all; }
.list-desc { font-size: 26px; color: #8b949e; line-height: 1.6; word-break: keep-all; }
```

### A시리즈 슬라이드 구성 (7-9장)
1. **표지** `cover` — badge(시리즈명) + 제목 + 부제목 + 푸터
2. **본문** `content` × 3-5장 — 슬라이드 번호 + 섹션 레이블 + 제목 + 본문
3. **리스트** `content` — 번호 리스트 (3-4항목)
4. **포인트** `point` — 핵심 메시지 1문장 (big-number 배경)
5. **마무리** `outro` — 인용구 + 작성자 + CTA

### A시리즈 HTML 패턴

```html
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<title>슬라이드 — A시리즈</title>
<style>/* 위 CSS 전체 삽입 */</style></head><body>

<!-- 표지 -->
<div class="slide cover">
  <div class="deco-line"></div>
  <div class="cover-badge">시리즈명</div>
  <div>
    <div class="cover-title">제목<br><span>강조 키워드</span></div>
    <div class="cover-subtitle">부제목 설명문</div>
  </div>
  <div class="slide-footer">
    <div class="brand">@계정명</div>
    <div class="progress-dots">
      <div class="dot active"></div><!-- 슬라이드 수만큼 -->
    </div>
  </div>
</div>
<br><br>

<!-- 본문 -->
<div class="slide content">
  <div class="slide-num">01 / 07</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:40px 0">
    <div class="section-label">섹션명</div>
    <div class="content-title">슬라이드 제목</div>
    <div class="content-body">
      <strong>강조 텍스트</strong>와 일반 텍스트<br>
      <span class="highlight">오렌지 하이라이트</span>
    </div>
  </div>
  <div class="slide-footer">
    <div class="brand">@계정명</div>
    <div class="progress-dots"><!-- 현재 위치 active --></div>
  </div>
</div>
<br><br>

<!-- 리스트 -->
<div class="slide content">
  <div class="slide-num">03 / 07</div>
  <div style="flex:1;padding:20px 0">
    <div class="content-title" style="margin-bottom:40px">리스트 제목</div>
    <div class="list-item"><div class="list-num">1</div><div class="list-content"><div class="list-title">항목명</div><div class="list-desc">설명</div></div></div>
    <!-- 반복 -->
  </div>
  <div class="slide-footer"><!-- 푸터 --></div>
</div>
<br><br>

<!-- 포인트 -->
<div class="slide point">
  <div class="big-number">★</div>
  <div class="point-text">"핵심 메시지를<br>한 문장으로"</div>
</div>
<br><br>

<!-- 마무리 -->
<div class="slide outro">
  <div class="deco-line"></div>
  <div class="outro-quote">"인용구 또는 핵심 메시지"</div>
  <div class="outro-footer">
    <div><div class="author-name">작성자명</div><div class="author-handle">@계정</div></div>
    <div class="cta-text">저장하고<br>나중에 보세요 💾</div>
  </div>
</div>

</body></html>
```

---

## 4. B시리즈 — 비주얼 네이티브 (인디고 다크)

### CSS (완전본)
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
.slide { width: 1080px; height: 1080px; font-family: 'Noto Sans KR', sans-serif; position: relative; overflow: hidden; }
/* 표지 */
.slide.cover-B {
  background: #0a0a0f; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center;
}
.cover-B .series-tag { font-size: 20px; font-weight: 500; color: #6366f1; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 32px; }
.cover-B .main-term { font-size: 140px; font-weight: 900; color: #fff; line-height: 1; letter-spacing: -4px; margin-bottom: 16px; position: relative; display: inline-block; }
.cursor { display: inline-block; width: 8px; height: 120px; background: #6366f1; margin-left: 8px; vertical-align: bottom; animation: blink 1s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
.cover-B .term-def { font-size: 32px; color: #888; font-weight: 400; }
.cover-B .bottom-bar { position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #6366f1, #818cf8, #a5b4fc); }
/* 정의 */
.slide.definition { background: #13131b; display: flex; flex-direction: column; padding: 70px 80px; }
.def-label { font-size: 20px; font-weight: 600; color: #6366f1; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 48px; }
.def-icon { font-size: 100px; margin-bottom: 40px; line-height: 1; }
.def-title { font-size: 56px; font-weight: 900; color: #fff; margin-bottom: 28px; word-break: keep-all; }
.def-body { font-size: 32px; color: #aaa; line-height: 1.7; word-break: keep-all; flex: 1; }
.def-body strong { color: #fff; }
.def-body .accent { color: #818cf8; font-weight: 700; }
/* 비유 */
.slide.analogy { background: linear-gradient(135deg, #0f0f1a, #1a1a2e); display: flex; flex-direction: column; padding: 70px 80px; justify-content: center; }
.analogy-label { font-size: 20px; color: #10b981; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 48px; font-weight: 600; }
.analogy-main { display: flex; align-items: center; gap: 48px; margin-bottom: 48px; }
.analogy-emoji { font-size: 120px; flex-shrink: 0; line-height: 1; }
.analogy-text { font-size: 40px; color: #e0e0e0; line-height: 1.5; word-break: keep-all; }
.analogy-text .keyword { color: #34d399; font-weight: 800; }
.analogy-sub { background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.15); border-radius: 16px; padding: 28px 36px; font-size: 28px; color: #888; line-height: 1.6; word-break: keep-all; }
/* 활용 관점 */
.slide.marketer-view { background: #0a0a0f; display: flex; flex-direction: column; padding: 70px 80px; }
.mv-label { font-size: 20px; color: #f59e0b; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 48px; font-weight: 600; }
.mv-title { font-size: 52px; font-weight: 900; color: #fff; margin-bottom: 48px; word-break: keep-all; }
.mv-cards { display: flex; flex-direction: column; gap: 20px; flex: 1; }
.mv-card { background: rgba(245,158,11,0.05); border: 1px solid rgba(245,158,11,0.15); border-radius: 16px; padding: 24px 28px; display: flex; align-items: center; gap: 20px; }
.mv-card-icon { font-size: 36px; flex-shrink: 0; }
.mv-card-text { font-size: 28px; color: #ccc; line-height: 1.5; word-break: keep-all; }
.mv-card-text strong { color: #fcd34d; }
/* 정리 */
.slide.summary-B { background: #13131b; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 70px 80px; }
.summary-badge { font-size: 20px; font-weight: 600; color: #6366f1; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 40px; }
.summary-title { font-size: 60px; font-weight: 900; color: #fff; margin-bottom: 48px; word-break: keep-all; }
.summary-points { display: flex; flex-direction: column; gap: 20px; width: 100%; text-align: left; }
.summary-point { display: flex; align-items: center; gap: 20px; background: rgba(99,102,241,0.06); border-radius: 14px; padding: 22px 28px; }
.sp-check { font-size: 28px; flex-shrink: 0; }
.sp-text { font-size: 28px; color: #ddd; word-break: keep-all; }
.sp-text strong { color: #a5b4fc; }
.follow-cta { margin-top: 48px; font-size: 26px; color: #555; }
.follow-cta span { color: #6366f1; }
```

### B시리즈 슬라이드 구성 (5-6장)
1. **표지** `cover-B` — 시리즈 태그 + 핵심 용어(대형) + 커서 애니메이션 + 영문명
2. **정의** `definition` — 이모지 + 제목 + 쉬운 설명
3. **비유** `analogy` — 실생활 비유 이모지 + 비유 텍스트 + 한 줄 요약 박스
4. **활용 관점** `marketer-view` — 활용 이유 카드 3개
5. **정리** `summary-B` — 핵심 3줄 체크리스트 + 팔로우 CTA

### B시리즈 HTML 패턴

```html
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<title>슬라이드 — B시리즈</title>
<style>/* 위 CSS 전체 삽입 */</style></head><body>

<!-- 표지 -->
<div class="slide cover-B">
  <div class="series-tag">알쓸IT잡 · IT단어장</div>
  <div class="main-term">용어<span class="cursor"></span></div>
  <div class="term-def">English Full Name</div>
  <div class="bottom-bar"></div>
</div>
<br><br>

<!-- 정의 -->
<div class="slide definition">
  <div class="def-label">Definition · 정의</div>
  <div class="def-icon">🔌</div>
  <div class="def-title">용어가 뭔가요?</div>
  <div class="def-body">
    쉬운 설명 <strong>핵심 개념</strong><br><br>
    <span class="accent">핵심 문구</span>
  </div>
</div>
<br><br>

<!-- 비유 -->
<div class="slide analogy">
  <div class="analogy-label">Real Life · 실생활 비유</div>
  <div class="analogy-main">
    <div class="analogy-emoji">🍽️</div>
    <div class="analogy-text"><span class="keyword">비유 키워드</span>와 같습니다</div>
  </div>
  <div class="analogy-sub">흐름 설명: A → B → C</div>
</div>
<br><br>

<!-- 활용 관점 -->
<div class="slide marketer-view">
  <div class="mv-label">Why it matters · 왜 중요한가</div>
  <div class="mv-title">이게 왜 필요할까?</div>
  <div class="mv-cards">
    <div class="mv-card"><div class="mv-card-icon">📊</div><div class="mv-card-text"><strong>이유 1</strong> — 설명</div></div>
    <div class="mv-card"><div class="mv-card-icon">🤖</div><div class="mv-card-text"><strong>이유 2</strong> — 설명</div></div>
    <div class="mv-card"><div class="mv-card-icon">⚡</div><div class="mv-card-text"><strong>이유 3</strong> — 설명</div></div>
  </div>
</div>
<br><br>

<!-- 정리 -->
<div class="slide summary-B">
  <div class="summary-badge">Summary · 정리</div>
  <div class="summary-title">핵심 요약</div>
  <div class="summary-points">
    <div class="summary-point"><div class="sp-check">✅</div><div class="sp-text">요약 1 — <strong>강조</strong></div></div>
    <div class="summary-point"><div class="sp-check">✅</div><div class="sp-text">요약 2 — <strong>강조</strong></div></div>
    <div class="summary-point"><div class="sp-check">✅</div><div class="sp-text">요약 3 — <strong>강조</strong></div></div>
  </div>
  <div class="follow-cta">더 알고 싶다면 팔로우 → <span>@계정명</span></div>
</div>

</body></html>
```

---

## 5. C시리즈 — 시네마틱 (필름 / 감성)

### CSS (완전본)
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
.slide { width: 1080px; height: 1080px; font-family: 'Noto Sans KR', sans-serif; position: relative; overflow: hidden; background: #1c1c1e; color: #ffffff; }
/* 표지 */
.slide.cinematic-cover { display: flex; flex-direction: column; justify-content: flex-end; padding: 80px; background: #000; }
.film-strip { position: absolute; top: 0; left: 0; right: 0; height: 8px; display: flex; gap: 2px; }
.film-hole { flex: 1; background: rgba(255,255,255,0.08); border-radius: 2px; }
.cover-eyebrow { font-size: 20px; font-weight: 300; color: #f5a623; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 32px; }
.cover-main-title { font-size: 80px; font-weight: 700; color: #fff; line-height: 1.2; letter-spacing: -1.5px; margin-bottom: 24px; word-break: keep-all; }
.cover-sub { font-size: 28px; font-weight: 300; color: rgba(255,255,255,0.5); line-height: 1.6; word-break: keep-all; padding-bottom: 60px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.cover-author { margin-top: 36px; display: flex; align-items: center; gap: 16px; }
.author-dot { width: 6px; height: 6px; border-radius: 50%; background: #f5a623; }
.author-info { font-size: 22px; font-weight: 400; color: rgba(255,255,255,0.4); }
.cover-bg-num { position: absolute; top: 50%; right: -40px; transform: translateY(-50%); font-size: 400px; font-weight: 900; color: rgba(255,255,255,0.02); line-height: 1; }
/* 텍스트 중심 본문 */
.slide.cinematic-content { background: #1c1c1e; display: flex; flex-direction: column; padding: 70px 80px; }
.chapter-label { font-size: 18px; color: #f5a623; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 56px; }
.main-quote { font-size: 56px; font-weight: 700; color: #fff; line-height: 1.35; letter-spacing: -0.5px; margin-bottom: 40px; word-break: keep-all; flex: 1; display: flex; align-items: center; }
.main-quote em { color: #f5a623; font-style: normal; }
.sub-text { font-size: 28px; font-weight: 300; color: rgba(255,255,255,0.45); line-height: 1.7; word-break: keep-all; }
/* 비포애프터 */
.slide.before-after { background: #141414; display: flex; flex-direction: column; padding: 70px 80px; }
.ba-label { font-size: 18px; color: #f5a623; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 48px; }
.ba-cards { display: flex; gap: 24px; flex: 1; }
.ba-card { flex: 1; border-radius: 20px; padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }
.ba-card.before { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
.ba-card.after { background: rgba(245,166,35,0.06); border: 1px solid rgba(245,166,35,0.2); }
.ba-tag { font-size: 16px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 28px; }
.ba-card.before .ba-tag { color: rgba(255,255,255,0.3); }
.ba-card.after .ba-tag { color: #f5a623; }
.ba-content { font-size: 34px; font-weight: 500; color: #fff; line-height: 1.5; word-break: keep-all; flex: 1; display: flex; align-items: center; }
/* 인용 강조 */
.slide.pull-quote { background: #000; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px; text-align: center; }
.pq-mark { font-size: 160px; font-weight: 900; color: rgba(245,166,35,0.15); line-height: 0.7; margin-bottom: 24px; }
.pq-text { font-size: 52px; font-weight: 700; color: #fff; line-height: 1.4; letter-spacing: -0.5px; word-break: keep-all; }
.pq-text em { color: #f5a623; font-style: normal; }
.pq-source { margin-top: 48px; font-size: 22px; color: rgba(255,255,255,0.3); letter-spacing: 2px; }
/* 클로징 */
.slide.cinematic-closing { background: #000; display: flex; flex-direction: column; justify-content: flex-end; padding: 80px; }
.closing-text { font-size: 42px; font-weight: 300; color: rgba(255,255,255,0.7); line-height: 1.6; word-break: keep-all; margin-bottom: 60px; }
.closing-text strong { color: #fff; font-weight: 700; }
.closing-divider { width: 60px; height: 2px; background: #f5a623; margin-bottom: 40px; }
.closing-footer { display: flex; justify-content: space-between; align-items: flex-end; }
.closing-name { font-size: 36px; font-weight: 700; color: #fff; }
.closing-handle { font-size: 24px; color: rgba(255,255,255,0.3); margin-top: 8px; }
.closing-cta { font-size: 24px; color: rgba(255,255,255,0.3); text-align: right; }
```

### C시리즈 슬라이드 구성 (6-8장)
1. **표지** `cinematic-cover` — 아이브로우 + 제목 + 부제목 + 필름스트립
2. **텍스트 중심** `cinematic-content` × 2-3장 — 챕터 레이블 + 핵심 문장
3. **비포/애프터** `before-after` — 2분할 비교 카드
4. **인용 강조** `pull-quote` — 큰따옴표 + 핵심 문장
5. **클로징** `cinematic-closing` — 마무리 문장 + 작성자

### C시리즈 HTML 패턴

```html
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<title>슬라이드 — C시리즈</title>
<style>/* 위 CSS 전체 삽입 */</style></head><body>

<!-- 표지 -->
<div class="slide cinematic-cover">
  <div class="film-strip"><!-- .film-hole × 40개 --></div>
  <div class="cover-bg-num">1</div>
  <div class="cover-eyebrow">시리즈명 · 에피소드</div>
  <div class="cover-main-title">메인 제목</div>
  <div class="cover-sub">부제목 설명문</div>
  <div class="cover-author">
    <div class="author-dot"></div>
    <div class="author-info">작성자 @계정명</div>
  </div>
</div>
<br><br>

<!-- 텍스트 중심 본문 -->
<div class="slide cinematic-content">
  <div class="chapter-label">Chapter 01 · 시작</div>
  <div class="main-quote">"핵심 문장에서<br><em>강조 키워드</em>를 담아"</div>
  <div class="sub-text">보조 설명 텍스트</div>
</div>
<br><br>

<!-- 비포/애프터 -->
<div class="slide before-after">
  <div class="ba-label">Before / After · 변화</div>
  <div class="ba-cards">
    <div class="ba-card before">
      <div class="ba-tag">Before</div>
      <div class="ba-content">이전 상태 설명</div>
    </div>
    <div class="ba-card after">
      <div class="ba-tag">After</div>
      <div class="ba-content">변화된 상태 설명</div>
    </div>
  </div>
</div>
<br><br>

<!-- 인용 강조 -->
<div class="slide pull-quote">
  <div class="pq-mark">"</div>
  <div class="pq-text">가장 기억에 남을<br><em>핵심 문장 하나</em></div>
  <div class="pq-source">출처 또는 소제목</div>
</div>
<br><br>

<!-- 클로징 -->
<div class="slide cinematic-closing">
  <div class="closing-text"><strong>강조 문구</strong>로 마무리하는<br>문장입니다.</div>
  <div class="closing-divider"></div>
  <div class="closing-footer">
    <div><div class="closing-name">작성자명</div><div class="closing-handle">@계정</div></div>
    <div class="closing-cta">저장하고<br>다시 보세요</div>
  </div>
</div>

</body></html>
```

---

## 6. 콘텐츠 생성 규칙

### 텍스트 분량
| 요소 | 권장 글자 수 |
|------|-------------|
| 표지 제목 | 12-20자 |
| 본문 제목 | 15-25자 |
| 본문 텍스트 | 60-120자 (줄바꿈 포함) |
| 리스트 항목 설명 | 25-50자 |
| 인용구/클로징 | 40-80자 |

### 한국어 작성 원칙
- `word-break: keep-all` 이미 적용됨 → 단어 중간 줄바꿈 없음
- `<br>` 로 의도적 줄바꿈 추가 (리듬감)
- 강조: `<strong>`, `<span class="highlight/accent/keyword">` 활용
- 이모지: B시리즈 적극 활용, A/C시리즈 절제

### progress-dots 규칙
- 총 슬라이드 수만큼 `.dot` 생성
- 현재 슬라이드까지 `.dot.active`
- 표지와 마무리는 항상 1번째/마지막 active

### 파일명 규칙
```
slide-[주제키워드]-YYYYMMDD.html
예: slide-ai-마케팅루틴-20250225.html
    slide-api-개념설명-20250225.html
```

---

## 7. 실행 순서

1. 주제·시리즈·슬라이드 수 파악 (미지정 시 자동 결정)
2. 콘텐츠 구조 설계 (슬라이드별 제목 + 요지)
3. HTML 파일 생성 (`output/slides/` 또는 현재 디렉터리)
4. 검증 체크리스트 자체 확인:
   - [ ] 모든 슬라이드 1080×1080 유지
   - [ ] overflow: hidden 적용
   - [ ] 외부 이미지 URL 없음
   - [ ] progress-dots 정확히 표시
   - [ ] 텍스트 오버플로우 없음
5. 파일 경로를 사용자에게 알림

---

## 8. D시리즈 추가 예정

D시리즈(포토 카드) — 배경 이미지 + 텍스트 오버레이 스타일
현재 `hf-card-generators/photo-card-generator/`에서 HuggingFace Gradio로 제공
