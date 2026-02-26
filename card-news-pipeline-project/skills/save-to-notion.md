# save-to-notion — 노션 저장 스킬

## 역할
완성된 카드뉴스 산출물을 노션 데이터베이스에 기록한다. (선택 사항)

## 입력
- 시리즈 유형
- 주제/제목
- 산출물 파일 경로들
- 노션 API 토큰 (환경변수: NOTION_TOKEN)
- 노션 데이터베이스 ID (환경변수: NOTION_DB_ID)

## 노션 페이지 구조

```
제목: [시리즈] [주제] — YYYY.MM.DD

Properties:
- 시리즈: A / B / C (선택)
- 날짜: YYYY-MM-DD
- 상태: 완료
- 해시태그: [자동 추출]

본문:
- 리서치 파일 링크
- 칼럼 내용 (복사)
- 슬라이드 미리보기 (링크)
- 캡션 텍스트
```

## 설정 방법

1. 노션 인테그레이션 생성: https://www.notion.so/my-integrations
2. 환경변수 설정:
   ```bash
   export NOTION_TOKEN="secret_..."
   export NOTION_DB_ID="[데이터베이스 ID]"
   ```
3. 데이터베이스에 인테그레이션 연결

## 노션 미사용 시

노션 저장 없이 로컬 파일로만 관리:
- 모든 산출물은 `output/` 폴더에 자동 저장됨
- `feedback.md`의 히스토리 테이블에 수동 기록
