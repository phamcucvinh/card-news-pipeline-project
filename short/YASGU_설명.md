# YASGU (Youtube Automatised Shorts Generator And Uploader)

## 📋 개요
- **목적**: 스크립트부터 이미지까지 완전 자동으로 YouTube Shorts 생성 및 업로드
- **기술 스택**: Python, GPT-4Free, CoquiTTS, DALL-E/Prodia, Selenium, Firefox
- **특징**:
  - 주제와 언어만 지정하면 나머지 자동 처리
  - 다양한 LLM 및 이미지 생성 모델 지원
  - 여러 생성기 동시 실행 가능
  - 5분 이내 비디오 생성

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Git
- Python 3.9.X (Python 3.10은 지원하지 않음)
- ImageMagick ("Install legacy utilities" 체크 필수)
- Microsoft Visual C++ Build Tools (CoquiTTS용)
- Firefox 브라우저

### 2. 저장소 클론 및 설치
```bash
git clone https://github.com/hankerspace/YASGU.git
cd YASGU

# 설정 파일 복사
cp config/config.example.json config/config.json

# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (Windows)
.\.venv\Scripts\activate

# 가상 환경 활성화 (Unix/Mac)
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 폰트 및 음악 다운로드
- [Google Fonts](https://fonts.google.com/)에서 폰트 다운로드 → `assets/fonts/` 폴더에 저장
- [YouTube Audio Library](https://www.youtube.com/audiolibrary/music)에서 무료 음악 다운로드 → `assets/music/` 폴더에 저장

### 4. config.json 설정
```json
{
  "verbose": true,
  "headless": false,
  "threads": 4,
  "assembly_ai_api_key": "YOUR_API_KEY",
  "imagemagick_path": "C:\\Program Files\\ImageMagick\\magick.exe",
  "generators": [
    {
      "id": "generator_1",
      "language": "en",
      "subject": "Random facts about trees",
      "llm": "claude_3_sonnet",
      "image_prompt_llm": "mixtral_8x7b",
      "image_model": "lexica",
      "images_count": 5,
      "is_for_kids": false,
      "font": "Arial.ttf",
      "firefox_profile": "C:\\Users\\YourName\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xxxxx.default"
    }
  ]
}
```

### 5. Firefox 프로필 설정
- Firefox에서 새 프로필 생성
- YouTube 계널에 로그인
- 프로필 경로를 `config.json`의 `firefox_profile`에 추가

## 💻 사용 방법 (Step-by-Step)

### 1. 기본 실행
```bash
python main.py
```

### 2. 자동 처리 과정
- 설정에 지정된 주제로 스크립트 생성 (LLM 사용)
- CoquiTTS로 음성 생성
- DALL-E/Prodia로 일러스트 이미지 생성
- 음악, 자막, 이미지를 결합하여 비디오 생성
- Selenium과 Firefox로 YouTube에 자동 업로드

### 3. 결과 확인
- YouTube 채널에서 업로드된 Shorts 확인
- 생성된 비디오는 로컬에도 저장됨

## ⚙️ 주요 기능

### 다양한 LLM 모델 지원
- **GPT-3.5/4**: OpenAI 모델
- **Llama 2**: 7b, 13b, 70b 버전
- **Mixtral**: 8x7B Instruct
- **Claude**: v2, 3-opus, 3-sonnet
- **Gemini**: Google 모델

### 이미지 생성 모델
- **DALL-E**: v1, v2, v2-beta, v3
- **Prodia, Lexica**: 무료 대안
- **Simurg, Animefy, Raava, Shonin**: 특화 모델

### 맞춤 설정
- 자막 폰트, 크기, 색상, 테두리 설정
- 배경 음악 볼륨 조절
- 이미지 개수 설정
- 어린이용 콘텐츠 플래그

### 다중 생성기
- **기능**: 여러 주제/언어로 동시에 비디오 생성
- **특징**: 각 생성기는 독립적으로 작동

## 📝 주의사항
- Python 3.10 지원하지 않음 (의존성 문제)
- Firefox 필수 (Selenium 사용)
- ImageMagick 설치 시 "legacy utilities" 체크 필수
- API 키 필요: AssemblyAI (자막용)
- YouTube 로그인 상태 유지 필요 (Firefox 프로필)
- 생성된 콘텐츠의 저작권과 윤리적 사용은 사용자 책임

## 🔗 참고 링크
- **GitHub**: https://github.com/hankerspace/YASGU
- **CoquiTTS**: https://github.com/coqui-ai/TTS
- **gpt4free**: https://github.com/xtekky/gpt4free
- **예시 비디오**: ./YASGU/assets/docs/example.mp4
- **원본 README**: ./YASGU/README.md
