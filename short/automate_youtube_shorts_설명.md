# automate_youtube_shorts

## 📋 개요
- **목적**: Instagram 콘텐츠를 자동으로 스크랩하여 YouTube Shorts로 변환 및 업로드
- **기술 스택**: Python3, Selenium, Chrome Beta, Instagram API
- **특징**:
  - 완전 자동화된 YouTube 채널 운영
  - 24시간마다 자동 실행
  - Instagram → YouTube Shorts 변환
  - 간단한 설정

## 🚀 설치 방법 (Step-by-Step)

### 1. 저장소 클론
```bash
git clone https://github.com/PatrickAcheson/automate_youtube_shorts.git
cd automate_youtube_shorts
```

### 2. Python3 및 pip 설치
- Python3와 pip가 설치되어 있지 않다면 설치

### 3. 의존성 설치
```bash
pip3 install -r requirements.txt
# 또는
python3 -m pip install -r requirements.txt
```

### 4. Instagram 계정 설정
```bash
# accounts.txt에 팔로우할 Instagram 계정 추가
echo "account_name1" >> accounts.txt
echo "account_name2" >> accounts.txt
```

### 5. .env 파일 설정
```bash
# .env 파일 생성 및 Instagram 로그인 정보 추가
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### 6. Instagram 크레덴셜 설정
- `download_insta.py` 파일 열기
- `# change here` 주석 부분에 Instagram 크레덴셜 입력

### 7. Chrome Beta 설치 및 설정
- Chrome Beta 브라우저 설치
- `upload_video.py`에서 Chrome Beta 경로 설정

### 8. YouTube 채널 로그인
- Chrome Beta 브라우저 열기
- YouTube 채널에 로그인
- 로그인 후 브라우저 닫기 (필수!)

## 💻 사용 방법 (Step-by-Step)

### 1. 스크립트 실행
```bash
python3 main.py
```

### 2. 자동 프로세스
- 24시간마다 자동으로 실행
- Instagram 계정에서 비디오 스크랩
- YouTube Shorts 형식으로 변환
- YouTube 채널에 자동 업로드

### 3. 커스터마이징
- `main.py`에서 변수 수정 가능
- 최대 클립 길이 설정
- 업로드 주기 설정

## ⚙️ 주요 기능

### Instagram 스크래핑
- **기능**: accounts.txt에 있는 계정들로부터 비디오 다운로드
- **특징**: 최신 콘텐츠 자동 수집

### 비디오 변환
- **기능**: Instagram 비디오를 YouTube Shorts 형식으로 변환
- **특징**: 세로 비율, 길이 조정

### 자동 업로드
- **기능**: 변환된 비디오를 YouTube에 자동 업로드
- **특징**: Selenium을 사용한 브라우저 자동화

### 스케줄링
- **기능**: 24시간마다 자동 실행
- **특징**: 완전 자동화된 채널 운영

## 📝 주의사항

### 알려진 이슈
1. **Instagram 로그아웃 필수**
   - 스크립트 실행 전 Instagram에서 로그아웃해야 함
   - 로그인 상태에서 실행 시 오류 발생

2. **Chrome Beta 브라우저 닫기**
   - 스크립트 실행 전 Chrome Beta를 닫아야 함
   - 열려있으면 오류 발생

3. **2024년 작동 확인**
   - 2024년에 다시 작동하도록 업데이트됨

### 기타 주의사항
- Instagram 계정 보안에 주의
- YouTube 커뮤니티 가이드라인 준수
- 저작권 문제 주의 (원본 콘텐츠 소유자 확인)
- 스크랩할 계정의 콘텐츠 사용 권한 확인

## 🔗 참고 링크
- **GitHub**: https://github.com/PatrickAcheson/automate_youtube_shorts
- **작동 예시 이미지**: ./automate_youtube_shorts/README.md (이미지 참조)
- **원본 README**: ./automate_youtube_shorts/README.md

## 📊 프로젝트 출력 예시
![image](https://github.com/user-attachments/assets/2fd8aecc-6cb5-40a1-bac0-46d957d18b74)

완전 자동화된 Instagram → YouTube Shorts 채널을 즐기세요!
