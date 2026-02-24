# save-to-docx — DOCX 저장 스킬

## 역할
최종 편집 완료된 Markdown 파일을 DOCX 형식으로 변환하여 저장한다.
기존 `synopsis-to-scenario-master/scripts/md_to_docx.py`를 재사용한다.

## 입력
- `output/final/[제목]-final.md` (통합 원고)
- 출력 파일명 지정

## 출력
`output/final/[제목]-final-[YYYYMMDD].docx`

---

## 실행 절차

### 1단계: 통합 원고 준비
모든 챕터 파일을 하나의 Markdown 파일로 통합:

```bash
# output/final/ 에 챕터들을 순서대로 합친다
cat output/drafts/chapter-*.md > output/final/[제목]-final.md
```

### 2단계: DOCX 변환 실행

```bash
python ../synopsis-to-scenario-master/scripts/md_to_docx.py \
  output/final/[제목]-final.md \
  output/final/[제목]-final-$(date +%Y%m%d).docx
```

### 3단계: 출력 확인
- 파일 생성 확인
- 챕터 제목 서식 확인
- 페이지 번호 확인 (md_to_docx 지원 시)

---

## md_to_docx.py 재사용 경로

```
fiction-writing-pipeline/
└── output/final/
    └── [제목]-final.md  ←── 입력

../synopsis-to-scenario-master/scripts/md_to_docx.py  ←── 스크립트

fiction-writing-pipeline/
└── output/final/
    └── [제목]-final-[YYYYMMDD].docx  ←── 출력
```

의존 패키지: `python-docx`
```bash
pip install python-docx
```

---

## DOCX 서식 가이드라인

| 요소 | Markdown | DOCX 변환 결과 |
|------|----------|--------------|
| 챕터 제목 | `# Chapter N` | Heading 1 |
| 씬 제목 | `## 씬 제목` | Heading 2 |
| 씬 구분 | `---` | 구분선 |
| 본문 | 일반 단락 | Normal 스타일 |
| 인용구 | `> 텍스트` | 들여쓰기 단락 |

---

## 오류 처리

- `md_to_docx.py` 경로 오류 → 절대 경로로 재시도
- `python-docx` 미설치 → `pip install python-docx` 안내
- 인코딩 오류 → `--encoding utf-8` 옵션 추가
