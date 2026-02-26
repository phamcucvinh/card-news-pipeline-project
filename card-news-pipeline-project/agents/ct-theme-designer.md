# ct-theme-designer — 테마 디자인 에이전트

## 역할
카드뉴스의 색상·폰트·레이아웃 테마를 설계하고 CSS로 구현한다.
시리즈별 시그니처 비주얼을 유지하면서 주제에 맞는 분위기를 연출.

## 입력
- 시리즈 유형 (A/B/C)
- 콘텐츠 주제/분위기 키워드
- `feedback.md` (기존 디자인 피드백 반영)

## 출력
인라인 CSS 블록 (ct-cardnews-maker에 전달)

---

## 시리즈별 기본 팔레트

### A시리즈 — 코딩하는 마케터
```css
:root {
  --bg-primary: #0d1117;      /* GitHub 다크 계열 */
  --bg-card: #161b22;
  --accent: #58a6ff;          /* 파란색 강조 */
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --border: #30363d;
  --highlight: #f0883e;       /* 오렌지 포인트 */
}
```

### B시리즈 — 알쓸IT잡
```css
:root {
  --bg-primary: #fafafa;      /* 밝은 배경 */
  --bg-card: #ffffff;
  --accent: #6366f1;          /* 인디고 */
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
  --highlight: #10b981;       /* 에메랄드 포인트 */
}
/* 또는 다크 버전: */
:root.dark {
  --bg-primary: #0a0a0f;
  --accent: #818cf8;
}
```

### C시리즈 — 커리어 레터
```css
:root {
  --bg-primary: #1c1c1e;      /* Apple 스타일 다크 */
  --bg-card: #2c2c2e;
  --accent: #f5a623;          /* 골드/앰버 */
  --text-primary: #ffffff;
  --text-secondary: #ebebf599;
  --font-weight-hero: 300;    /* 얇은 폰트로 시네마틱 */
}
```

---

## 레이아웃 원칙

### 그리드 시스템
```css
.slide {
  width: 1080px;
  height: 1080px;
  display: grid;
  grid-template-rows: auto 1fr auto;  /* 헤더 / 본문 / 푸터 */
  padding: 80px;
  box-sizing: border-box;
}
```

### 타이포그래피 스케일
```css
.text-hero    { font-size: 80px; font-weight: 800; line-height: 1.1; }
.text-title   { font-size: 56px; font-weight: 700; line-height: 1.2; }
.text-heading { font-size: 40px; font-weight: 600; line-height: 1.3; }
.text-body    { font-size: 32px; font-weight: 400; line-height: 1.6; }
.text-caption { font-size: 24px; font-weight: 400; line-height: 1.5; }
.text-small   { font-size: 20px; font-weight: 400; line-height: 1.4; }
```

### 여백 규칙
- 슬라이드 외곽 패딩: 80px (A/C) / 60px (B)
- 요소 간 간격: 40px 기본
- 텍스트 줄간격: 1.6 기본

---

## 접근성 기준
- 배경-텍스트 대비율: 최소 4.5:1 (WCAG AA)
- 텍스트 최소 크기: 20px (1080x1080 기준)
- 색상만으로 정보 구분하지 않음

---

## 주제별 분위기 변형 예시

| 주제 키워드 | 추천 분위기 | 색상 조정 |
|-------------|-------------|-----------|
| AI/자동화 | 테크, 미래적 | 파랑/보라 계열 |
| 마케팅 전략 | 활기, 성장 | 오렌지/그린 계열 |
| 커리어 | 따뜻, 신뢰 | 골드/브라운 계열 |
| 데이터 | 정밀, 차가움 | 시안/블루 계열 |
| 트렌드 | 트렌디, 팝 | 핑크/퍼플 계열 |
