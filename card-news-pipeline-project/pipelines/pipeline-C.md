# Pipeline C — 커리어 레터

## 개요
- **특징**: 원문 보존, JJ가 쓴 글을 그대로 시네마틱 슬라이드화
- **JJ 컨펌**: 1회
- **참여 에이전트**: 2-3개
- **산출물**: 시네마틱 카드뉴스 PNG
- **소요 시간**: 약 10-20분
- **⚠️ 핵심**: 리서치 없음, 원문 수정 금지

---

## 실행 순서

### 📥 Step 0: 시작
```
JJ 입력: "C시리즈 - [원문 텍스트 붙여넣기]"
```
→ `feedback.md` 로드
→ 파이프라인 C 시작 선언
→ 원문 글자수 확인 및 예상 슬라이드 수 안내

---

### 📝 Step 1: 텍스트 포맷팅
```
호출: text-formatter
모드: C시리즈 (원문 보존 모드)
입력: JJ 원문 텍스트
출력: output/columns/formatted-column-[YYYYMMDD].md
```

포맷팅 원칙:
- ⚠️ 원문 단어 수정 절대 금지
- 슬라이드용 줄바꿈만 추가
- 강조어 **볼드** 처리
- 슬라이드 구분선 `---` 추가

---

### 🎨 Step 2: 카드뉴스 제작
```
호출: ct-cardnews-maker
모드: 시네마틱 (원문 보존 모드)
입력: output/columns/formatted-column.md
템플릿: templates/slide-template-cinematic.html
출력: output/slides/slide-*.html
```

시네마틱 스타일:
- 영화적 레이아웃 (충분한 여백)
- 모노크롬 또는 단색 강조
- 폰트: Pretendard Light (얇은 폰트)
- 원문 분위기 살리기

---

### ⭐ 컨펌 — 결과물 검토

```
🎬 커리어 레터 카드뉴스 완성 — JJ 확인

preview.html: output/slides/preview-career.html
슬라이드 수: [N]장

✅ 승인하면 PNG 추출합니다
✏️ 수정이 필요하면 알려주세요
   (원문 내용 수정 시 Step 1부터 재시작)
```

---

### 📦 Step 3: 파일 추출 (자동)
```
bash scripts/html_to_png.sh output/slides/ output/images/
caption-writer → output/captions/caption-career-[YYYYMMDD].txt
```

---

### 🏁 Step 4: 마무리
```
선택: save-to-notion
필수: feedback.md 업데이트
```

```
완료 🎉

📁 output/
  🖼️ images/slide-*.png
  📝 captions/caption-career-[날짜].txt

이번 커리어 레터 카드뉴스 어떠셨나요? 😊
글의 분위기가 잘 살았나요?
```
