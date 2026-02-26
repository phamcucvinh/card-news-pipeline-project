# project1 구성도

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    🎯 project1 구성도
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                       [ 사용자 ]
                           │
                           ▼
              ┌────────────────────────┐
              │      project1          │
              │   Team Orchestrator    │
              │  • 의도 분석            │
              │  • 에이전트 선택        │
              │  • 병렬/순차 판단       │
              └────────────┬───────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   [병렬 실행]       [순차 실행]       [혼합 실행]
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
         ┌─────────────────────────────────┐
         │         context-manager         │
         │     (3단계+ 파이프라인 조율)     │
         └──────────────┬──────────────────┘
                        │
     ┌──────────────────┼──────────────────┐
     │                  │                  │
     ▼                  ▼                  ▼
 [분석/계획]        [리서치/문서]       [콘텐츠/마케팅]
     │                  │                  │
 ┌───┴───┐          ┌───┴───┐          ┌───┴───┐
 │planner│     business  technical   content  social
 │       │     analyst   writer      marketer media
 └───────┘                                 copywriter
                research  report      social
                coord.    generator   media
                                     clip-creator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📌 실행 패턴
  ─────────────────────────────────────────────────
  SNS 전략      → content-marketer ┐ 병렬
                  research-coord  ┘
  분석+문서화   → business-analyst → technical-writer
  리포트        → research-coord  → report-generator
  프롬프트 개발 → planner → prompt-engineer
  ─────────────────────────────────────────────────

  🤖 10개 전문 에이전트
  ┌─────────────────────┬──────────────────────────┐
  │ business-analyst    │ 비즈니스 분석/요구사항    │
  │ content-marketer    │ 마케팅 전략/캠페인        │
  │ context-manager     │ 컨텍스트 보존/세션 조율   │
  │ planner             │ 구현 계획/작업 분해       │
  │ prompt-engineer     │ 프롬프트 설계/최적화      │
  │ report-generator    │ 보고서 작성/문서 변환     │
  │ research-coordinator│ 리서치 전략/정보 수집     │
  │ social-media-clip   │ 영상 클립/썸네일          │
  │ social-media-copy   │ SNS 카피/스레드           │
  │ technical-writer    │ 기술 문서/API 가이드      │
  └─────────────────────┴──────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
