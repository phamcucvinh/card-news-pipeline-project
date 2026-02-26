# Auto-YouTube-Shorts-Maker

## 📋 개요
- **목적**: 스크립트 실행만으로 YouTube Shorts를 자동 생성하는 도구
- **기술 스택**: Python, OpenAI, gTTS, MoviePY
- **특징**:
  - 매우 간단하고 직관적인 사용법
  - AI 콘텐츠 생성 또는 수동 입력 선택 가능
  - 게임플레이 영상 위에 음성 오버레이
  - 완전 무료

## 🚀 설치 방법 (Step-by-Step)

### 1. 사전 요구사항
- Python 3.x
- OpenAI API Key (AI 콘텐츠 생성 사용 시, $18 무료 크레딧 제공)

### 2. 저장소 다운로드
```bash
git clone https://github.com/Binary-Bytes/Auto-YouTube-Shorts-Maker.git
cd Auto-YouTube-Shorts-Maker
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 설정
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집 (AI 사용 시)
# OPENAI_API=<your_api_key>
```

### 5. 게임플레이 영상 다운로드
- [Google Drive](https://drive.google.com/drive/folders/1qToyKgKDLOPgoMj_EMhA6qusV4xCr4Sb?usp=sharing)에서 2개의 게임플레이 영상 다운로드
- `gameplay` 폴더 생성 후 영상 저장

## 💻 사용 방법 (Step-by-Step)

### 1. 스크립트 실행
```bash
python shorts.py
```

### 2. 비디오 이름 입력
- 프롬프트에 비디오 제목 입력

### 3. 콘텐츠 생성 선택
- **AI 생성**: OpenAI가 자동으로 콘텐츠 생성 (API Key 필요)
- **수동 입력**: 직접 스크립트 작성

### 4. 콘텐츠 편집 (선택사항)
- AI 생성 콘텐츠를 수정 가능

### 5. 자동 생성
- 텍스트 → 음성 변환
- 게임플레이 영상 선택 및 편집
- 음성과 영상 결합
- 9:16 비율로 리사이징

### 6. 결과 확인
- `generated/` 폴더에서 완성된 비디오 확인

## ⚙️ 주요 기능

### AI 콘텐츠 생성
- **기능**: OpenAI GPT로 비디오 콘텐츠 자동 작성
- **특징**: 흥미로운 내용 자동 구성 후 수동 편집 가능

### 텍스트 음성 변환
- **기능**: gTTS로 자연스러운 음성 생성
- **특징**: `speech.mp3` 파일로 저장

### 자동 비디오 편집
- **기능**: 게임플레이 영상의 무작위 부분 선택
- **특징**: 음성 길이에 맞춰 자동 트리밍

### 9:16 비율 변환
- **기능**: YouTube Shorts에 최적화된 세로 비율
- **특징**: 자동 리사이징

## 📝 주의사항
- 현재는 기본 기능만 제공 (자막, 이미지 등 미지원)
- 게임플레이 영상은 반드시 다운로드 필요 (GitHub 용량 제한)
- OpenAI API Key는 선택사항 (수동 입력 가능)
- 프로젝트 개발이 느림 (학교, 시험 등으로 인해)
- 향후 계획: 자막, 이미지, Reddit 비디오 메이커 추가 예정

## 🔗 참고 링크
- **GitHub**: https://github.com/Binary-Bytes/Auto-YouTube-Shorts-Maker
- **데모 비디오**: ./Auto-YouTube-Shorts-Maker/demo/Demo.mp4
- **게임플레이 영상**: https://drive.google.com/drive/folders/1qToyKgKDLOPgoMj_EMhA6qusV4xCr4Sb?usp=sharing
- **Discord**: BedrockGranny#8331 또는 bedrockgranny
- **원본 README**: ./Auto-YouTube-Shorts-Maker/README.md
