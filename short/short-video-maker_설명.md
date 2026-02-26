# short-video-maker

## 📋 개요
- **목적**: 텍스트 입력만으로 짧은 형태의 비디오를 생성하는 오픈소스 도구
- **기술 스택**: Node.js, Remotion, Whisper.cpp, Kokoro TTS, Pexels API
- **특징**:
  - MCP (Model Context Protocol) 및 REST API 제공
  - GPU 없이도 작동 (경량 리소스)
  - 무료 대안 (타사 API 호출 불필요)
  - Web UI 제공

## 🚀 설치 방법 (Step-by-Step)

### Docker 설치 (권장)

#### 1. Tiny 버전 (최소 리소스)
```bash
docker run -it --rm --name short-video-maker \
  -p 3123:3123 \
  -e LOG_LEVEL=debug \
  -e PEXELS_API_KEY=YOUR_API_KEY \
  gyoridavid/short-video-maker:latest-tiny
```
- **사용**: tiny.en whisper 모델, q4 kokoro 모델
- **리소스**: 2GB RAM, CONCURRENCY=1

#### 2. Normal 버전
```bash
docker run -it --rm --name short-video-maker \
  -p 3123:3123 \
  -e LOG_LEVEL=debug \
  -e PEXELS_API_KEY=YOUR_API_KEY \
  gyoridavid/short-video-maker:latest
```
- **사용**: base.en whisper 모델, fp32 kokoro 모델

#### 3. CUDA 버전 (GPU 가속)
```bash
docker run -it --rm --name short-video-maker \
  -p 3123:3123 \
  -e LOG_LEVEL=debug \
  -e PEXELS_API_KEY=YOUR_API_KEY \
  --gpus=all \
  gyoridavid/short-video-maker:latest-cuda
```
- **사용**: medium.en whisper 모델 (GPU 가속)

### NPM 설치 (대안)

#### 1. 시스템 요구사항
- Ubuntu ≥ 22.04 (libc 2.5) 또는 Mac OS
- FFmpeg 설치
- Node.js 22+

#### 2. 패키지 설치 (Ubuntu)
```bash
sudo apt install -y git wget cmake ffmpeg curl make libsdl2-dev \
  libnss3 libdbus-1-3 libatk1.0-0 libgbm-dev libasound2 \
  libxrandr2 libxkbcommon-dev libxfixes3 libxcomposite1 \
  libxdamage1 libatk-bridge2.0-0 libpango-1.0-0 libcairo2 libcups2
```

## 💻 사용 방법 (Step-by-Step)

### Web UI 사용

#### 1. 브라우저 접속
```
http://localhost:3123
```

#### 2. 비디오 생성
- 텍스트와 검색어 입력
- 음성, 음악, 자막 설정
- "Generate Video" 클릭

### REST API 사용

#### 1. 비디오 생성 요청
```bash
curl --location 'localhost:3123/api/short-video' \
--header 'Content-Type: application/json' \
--data '{
    "scenes": [
      {
        "text": "Hello world!",
        "searchTerms": ["river"]
      }
    ],
    "config": {
      "paddingBack": 1500,
      "music": "chill"
    }
}'
```

**응답**:
```json
{
    "videoId": "cma9sjly700020jo25vwzfnv9"
}
```

#### 2. 상태 확인
```bash
curl --location 'localhost:3123/api/short-video/{videoId}/status'
```

#### 3. 비디오 다운로드
```bash
curl --location 'localhost:3123/api/short-video/{videoId}' > video.mp4
```

### MCP Server 사용

#### MCP 엔드포인트
- `/mcp/sse` - Server-Sent Events
- `/mcp/messages` - Messages

#### 사용 가능한 도구
- `create-short-video`: 짧은 비디오 생성
- `get-video-status`: 비디오 상태 확인

## ⚙️ 주요 기능

### Scene 기반 구성
- **텍스트**: TTS가 읽을 나레이션
- **검색어**: Pexels에서 배경 영상 찾을 키워드
- **Joker 키워드**: 검색 실패 시 자동 대체 ("nature", "globe", "space", "ocean")

### 텍스트 음성 변환
- **Kokoro TTS**: 다양한 영어 음성 (af_heart, am_adam 등)
- **특징**: CPU에서 작동, GPU 불필요

### 자동 자막 생성
- **Whisper.cpp**: 정확한 음성 인식
- **특징**: 자막 위치 선택 (top, center, bottom)

### 배경 영상
- **Pexels API**: 무료 스톡 영상
- **특징**: 자동 검색 및 다운로드

### 배경 음악
- **기능**: 분위기별 음악 선택
- **옵션**: sad, happy, chill, dark, hopeful 등

### 방향 지원
- **Portrait**: 세로 (9:16)
- **Landscape**: 가로 (16:9)

## 📝 주의사항
- 영어 음성만 지원 (Kokoro-js 제한)
- 배경 영상은 Pexels만 지원
- 이미지나 비디오로부터 생성하지 않음 (텍스트 기반만)
- 최소 리소스: 3GB RAM, 2 vCPU, 5GB 디스크
- Docker에서 충분한 메모리 할당 필요
- Windows는 지원하지 않음 (whisper.cpp 설치 문제)

## 🔗 참고 링크
- **GitHub**: https://github.com/gyoridavid/short-video-maker
- **YouTube 채널**: [AI Agents A-Z](https://www.youtube.com/channel/UCloXqLhp_KGhHBe1kwaL2Tg)
- **튜토리얼**: https://www.youtube.com/watch?v=jzsQpn-AciM
- **n8n 워크플로우**: https://github.com/gyoridavid/ai_agents_az/tree/main/episode_7
- **Skool 커뮤니티**: https://www.skool.com/ai-agents-az/about
- **원본 README**: ./short-video-maker/README.md
