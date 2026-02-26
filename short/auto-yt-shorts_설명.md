# auto-yt-shorts

## 📋 개요
- **목적**: AI를 활용한 YouTube Shorts 및 TikTok 자동 생성 및 업로드
- **기술 스택**: Python, FastAPI, OpenAI, AssemblyAI, Pexels, Docker
- **특징**:
  - 주제 제안부터 업로드까지 완전 자동화
  - YouTube OAuth 2.0 인증 지원
  - Docker 및 스케줄링 지원
  - 병렬 실행으로 빠른 처리

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Python 3.12
- Pexels API Key (무료)
- OpenAI API Key
- AssemblyAI API Key
- YouTube OAuth 2.0 Credentials

### 2. 저장소 클론
```bash
git clone https://github.com/marvinvr/auto-yt-shorts
cd auto-yt-shorts
```

### 3. 환경 설정
```bash
# 환경 파일 복사
cp example.env .env

# .env 파일 편집
# OPENAI_API_KEY, PEXELS_API_KEY, ASSEMBLY_AI_API_KEY 등 추가
```

### 4. 배경 음악 및 보조 영상 준비
- `music/` 폴더에 배경 음악 (.mp3) 추가
- `secondary_video/` 폴더에 보조 영상 (.mp4) 추가

### 5. YouTube OAuth 설정
```bash
# YouTube Data API에서 OAuth 2.0 credentials 생성
# client_secrets.json을 ./credentials 폴더에 저장

# 초기 인증 (한 번만 실행)
python upload_video.py

# 토큰 갱신 (필요 시)
python update_tokens.py
```

### 6. 의존성 설치
```bash
pip install -r requirements.txt
```

## 💻 사용 방법 (Step-by-Step)

### 로컬 실행

#### 1. 한 번만 실행
```bash
RUN_ONCE=true python main.py
```

#### 2. 스케줄 실행 (cron)
```bash
# 6시간마다 실행
CRON_SCHEDULE="0 */6 * * *" python main.py
```

#### 3. .env 파일에 설정 추가 (대안)
```bash
# 한 번만 실행
RUN_ONCE=true

# 또는 스케줄 실행
CRON_SCHEDULE=0 */6 * * *
```

### Docker 실행

```bash
docker compose up
```

- REST API 엔드포인트: `http://localhost:8000`
- POST `/generate_videos`로 비디오 생성 요청

## ⚙️ 주요 기능

### 완전 자동화 파이프라인
- **기능**: 주제 선택 → 스크립트 생성 → 음성 합성 → 영상 편집 → 업로드
- **특징**: 사용자 개입 최소화

### AI 콘텐츠 생성
- **llm.py**: OpenAI로 흥미로운 주제, 제목, 설명 생성
- **특징**: 논란의 여지가 있는 주제 선택으로 참여도 극대화

### 음성 및 자막
- **audio.py**: OpenAI로 음성 생성
- **video.py**: AssemblyAI로 자막 생성 및 SRT 균등화

### 배경 영상
- **stock_videos.py**: Pexels API로 관련 영상 자동 검색
- **특징**: 저작권 걱정 없는 스톡 영상

### 자동 업로드
- **yt.py**: YouTube OAuth 2.0 인증으로 자동 업로드
- **tiktok.py**: TikTok 업로드 지원
- **특징**: 메타데이터 자동 생성

### 병렬 처리
- **기능**: 여러 비디오 동시 생성 가능
- **특징**: 처리 속도 대폭 향상

## 📝 주의사항
- 이 프로젝트는 교육 목적으로 만들어짐
- 상업적 사용이나 저작권 침해 의도 없음
- 실제로 AI 생성 비디오를 운영하는 데 사용되지 않음
- YouTube Channel 예시: [QuickQuirks](https://www.youtube.com/channel/UC4igt1OgsZGBs7PRqpxI9eQ)

## 🔗 참고 링크
- **GitHub**: https://github.com/marvinvr/auto-yt-shorts
- **MoneyPrinter 프로젝트**: https://github.com/FujiwaraChoki/MoneyPrinter (영감을 받음)
- **YouTube API 문서**: https://developers.google.com/youtube/v3/quickstart/python
- **원본 README**: ./auto-yt-shorts/README.md
