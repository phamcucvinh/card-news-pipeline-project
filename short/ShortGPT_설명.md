# ShortGPT

## 📋 개요
- **목적**: AI를 활용한 YouTube Shorts 및 TikTok 비디오 자동 생성 프레임워크
- **기술 스택**: Python, OpenAI GPT, MoviePy, ElevenLabs/EdgeTTS, Pexels API
- **특징**:
  - 스크립트 생성부터 음성 합성, 영상 편집까지 완전 자동화
  - 30개 이상 언어 지원
  - 자동 자막 생성
  - 웹 인터페이스 제공 (Gradio)

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Docker 설치 필요
- OpenAI API Key
- ElevenLabs API Key (옵션)

### 2. 저장소 클론
```bash
git clone https://github.com/RayVentura/ShortGPT.git
cd ShortGPT
```

### 3. 환경 설정
```bash
# .env 파일 생성 및 API 키 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 등 추가
```

### 4. Docker 실행
```bash
docker build -t short_gpt_docker:latest .
docker run -p 31415:31415 --env-file .env short_gpt_docker:latest
```

## 💻 사용 방법 (Step-by-Step)

### 1. 웹 인터페이스 접속
- 브라우저에서 `http://localhost:31415` 접속

### 2. 비디오 생성
- Gradio UI에서 주제, 언어, 스타일 선택
- 자동으로 스크립트, 음성, 영상 생성
- YouTube 메타데이터 자동 생성

### 3. Google Colab 사용 (추천)
```bash
https://colab.research.google.com/drive/1_2UKdpF6lqxCqWaAcZb3rwMVQqtbisdE?usp=sharing
```
- 설치 없이 바로 사용 가능

## ⚙️ 주요 기능

### ContentShortEngine
- **기능**: YouTube Shorts 생성 전용 엔진
- **특징**: 스크립트 → 렌더링 → YouTube 메타데이터 생성

### ContentVideoEngine
- **기능**: 긴 형태의 비디오 생성
- **특징**: 자동 음성 생성, 배경 영상 소싱, 자막 타이밍

### ContentTranslationEngine
- **기능**: 비디오 더빙 및 번역
- **특징**: 전체 비디오를 다른 언어로 번역 및 음성 생성

### 자동화 기능
- 🎞️ Pexels API를 통한 배경 영상 자동 소싱
- 🗣️ ElevenLabs 또는 EdgeTTS로 음성 합성
- 🔗 자막 자동 생성
- 💾 TinyDB로 상태 저장

## 📝 주의사항
- Docker 필수 (로컬 실행 시)
- OpenAI API 크레딧 필요 ($18 무료 크레딧 제공)
- ImageMagick 설치 시 "Install legacy utilities" 체크 필요
- Python 3.10은 지원하지 않음 (의존성 문제)

## 🔗 참고 링크
- **GitHub**: https://github.com/RayVentura/ShortGPT
- **문서**: https://docs.shortgpt.ai/
- **Discord**: https://discord.gg/uERx39ru3R
- **YouTube 데모**: https://youtu.be/hpoSHq-ER8U
- **원본 README**: ./ShortGPT/README.md
