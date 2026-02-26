# PRD — project1 Team Orchestrator

**문서 버전**: 1.0  
**작성일**: 2026.02.26  
**분석 원본**: team-orchestra.png  

---

## 1. 개요

`team-orchestrator` 는 복잡한 작업을 전문 에이전트들에게 자동 위임하는 멀티에이전트 오케스트레이션 시스템이다.  
사용자는 자연어로 요청하면, 오케스트레이터가 최적의 에이전트 조합을 선택해 병렬 또는 순차 실행한다.

---

## 2. 팀 구성 (설치된 에이전트)

| 에이전트 | 역할 |
|---------|------|
| `business-analyst` | 비즈니스 프로세스 분석, 요구사항 정의, 개선 기회 식별 |
| `content-marketer` | SNS 콘텐츠 전략, 채널별 콘텐츠 제작, 캠페인 기획 |
| `context-manager` | 멀티에이전트 워크플로우의 컨텍스트 보존 및 세션 조율 |
| `planner` | 구현 계획 수립, 단계별 작업 분해, 의존성 관리 |
| `prompt-engineer` | LLM 프롬프트 설계, 최적화, 평가 |
| `report-generator` | 리서치 결과를 구조화된 보고서로 변환 |
| `research-coordinator` | 복합 리서치 전략 수립, 전문 리서처 조율 |
| `social-media-clip-creator` | 플랫폼별 영상 클립 최적화, 자막/썸네일 생성 |
| `social-media-copywriter` | 트위터 스레드, 링크드인, 인스타그램 카피라이팅 |
| `technical-writer` | API 문서, 사용자 가이드, SDK 문서 작성 |

---

## 3. 실행 패턴

### 병렬 실행
```
"SNS 마케팅 전략 전체 짜줘"
→ content-marketer + research-coordinator 동시 실행
```

### 순차 실행 (파이프라인)
```
"이 프로젝트 분석하고 문서화해줘"
→ business-analyst → technical-writer

"리포트 작성해줘"
→ research-coordinator → report-generator
```

### 혼합 실행
```
"SNS 콘텐츠 + 보고서 동시에"
→ [content-marketer + research-coordinator] 병렬
→ [social-media-copywriter + report-generator] 각각 수령
```

---

## 4. 워크플로우 설계

```
사용자 요청
    ↓
[project1 오케스트레이터] — 의도 분석 + 에이전트 선택
    ↓
┌─────────────────────────────────┐
│ 병렬 실행 가능 여부 판단         │
│ - 독립적 작업 → 병렬             │
│ - 의존성 있음 → 순차             │
└─────────────────────────────────┘
    ↓
[전문 에이전트 실행]
    ↓
[context-manager] — 중간 결과 통합
    ↓
최종 산출물 전달
```

---

## 5. 활성화 트리거

| 요청 유형 | 활성화 에이전트 |
|---------|--------------|
| 마케팅 전략 | content-marketer + research-coordinator |
| 분석 + 문서화 | business-analyst → technical-writer |
| 리포트 작성 | research-coordinator → report-generator |
| SNS 콘텐츠 | social-media-copywriter + social-media-clip-creator |
| 프롬프트 개발 | prompt-engineer + planner |
| 프로젝트 계획 | planner + business-analyst |

---

## 6. 성공 지표

- 단일 요청으로 다중 에이전트 자동 조율
- 중간 컨텍스트 손실 없음 (context-manager 보장)
- 병렬 실행으로 처리 시간 40–70% 단축
- 산출물: 구조화된 문서 / 콘텐츠 / 보고서

---

## 7. 제약 조건

- 에이전트 간 데이터 포맷 통일 필요
- context-manager 없이 5단계 이상 파이프라인 지양
- 병렬 에이전트는 최대 3개 동시 실행 권장

---

## 8. 파일 구조

```
.claude/
└── agents/
    ├── project1.md              ← 이 프로젝트 오케스트레이터
    ├── business-analyst.md
    ├── content-marketer.md
    ├── context-manager.md
    ├── planner.md
    ├── prompt-engineer.md
    ├── report-generator.md
    ├── research-coordinator.md
    ├── social-media-clip-creator.md
    ├── social-media-copywriter.md
    └── technical-writer.md
```
