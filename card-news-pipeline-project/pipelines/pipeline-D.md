# Pipeline D — 뉴스레터

## 개요
- **시리즈**: D. 코마레터 (코딩하는 마케터 뉴스레터)
- **특징**: 칼럼 기반 이메일 뉴스레터 + 멀티채널 배포 패키지
- **JJ 컨펌**: 2회
- **참여 에이전트**: ct-researcher, ct-distributor
- **산출물**: 뉴스레터 본문 + 인스타/링크드인/스레드 배포본 + 해시태그

---

## 실행 순서

### 📥 Step 0: 시작
```
JJ 입력: "D시리즈 - [주제/키워드]로 뉴스레터 써줘" 또는
         "D시리즈 - [원문 텍스트 붙여넣기]"
```
→ `feedback.md` 로드
→ 발행 회차 확인 (히스토리 참조)

---

### 🔍 Step 1: 리서치 + 칼럼 작성
```
호출: ct-researcher
입력: 주제, 시리즈=D
출력: output/research/research-[주제]-[YYYYMMDD].md

호출: column-writer
입력: research.md
출력: output/columns/column-[주제]-[YYYYMMDD].md
```

---

### 📝 Step 2: 뉴스레터 초안 작성
```
호출: newsletter-writer
입력: column-[주제].md + research-[주제].md
출력: output/columns/newsletter-[주제]-[YYYYMMDD].md
```

---

### ⭐ 컨펌 1 — 뉴스레터 본문 확정

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 뉴스레터 초안 완료 — JJ 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[뉴스레터 전문 제시]

✅ 승인하면 배포 패키지 제작을 시작합니다
✏️ 수정하면 수정 내용을 알려주세요
```

---

### 📦 Step 3: 멀티채널 배포 패키지 제작
```
호출: ct-distributor
  → caption-writer → output/captions/caption-[주제].txt
  → hashtag-generator → 인스타/링크드인 해시태그 세트
  → linkedin-post → output/columns/linkedin-[주제].md
  → thread-writer → output/columns/thread-[주제].md
  → title-ab-tester → 제목 3안 (이메일 제목용)
입력: column-[주제].md + newsletter-[주제].md
```

---

### ⭐ 컨펌 2 — 배포 패키지 최종 확인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 배포 패키지 완성 — 최종 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 이메일 제목 3안:
  A. [감성형]
  B. [정보형]
  C. [질문형]

📁 산출물:
  ✅ 뉴스레터 본문
  ✅ 인스타그램 캡션 + 해시태그
  ✅ 링크드인 포스트
  ✅ 스레드 포스트

✅ 승인하면 모든 파일이 준비됩니다
✏️ 수정이 필요하면 알려주세요
```

---

### 🏁 Step 4: 마무리
```
JJ에게 회고 요청 → feedback.md 업데이트
발행 회차 기록 업데이트
```

---

## D시리즈 콘텐츠 원칙
- **발행 주기**: 주 1회 (월요일 오전 권장)
- **주제 선정**: A시리즈 칼럼 주제와 연동 또는 독립 주제
- **분량**: 뉴스레터 800-1,200자 + 배포 채널별 최적화
- **일관성**: 매호 "JJ's Pick" 코너 필수 포함
