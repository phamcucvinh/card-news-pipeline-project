# 카카오톡 연락처 자동 추가 도구 - Windows 버전

## 설치 및 실행 방법

### 1. Python 설치 (필수)
1. https://python.org 방문
2. Python 3.8 이상 최신 버전 다운로드
3. 설치시 "Add Python to PATH" 체크 ✅

### 2. Chrome과 ChromeDriver 설치
1. Google Chrome 최신 버전 설치
2. Chrome 버전 확인: chrome://version/
3. https://chromedriver.chromium.org/ 에서 맞는 버전 다운로드
4. 이 폴더에 chromedriver.exe로 저장

### 3. 프로그램 실행
1. `실행.bat` 더블클릭
2. 또는 명령프롬프트에서:
   ```
   pip install -r requirements.txt
   python kakao_contact_manager_gui.py
   ```

## 사용 방법
1. 엑셀 파일 준비 (업체명, 핸드폰번호 컬럼)
2. 프로그램에서 파일 선택 → 데이터 로드
3. 설정 조정 (배치 크기: 10개, 지연시간: 3초)
4. 카카오톡 자동화 시작
5. QR코드 스캔 후 진행상황 확인

## 주의사항
- 지연시간을 충분히 설정하세요 (3초 이상)
- 배치 크기를 작게 하세요 (10개 이하)
- 처음엔 100개 정도로 테스트하세요

## 문제 해결
- Python 설치 오류: PATH 환경변수 확인
- 패키지 설치 오류: 관리자 권한으로 실행
- ChromeDriver 오류: Chrome 버전 확인

버전: 1.0.0 (Python 소스 버전)
