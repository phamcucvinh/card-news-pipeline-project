# Pipeline Short — 단편소설

## 개요
- **대상**: 단편소설 (8,000-15,000자, 단일 아크)
- **컨펌 횟수**: 3회
- **참여 에이전트**: fw-concepter, fw-plotter, fw-writer, fw-editor
- **주요 산출물**: 로그라인 + 씬 카드 + 초고 + DOCX 완성본
- **특이점**: 세계관 노트 생략 가능 (간단한 설정이면 씬 카드에 통합)

---

## 실행 순서

### 📥 Step 0: 시작
```
작가 입력: "Short — [아이디어]로 단편소설 써줘"
```
→ `feedback.md` 로드
→ Short 파이프라인 시작 선언

---

### 💡 Step 1: 컨셉 + 구조 설계
```
호출: fw-concepter → 로그라인 + 단일 아크 아웃라인
호출: fw-plotter → skills/scene-card-maker.md
출력:
  - output/concepts/logline-[제목]-[YYYYMMDD].md
  - output/structure/scene-cards-[제목]-[YYYYMMDD].md
```

단편 특화:
- 로그라인 1-2안 (장편보다 단순)
- 씬 카드 10-20씬
- 세계관은 씬 카드 상단에 간략 메모로 통합

---

### ⭐ 컨펌 1 — 로그라인 + 구조 동시 확인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 컨셉 + 구조 완성 — 작가 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[로그라인 1-2안]
[씬 카드 목록]

✅ 승인하면 집필을 시작합니다
✏️ 수정하면 수정 내용을 알려주세요
```

---

### ✍️ Step 2: 초고 집필 (한 번에 전체)
```
호출: fw-writer → skills/draft-writer.md
입력: scene-cards.md (전체)
출력: output/drafts/short-[제목]-[YYYYMMDD].md
```
- 전체 8,000-15,000자를 한 파일로 집필
- 씬 사이는 `---` 구분선

---

### ⭐ 컨펌 2 — 초고 확인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 단편 초고 완성 — 작가 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[초고 앞부분 미리보기]
분량: 약 [X]자

✅ 승인하면 편집 단계로 넘어갑니다
✏️ 방향 수정이 필요하면 알려주세요
```

---

### 🔧 Step 3: 3단계 편집 (압축 버전)
```
호출: fw-editor
  1차: skills/structural-editor.md (단편 특화 — 씬 흐름 집중)
  2차: skills/character-editor.md (주인공 집중)
  3차: skills/prose-editor.md
입력: output/drafts/short-[제목].md
출력: output/final/[제목]-final.md
```

단편 편집 특화:
- 구조 편집: 전체 흐름 + 결말의 여운
- 캐릭터 편집: 주인공 단일 아크 집중
- 문장 편집: 오프닝과 결말 문장 특히 신경

---

### ⭐ 컨펌 3 — 최종 승인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 편집 완료 — 최종 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[편집 메모 요약]

✅ 승인하면 DOCX로 저장합니다
✏️ 추가 수정이 필요하면 알려주세요
```

---

### 📦 Step 4: DOCX 저장 + 마무리
```
호출: skills/save-to-docx.md
출력: output/final/[제목]-final-[YYYYMMDD].docx
```

```
단편소설 완성 🎉
output/final/[제목]-final-[YYYYMMDD].docx
```
