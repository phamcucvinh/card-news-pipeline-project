# 픽션 글쓰기 AI 파이프라인

AI 멀티에이전트 기반 픽션 창작 지원 시스템.
아이디어 한 줄에서 DOCX 완성본까지, Human-in-the-Loop으로 작가가 모든 단계를 주도한다.

---

## 빠른 시작

```
"Novel — 조선시대 배경의 무협 로맨스 써줘"
"Short — AI가 감정을 갖게 된 근미래 단편소설 써줘"
"Chapter — [설정 파일 첨부] 3챕터 써줘"
"Poem — 첫눈 내리던 날 헤어진 사람, 자유시로 써줘"
```

---

## 파이프라인 유형

| 유형 | 설명 | 컨펌 횟수 |
|------|------|----------|
| **Novel** | 장편소설 전체 제작 | 5회 |
| **Short** | 단편소설 완성 | 3회 |
| **Chapter** | 단일 챕터 집필 | 2회 |
| **Poem** | 시 쓰기 (전 형식) | 2회 |

---

## 시스템 구조

```
fiction-writing-pipeline/
├── CLAUDE.md          ← 오케스트레이터 (워크플로우 제어)
├── PRD.md             ← 전체 시스템 요구사항
├── feedback.md        ← 작가 취향 누적 저장소
│
├── agents/            ← 전문 에이전트 (5개)
│   ├── fw-concepter.md      아이디어 → 로그라인
│   ├── fw-world-builder.md  세계관 + 인물 설계
│   ├── fw-plotter.md        플롯 + 씬 카드
│   ├── fw-writer.md         챕터 초고 집필
│   └── fw-editor.md         3단계 편집 + DOCX
│
├── skills/            ← Executor 스킬 (9개)
│   ├── logline-writer.md    로그라인 3안 생성
│   ├── character-sheet.md   캐릭터 시트 생성
│   ├── world-notes.md       세계관 노트 생성
│   ├── scene-card-maker.md  씬 카드 전체 생성
│   ├── draft-writer.md      챕터 초고 집필
│   ├── structural-editor.md 구조 편집 (1차)
│   ├── character-editor.md  캐릭터 편집 (2차)
│   ├── prose-editor.md      문장 편집 (3차)
│   └── save-to-docx.md      DOCX 최종 저장
│
├── pipelines/         ← 유형별 실행 순서
├── templates/         ← 캐릭터/씬카드/3막 템플릿
└── output/            ← 모든 산출물
```

---

## Novel 파이프라인 흐름

```
아이디어 입력
  ↓ STEP 1 — 컨셉터: 로그라인 3안
  ↓ [컨펌 1] 로그라인 선택
  ↓ STEP 2 — 월드빌더: 세계관 + 캐릭터 시트
  ↓ [컨펌 2] 세계관/인물 승인
  ↓ STEP 3 — 플로터: 3막 아웃라인 + 씬 카드
  ↓ [컨펌 3] 구조 승인
  ↓ STEP 4 — 라이터: 챕터별 초고 (반복)
  ↓ [컨펌 4] 초고 방향 확인
  ↓ STEP 5 — 에디터: 3단계 편집
  ↓ [컨펌 5] 최종 승인
  ↓ STEP 6 — DOCX 저장
```

---

## 기술 의존성

- Python 3.8+
- python-docx (`pip install python-docx`)
- DOCX 변환: `synopsis-to-scenario-master/scripts/md_to_docx.py` 재사용
