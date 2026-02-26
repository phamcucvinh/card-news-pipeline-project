# Pipeline A — 코딩하는 마케터

## 개요
- **특징**: 칼럼 기반, 가장 풍부한 파이프라인
- **JJ 컨펌**: 3회
- **참여 에이전트**: 5-7개
- **산출물**: 카드뉴스 + 롱폼 + 스레드 (선택)
- **소요 시간**: 약 30-60분

---

## 실행 순서

### 📥 Step 0: 시작
```
JJ 입력: "A시리즈 - [주제/키워드]로 카드뉴스 만들어줘"
```
→ `feedback.md` 로드하여 JJ 취향 파악
→ 파이프라인 A 시작 선언

---

### 🔍 Step 1: 리서치
```
호출: ct-researcher
입력: 주제, 시리즈=A
출력: output/research/research-[주제]-[YYYYMMDD].md
```
- 웹 검색으로 팩트·트렌드·사례 수집
- research.md 구조에 맞게 작성

---

### 📋 Step 2: 방향성 + 제목 3안
```
호출: brief-writer
입력: output/research/research-[주제].md
출력: 채팅으로 JJ에게 직접 제시
```
- 콘텐츠 방향성 + 제목 3안 + 추천안 제시

---

### ⭐ 컨펌 1 — 방향성 + 제목 확정

```
🎬 리서치 + 방향성 완료 — JJ 확인 필요

[방향성 요약]
[제목 3안]

✅ 승인하면 칼럼 작성을 시작합니다
✏️ 수정하면 수정 내용 알려주세요
```

JJ 응답 대기 → 확정된 방향/제목으로 Step 3 진행

---

### ✍️ Step 3: 칼럼 작성
```
호출: column-writer
입력: research.md + 확정된 방향 + 확정된 제목
출력: output/columns/column-[주제]-[YYYYMMDD].md
```

---

### ⭐ 컨펌 2 — 칼럼 확정 + 산출물 선택

```
🎬 칼럼 작성 완료 — JJ 확인 필요

[칼럼 전문 제시]

원하는 산출물을 선택해 주세요 (복수 가능):
□ 카드뉴스 (인스타그램 슬라이드)
□ 롱폼 (브런치/링크드인)
□ 스레드 (스레드/X)

✅ 승인 + 선택하면 제작을 시작합니다
✏️ 칼럼 수정이 필요하면 알려주세요
```

JJ 응답 대기 → 선택한 산출물별로 Step 4 진행

---

### 🎨 Step 4: 산출물 제작 (선택별 분기, 병렬 가능)

#### □ 카드뉴스 선택 시
```
1. text-formatter → output/columns/formatted-column.md
2. ct-theme-designer → 테마 CSS 생성
3. ct-cardnews-maker → output/slides/slide-*.html
4. preview.html 생성
```

#### □ 롱폼 선택 시
```
longform-writer → output/columns/longform-[주제].md
```

#### □ 스레드 선택 시
```
thread-writer → output/columns/thread-[주제].md
```

---

### 🔍 Step 5: QA 검수 (자동)
```
실행: python scripts/validate_slide.py output/slides/
```
- 고/중 결함 발견 시 → ct-cardnews-maker에 수정 요청 → 재검증
- 저 결함만 남으면 → Step 6 진행

---

### ⭐ 컨펌 3 — 최종 결과물 검토

```
🎬 카드뉴스 제작 완료 — 최종 확인

[QA 결과 요약]
preview.html: output/slides/preview-[주제].html

✅ 승인하면 PNG 추출을 시작합니다
✏️ 수정이 필요하면 알려주세요
```

---

### 📦 Step 6: 파일 추출 (자동)
```
1. bash scripts/html_to_png.sh output/slides/ output/images/
2. caption-writer → output/captions/caption-[주제].txt
```
출력: `slide-*.png` + `caption.txt`

---

### 🏁 Step 7: 마무리
```
선택: save-to-notion (노션 저장)
필수: JJ에게 회고 요청 → feedback.md 업데이트
```

```
작업이 완료되었습니다 🎉

📁 저장 위치: output/
  📊 슬라이드: images/slide-*.png
  📝 캡션: captions/caption-[주제].txt
  [롱폼/스레드 선택 시 추가 파일]

이번 카드뉴스 어떠셨나요?
다음에 개선할 점 있으면 알려주세요 😊
```
