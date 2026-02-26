# MoneyPrinter

## 📋 개요
- **목적**: 주제만 입력하면 YouTube Shorts를 자동으로 생성하는 도구
- **기술 스택**: Python, MoviePy, OpenAI, ImageMagick
- **특징**:
  - 매우 간단한 사용법 (주제만 입력)
  - 빠른 비디오 생성
  - TikTok 업로드 지원

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Python 3.10+
- ImageMagick 설치 필요
- OpenAI API Key

### 2. 저장소 클론
```bash
git clone https://github.com/FujiwaraChoki/MoneyPrinter.git
cd MoneyPrinter
```

### 3. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성
# OPENAI_API_KEY 추가
# IMAGEMAGICK_BINARY 경로 설정 (예: "C:\\Program Files\\ImageMagick-7.1.0-Q16\\magick.exe")
```

### 4. ImageMagick 설정
- 설치 시 "Install legacy utilities (e.g. convert)" 체크
- `.env`에서 경로 설정 (Windows는 이중 백슬래시 `\\` 사용)

## 💻 사용 방법 (Step-by-Step)

### 1. 기본 실행
```bash
python main.py
```

### 2. 주제 입력
- 프롬프트에 비디오 주제 입력
- 예: "The history of the internet"

### 3. 자동 생성
- 스크립트 자동 생성
- 배경 영상 자동 선택
- 음성 합성
- 비디오 렌더링

### 4. 결과 확인
- 생성된 비디오는 output 폴더에 저장

## ⚙️ 주요 기능

### 자동 스크립트 생성
- **기능**: OpenAI GPT로 주제 기반 스크립트 작성
- **특징**: 흥미로운 내용 자동 구성

### 배경 영상 자동 선택
- **기능**: 주제에 맞는 영상 자동 검색 및 다운로드
- **특징**: 저작권 걱정 없는 영상 사용

### 음성 합성
- **기능**: 텍스트를 자연스러운 음성으로 변환
- **특징**: 다양한 음성 옵션

### TikTok 세션 ID 지원
- **기능**: TikTok 자동 업로드
- **특징**: 브라우저 쿠키에서 sessionid 추출하여 사용

## 📝 주의사항
- ImageMagick 경로 설정 필수 (`.env` 파일에서)
- Windows 사용자는 경로에 이중 백슬래시(`\\`) 사용
- playsound 설치 오류 시:
  ```bash
  pip install -U wheel
  pip install -U playsound
  ```
- Pull Request는 현재 받지 않음

## 🔗 참고 링크
- **GitHub**: https://github.com/FujiwaraChoki/MoneyPrinter
- **YouTube 튜토리얼**: https://youtu.be/mkZsaDA2JnA
- **로컬 버전 설명서**: ./MoneyPrinter/Local.md
- **X (Twitter)**: @DevBySami
- **원본 README**: ./MoneyPrinter/README.md
