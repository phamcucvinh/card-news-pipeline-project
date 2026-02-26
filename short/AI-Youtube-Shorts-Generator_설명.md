# AI-Youtube-Shorts-Generator

## 📋 개요
- **목적**: 긴 영상에서 하이라이트를 자동 추출하여 YouTube Shorts 생성
- **기술 스택**: Python, GPT-4o-mini, Whisper (CUDA), FFmpeg, ImageMagick
- **특징**:
  - GPU 가속 음성 인식 (Whisper CUDA)
  - AI 기반 하이라이트 자동 선택
  - 얼굴 인식 자동 크롭
  - 인터랙티브 승인 시스템

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Python 3.10+
- NVIDIA GPU (CUDA 지원, 선택사항)
- FFmpeg with development headers
- ImageMagick
- OpenAI API Key

### 2. 시스템 패키지 설치 (Ubuntu)
```bash
sudo apt install -y ffmpeg libavdevice-dev libavfilter-dev libopus-dev \
  libvpx-dev pkg-config libsrtp2-dev imagemagick
```

### 3. ImageMagick 보안 정책 수정
```bash
sudo sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml
```

### 4. 저장소 설치
```bash
git clone https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator.git
cd AI-Youtube-Shorts-Generator

# 가상 환경 생성
python3.10 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 5. 환경 변수 설정
```bash
# .env 파일 생성
echo "OPENAI_API=your_openai_api_key_here" > .env
```

## 💻 사용 방법 (Step-by-Step)

### 1. YouTube URL로 실행 (인터랙티브)
```bash
./run.sh
# YouTube URL 입력
# 해상도 선택 (5초 대기 시 최고화질 자동 선택)
```

### 2. 명령줄에서 실행
```bash
# YouTube URL 지정
./run.sh "https://youtu.be/VIDEO_ID"

# 로컬 비디오 파일
./run.sh "/path/to/your/video.mp4"
```

### 3. 배치 처리 (urls.txt 사용)
```bash
# urls.txt 파일 생성 (한 줄에 하나의 URL)
# 자동 승인 모드로 처리
xargs -a urls.txt -I{} ./run.sh --auto-approve {}
```

### 4. AI 하이라이트 승인
- AI가 하이라이트 선택 후 15초 대기
- **Enter/y**: 승인
- **r**: 다시 생성
- **n**: 취소

## ⚙️ 주요 기능

### GPU 가속 음성 인식
- **기능**: CUDA 지원 Whisper로 빠른 전사
- **성능**: 5분 영상을 약 30초에 처리

### AI 하이라이트 선택
- **기능**: GPT-4o-mini가 가장 흥미로운 2분 구간 자동 선택
- **특징**: 흥미롭고, 유용하고, 놀랍거나 논란의 여지가 있는 내용 선택

### 스마트 크롭
- **얼굴 비디오**: 얼굴 중심의 정적 크롭 (떨림 없음)
- **화면 녹화**: 절반 너비 디스플레이, 부드러운 모션 트래킹 (1초당 최대 1회 이동)

### 자동 자막
- **기능**: Franklin Gothic 폰트로 스타일화된 자막
- **특징**: 비디오에 자막 삽입, 파란색 텍스트/검은색 테두리

### 반응형 해상도
- **기능**: 소스 비디오 높이에 맞춤 (720p → 404x720, 1080p → 607x1080)
- **특징**: 9:16 세로 비율 자동 생성

## 📝 주의사항
- GPU 없이도 작동하지만 속도가 느림
- ImageMagick 정책 수정 필수 (자막 생성용)
- 얼굴 감지는 처음 30 프레임에서 작동
- 저해상도 비디오는 얼굴 감지가 불안정할 수 있음
- 동시 실행 시 각 인스턴스는 고유한 세션 ID 사용

## 🔗 참고 링크
- **GitHub**: https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator
- **관련 프로젝트**:
  - AI Influencer Generator: https://github.com/SamurAIGPT/AI-Influencer-Generator
  - Text to Video AI: https://github.com/SamurAIGPT/Text-To-Video-AI
  - Faceless Video Generator: https://github.com/SamurAIGPT/Faceless-Video-Generator
- **원본 README**: ./AI-Youtube-Shorts-Generator/README.md
