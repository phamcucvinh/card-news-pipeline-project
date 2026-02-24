# 픽션 글쓰기 AI 파이프라인 PRD

## 제품 개요

- **목적**: AI 멀티에이전트 기반 픽션 창작 지원 시스템
- **대상**: 소설·단편·챕터 단위 글쓰기를 원하는 작가
- **원칙**: Human-in-the-Loop, 작가가 최종 결정권을 가진다
- **버전**: v1.0 | 작성일: 2026-02-24

---

## 핵심 원칙

1. **오케스트레이터는 집필하지 않는다** — 워크플로우 관리만 담당
2. **작가가 컨펌한 방향만 진행한다** — 어떤 단계도 무단으로 건너뛰지 않는다
3. **feedback.md를 항상 참조한다** — 작가의 취향이 모든 에이전트에 반영된다
4. **산출물은 반드시 output/에 저장한다** — 작업 히스토리를 유지한다
5. **3단계 편집을 거친다** — 구조 → 캐릭터 → 문장 순서로 품질을 높인다

---

## 파이프라인 유형

| 유형 | 대상 | 컨펌 횟수 | 에이전트 수 | 소요 단계 |
|------|------|----------|-----------|----------|
| Novel | 장편소설 (5만 자 이상) | 5회 | 5개 | 8단계 |
| Short | 단편소설 (1-2만 자) | 3회 | 3-4개 | 5단계 |
| Chapter | 단일 챕터 (3-5천 자) | 2회 | 2-3개 | 3단계 |

---

## 에이전트 구조

### 오케스트레이터 (CLAUDE.md)
- 전체 워크플로우 제어
- Human-in-the-Loop 컨펌 조율
- feedback.md 로드 및 업데이트
- **집필 금지** — 모든 생성 작업은 에이전트/스킬에 위임

### 전문 에이전트 (5개)

| 에이전트 | 담당 단계 | 주요 스킬 |
|----------|----------|----------|
| fw-concepter | 아이디어 → 로그라인 | logline-writer |
| fw-world-builder | 세계관 + 인물 설계 | world-notes, character-sheet |
| fw-plotter | 플롯 + 씬 카드 | scene-card-maker |
| fw-writer | 챕터별 초고 집필 | draft-writer |
| fw-editor | 3단계 편집 + DOCX | structural-editor, character-editor, prose-editor, save-to-docx |

### Executor 스킬 (9개)

| 스킬 | 기능 | 소속 에이전트 |
|------|------|------------|
| logline-writer | 로그라인 3안 생성 | fw-concepter |
| character-sheet | 캐릭터 시트 생성 | fw-world-builder |
| world-notes | 세계관 노트 생성 | fw-world-builder |
| scene-card-maker | 씬 카드 전체 생성 | fw-plotter |
| draft-writer | 챕터 초고 집필 | fw-writer |
| structural-editor | 구조 편집 (1차) | fw-editor |
| character-editor | 캐릭터 편집 (2차) | fw-editor |
| prose-editor | 문장 편집 (3차) | fw-editor |
| save-to-docx | DOCX 최종 저장 | fw-editor |

---

## Novel 파이프라인 상세 흐름

```
[입력] 작가의 아이디어 (1줄 ~ 1페이지)
  ↓
[STEP 1] fw-concepter → logline-writer → 로그라인 3안
  ↓ [컨펌 1] 작가가 로그라인 선택 + 수정
  ↓
[STEP 2] fw-world-builder → world-notes + character-sheet
  ↓ [컨펌 2] 세계관 / 인물 수정 또는 승인
  ↓
[STEP 3] fw-plotter → 3막 아웃라인 + scene-card-maker → 씬 카드 전체
  ↓ [컨펌 3] 구조 수정 또는 승인
  ↓
[STEP 4] fw-writer → draft-writer → 챕터별 초고 (반복)
  ↓ [컨펌 4] 초고 방향 확인 및 수정 지시
  ↓
[STEP 5] fw-editor → structural-editor → character-editor → prose-editor
  ↓ [컨펌 5] 최종 원고 승인
  ↓
[STEP 6] save-to-docx → output/final/ DOCX 저장
```

---

## 산출물 목록

| 단계 | 파일 위치 | 형식 |
|------|----------|------|
| 로그라인 | output/concepts/logline-[제목]-[YYYYMMDD].md | Markdown |
| 캐릭터 시트 | output/characters/characters-[제목]-[YYYYMMDD].md | Markdown |
| 세계관 노트 | output/worldbuilding/worldnotes-[제목]-[YYYYMMDD].md | Markdown |
| 씬 카드 | output/structure/scene-cards-[제목]-[YYYYMMDD].md | Markdown |
| 챕터 초고 | output/drafts/chapter-[N]-[제목]-[YYYYMMDD].md | Markdown |
| 최종 원고 | output/final/[제목]-final-[YYYYMMDD].docx | DOCX |

---

## 기술 의존성

- `synopsis-to-scenario-master/scripts/md_to_docx.py` — DOCX 변환에 재사용
- Python 3.8+ (md_to_docx 실행)
- python-docx 패키지

---

## 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2026-02-24 | 최초 작성 |
