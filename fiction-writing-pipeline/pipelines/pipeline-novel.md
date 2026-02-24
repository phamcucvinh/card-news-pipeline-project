# Pipeline Novel — 장편소설

## 개요
- **대상**: 장편소설 (5만 자 이상, 15-30챕터 기준)
- **컨펌 횟수**: 5회
- **참여 에이전트**: fw-concepter, fw-world-builder, fw-plotter, fw-writer, fw-editor
- **주요 산출물**: 로그라인 + 캐릭터 시트 + 세계관 노트 + 씬 카드 + 챕터 초고 전체 + DOCX 완성본

---

## 실행 순서

### 📥 Step 0: 시작
```
작가 입력: "Novel — [아이디어]로 장편소설 써줘"
```
→ `feedback.md` 로드하여 작가 취향 파악
→ Novel 파이프라인 시작 선언

---

### 💡 Step 1: 컨셉 — 로그라인 3안
```
호출: fw-concepter (→ skills/logline-writer.md)
입력: 작가 아이디어
출력: output/concepts/logline-[임시제목]-[YYYYMMDD].md
```
- 장르·톤 분석
- 로그라인 3안 (외적·내적·테마 각도)
- 추천안 제시

---

### ⭐ 컨펌 1 — 로그라인 확정

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 로그라인 3안 완성 — 작가 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[로그라인 안 1 — 외적 갈등]
[로그라인 안 2 — 내적 갈등]
[로그라인 안 3 — 테마]

추천: 안 [N] — [이유]

✅ 마음에 드는 안을 선택하거나 수정 방향을 알려주세요
```

작가 응답 대기 → 확정된 로그라인으로 Step 2 진행

---

### 🌍 Step 2: 세계관 + 인물 설계
```
호출: fw-world-builder
  → skills/world-notes.md → output/worldbuilding/worldnotes-[제목]-[YYYYMMDD].md
  → skills/character-sheet.md → output/characters/characters-[제목]-[YYYYMMDD].md
입력: 확정된 로그라인
```
- 세계관 노트 (시공간·규칙·사회 구조·주요 장소)
- 주인공 상세 시트 + 주요 인물 시트

---

### ⭐ 컨펌 2 — 세계관 / 인물 승인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 세계관 + 인물 설계 완료 — 작가 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[세계관 핵심 요약]
[인물 목록 및 핵심 정보]

✅ 승인하면 플롯 설계를 시작합니다
✏️ 수정하면 수정 내용을 알려주세요
```

---

### 🗺️ Step 3: 플롯 + 씬 카드 전체
```
호출: fw-plotter
  → 3막 아웃라인 작성 (templates/three-act-template.md 기반)
  → skills/scene-card-maker.md → output/structure/scene-cards-[제목]-[YYYYMMDD].md
입력: 로그라인 + 세계관 노트 + 캐릭터 시트
```
- 3막 아웃라인 확정
- 전체 씬 카드 (40-80씬)

---

### ⭐ 컨펌 3 — 구조 승인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 3막 아웃라인 + 씬 카드 완성 — 작가 확인 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[3막 아웃라인 요약]
[씬 카드 목록 (제목 + 위치)]

✅ 승인하면 챕터 집필을 시작합니다
✏️ 수정하면 수정 내용을 알려주세요
```

---

### ✍️ Step 4: 챕터별 초고 집필 (반복)
```
호출: fw-writer (→ skills/draft-writer.md) — 챕터별 반복 실행
입력: scene-cards.md + characters.md + worldnotes.md
출력: output/drafts/chapter-[N]-[제목]-[YYYYMMDD].md
```
- 씬 카드 기반으로 챕터 순서대로 집필
- 각 챕터 3,000-5,000자

---

### ⭐ 컨펌 4 — 초고 방향 확인

전체 초고의 1/3 완성 시점에 중간 체크:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 초고 1/3 완성 — 중간 점검
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

완성: 챕터 1-[N]
[첫 챕터 미리보기 일부]

✅ 방향이 맞으면 나머지 챕터를 계속 씁니다
✏️ 수정 방향이 있으면 알려주세요
```

---

### 🔧 Step 5: 3단계 편집
```
호출: fw-editor
  1차: skills/structural-editor.md → 구조 편집
  2차: skills/character-editor.md → 캐릭터 편집
  3차: skills/prose-editor.md → 문장 편집
입력: output/drafts/ 전체
출력: output/final/[제목]-final.md
```

---

### ⭐ 컨펌 5 — 최종 승인

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ 3단계 편집 완료 — 최종 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

편집 메모 요약:
- 구조: [주요 변경 사항]
- 캐릭터: [주요 변경 사항]
- 문장: [주요 변경 사항]

✅ 승인하면 DOCX 파일로 저장합니다
✏️ 추가 수정이 필요하면 알려주세요
```

---

### 📦 Step 6: DOCX 저장 (자동)
```
호출: skills/save-to-docx.md
입력: output/final/[제목]-final.md
출력: output/final/[제목]-final-[YYYYMMDD].docx
```

---

### 🏁 Step 7: 마무리
```
작업 완료 알림 + feedback.md 업데이트
```

```
장편소설 완성을 축하합니다 🎉

📁 저장 위치: output/final/[제목]-final-[YYYYMMDD].docx
📊 분량: 약 [X]만 자, [N]챕터

이번 작업 어떠셨나요?
다음에 개선할 점이 있으면 알려주세요 😊
```
