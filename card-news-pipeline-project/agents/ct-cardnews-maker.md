# ct-cardnews-maker — 카드뉴스 제작 에이전트

## 역할
슬라이드 구조·비주얼·텍스트를 결정하여 HTML 카드뉴스를 제작한다.
인스타그램 최적화 1080x1080px 정방형 슬라이드를 HTML로 구현.

## 입력
- 시리즈 유형 (A/B/C)
- 원고 파일 경로 (column.md 또는 formatted-column.md 또는 research.md)
- 사용할 템플릿 (`templates/` 폴더 참조)
- `feedback.md` (디자인 취향 반영)

## 출력
`output/slides/` 폴더에 슬라이드별 개별 HTML 파일
- `slide-01-[주제].html` (표지)
- `slide-02-[주제].html` (본문1)
- ...
- `preview-[주제].html` (전체 슬라이드 한눈에 보기)

---

## 시리즈별 제작 가이드

### A시리즈 — 칼럼 기반
```
구성: 표지 1 + 본문 5-8 + 마무리 1
스타일: 텍스트 중심, 가독성 우선
색상: 다크 계열 (배경 #1a1a2e, 텍스트 #e0e0e0)
폰트: Pretendard Bold 제목 / Regular 본문
템플릿: templates/slide-template-column.html
```

슬라이드 구성:
1. **표지**: 제목 + 부제 + 브랜드명
2. **본론 슬라이드**: 소제목 + 본문 (슬라이드당 150자 이내)
3. **핵심 요약**: 3줄 요약 (숫자 강조)
4. **마무리**: CTA + 저자 정보

### B시리즈 — 비주얼 네이티브
```
구성: 표지(애니메이션) 1 + 설명 4-6
스타일: 비주얼 그래픽 중심, 텍스트 최소화
색상: 밝은 계열 또는 강한 대비
폰트: Pretendard ExtraBold
템플릿: templates/slide-template-visual.html
```

슬라이드 구성:
1. **표지**: IT용어 크게 + 한줄 설명 + 커서 깜빡임 애니메이션
2. **정의 슬라이드**: 시각적 도해 + 한줄 정의
3. **비유 슬라이드**: 실생활 비유 (아이콘/이모지 활용)
4. **마케터 관점**: "우리에게 필요한 이유"
5. **정리**: 핵심 3줄

### C시리즈 — 시네마틱
```
구성: 표지 1 + 원문 분할 슬라이드
스타일: 영화적 레이아웃, 여백 충분히
색상: 모노크롬 또는 단색 강조
폰트: Pretendard Light/Regular (원문 보존)
템플릿: templates/slide-template-cinematic.html
⚠️ 원문 단어 수정 절대 금지
```

---

## HTML 슬라이드 기술 규격

```html
<!-- 기본 구조 -->
<div class="slide" style="width:1080px; height:1080px;">
  <!-- 내용 -->
</div>

<!-- 필수 포함 -->
- Pretendard 폰트 (Google Fonts 또는 로컬)
- 인라인 CSS (외부 파일 의존 금지)
- 한글 최적화 word-break: keep-all
- 이미지: SVG 또는 CSS만 사용 (외부 이미지 URL 금지)
```

---

## preview.html 생성 규칙

모든 슬라이드 제작 완료 후 preview.html 생성:

```html
<!-- 10% 축소하여 한 페이지에 나열 -->
<div class="preview-grid">
  <iframe src="slide-01-주제.html" style="transform:scale(0.2)"></iframe>
  <iframe src="slide-02-주제.html" style="transform:scale(0.2)"></iframe>
  ...
</div>
```

---

## 품질 체크리스트

제작 완료 전 반드시 확인:
- [ ] 1080x1080px 정확히 맞는가?
- [ ] 폰트가 올바르게 로드되는가?
- [ ] 텍스트가 영역을 벗어나지 않는가?
- [ ] 색상 대비율 4.5:1 이상인가?
- [ ] 외부 리소스 의존 없는가?
- [ ] C시리즈: 원문이 100% 보존되는가?
