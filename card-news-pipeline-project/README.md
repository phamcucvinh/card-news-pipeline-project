# 카드뉴스 자동화 파이프라인

> 마케터 임지은의 AI 에이전트 기반 카드뉴스 제작 시스템

---

## 빠른 시작

이 폴더에서 Claude Code를 열고 다음과 같이 요청하세요:

```
# A시리즈 — 코딩하는 마케터 (주제 기반)
"A시리즈 - AI 마케팅 자동화로 카드뉴스 만들어줘"

# B시리즈 — 알쓸IT잡 (IT 용어 설명)
"B시리즈 - MCP 카드뉴스 해줘"

# C시리즈 — 커리어 레터 (원문 변환)
"C시리즈 - [원문 텍스트 붙여넣기]"
```

---

## 시스템 구조

```
오케스트레이터 (CLAUDE.md)
    │
    ├── 서브에이전트
    │   ├── ct-researcher       웹 리서치
    │   ├── ct-cardnews-maker   슬라이드 제작
    │   └── ct-theme-designer   테마 디자인
    │
    └── Executor 스킬 (9개)
        ├── brief-writer        방향성 + 제목 3안
        ├── column-writer       칼럼 작성
        ├── text-formatter      텍스트 포맷팅
        ├── caption-writer      SNS 캡션
        ├── longform-writer     롱폼 콘텐츠
        ├── thread-writer       스레드/X
        ├── save-to-notion      노션 저장
        ├── validate-slide      QA 검증
        └── html-to-png         PNG 변환
```

---

## 파이프라인 비교

| 구분 | A. 코딩하는 마케터 | B. 알쓸IT잡 | C. 커리어 레터 |
|------|-------------------|------------|----------------|
| 입력 | 주제/키워드 | IT 용어 | 원문 글 |
| 리서치 | ✅ | ✅ | ❌ |
| 칼럼 작성 | ✅ | ❌ | ❌ |
| JJ 컨펌 | 3회 | 1회 | 1회 |
| 산출물 | 카드뉴스+롱폼+스레드 | 카드뉴스(비주얼) | 카드뉴스(시네마틱) |
| 표지 | 정적 PNG | 애니메이션 MP4 | 정적 PNG |
| 에이전트 수 | 5~7개 | 2~3개 | 2~3개 |

---

## 파일 구조

```
card-news-pipeline-project/
├── CLAUDE.md                   ← 오케스트레이터 지시서 (핵심!)
├── README.md                   ← 이 파일
├── feedback.md                 ← JJ 취향 누적 저장소
│
├── agents/                     ← 공식 서브에이전트
│   ├── ct-researcher.md
│   ├── ct-cardnews-maker.md
│   └── ct-theme-designer.md
│
├── skills/                     ← Executor 스킬
│   ├── brief-writer.md
│   ├── column-writer.md
│   ├── text-formatter.md
│   ├── caption-writer.md
│   ├── longform-writer.md
│   ├── thread-writer.md
│   ├── save-to-notion.md
│   ├── validate-slide.md
│   └── html-to-png.md
│
├── pipelines/                  ← 시리즈별 실행 순서
│   ├── pipeline-A.md
│   ├── pipeline-B.md
│   └── pipeline-C.md
│
├── templates/                  ← HTML 슬라이드 템플릿
│   ├── slide-template-column.html    (A시리즈)
│   ├── slide-template-visual.html    (B시리즈)
│   └── slide-template-cinematic.html (C시리즈)
│
├── scripts/                    ← 자동화 스크립트
│   ├── validate_slide.py       QA 검증
│   ├── html_to_png.sh          PNG 변환
│   └── preview_server.py       로컬 프리뷰
│
└── output/                     ← 모든 산출물
    ├── research/               research.md
    ├── columns/                칼럼, 롱폼, 스레드
    ├── slides/                 HTML 슬라이드
    ├── images/                 PNG / MP4
    └── captions/               캡션 텍스트
```

---

## 유틸리티 명령어

```bash
# 슬라이드 QA 검증
python scripts/validate_slide.py output/slides/

# HTML → PNG 변환
bash scripts/html_to_png.sh output/slides/ output/images/

# 로컬 프리뷰 서버 (http://localhost:8080)
python scripts/preview_server.py
```

---

## 핵심 설계 원칙

1. **Human-in-the-Loop** — 핵심 분기점마다 JJ가 직접 결정
2. **역할 분리 + 조합** — 스킬을 레고처럼 조합하는 모듈식 설계
3. **누적 학습** — feedback.md를 통해 JJ 취향에 점점 가까워짐

---

*Built with Claude Code — AI-native content automation pipeline*
*@imjieun.mkt*
