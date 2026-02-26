# Pipeline B — 알쓸IT잡 (IT단어장)

## 개요
- **특징**: 슬라이드 네이티브, 리서치→카드뉴스 직행
- **JJ 컨펌**: 1회
- **참여 에이전트**: 2-3개
- **산출물**: 카드뉴스 PNG + 표지 MP4
- **소요 시간**: 약 15-30분

---

## 실행 순서

### 📥 Step 0: 시작
```
JJ 입력: "B시리즈 - [IT용어] 카드뉴스 해줘"
예시: "B시리즈 - API 카드뉴스 해줘"
```
→ `feedback.md` 로드
→ 파이프라인 B 시작 선언

---

### 🔍 Step 1: 리서치
```
호출: ct-researcher
입력: IT용어, 시리즈=B
출력: output/research/research-[용어]-[YYYYMMDD].md
```

수집 항목 (B시리즈 특화):
- 용어 정의 (공식 + 쉬운 버전)
- 실생활 비유 (3개 이상)
- 마케터에게 필요한 이유
- 실무 활용 사례

---

### 🎨 Step 2: 카드뉴스 제작 (칼럼 없이 바로 진행)
```
호출: ct-cardnews-maker
모드: 슬라이드 네이티브 (비주얼 그래픽 중심)
입력: output/research/research-[용어].md
템플릿: templates/slide-template-visual.html
출력: output/slides/slide-*.html
```

특징:
- maker가 슬라이드 구조·비주얼·텍스트 자율 결정
- 표지에 커서 깜빡임 CSS 애니메이션 적용
- 텍스트 최소화, 비주얼 중심

---

### 🔍 Step 3: QA 검수 (자동)
```
실행: python scripts/validate_slide.py output/slides/
```
- 고/중 결함 시 수정 반복
- 통과 후 → 컨펌

---

### ⭐ 컨펌 — 유일한 확인 포인트

```
🎬 카드뉴스 완성 — JJ 확인 필요

preview.html: output/slides/preview-[용어].html

✅ 승인하면 PNG + MP4 추출합니다
✏️ 수정이 필요하면 알려주세요
```

---

### 📦 Step 4: 파일 추출 (자동)
```
1. PNG 추출: html_to_png.sh (모든 슬라이드)
2. MP4 녹화: 표지 슬라이드 3초 녹화 (커서 애니메이션)
3. caption-writer → output/captions/caption-[용어].txt
```

출력:
- `output/images/slide-*.png`
- `output/images/cover-[용어].mp4` (표지 MP4)
- `output/captions/caption-[용어].txt`

---

### 🏁 Step 5: 마무리
```
선택: save-to-notion
필수: feedback.md 업데이트
```

```
완료 🎉

📁 output/
  🖼️ images/slide-*.png
  🎬 images/cover-[용어].mp4
  📝 captions/caption-[용어].txt

이번 [용어] 카드뉴스 어떠셨나요? 😊
```
