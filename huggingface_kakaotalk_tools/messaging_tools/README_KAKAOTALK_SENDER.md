# 카카오톡 다중 문자 발송기

## 주의사항
⚠️ **이 도구는 교육/연구 목적으로 제공됩니다.**
⚠️ **실제 사용시 카카오 개발자센터에서 API 승인을 받아야 합니다.**
⚠️ **스팸 발송은 법적 문제가 될 수 있습니다.**

## 설치 및 설정

### 1. 필수 라이브러리 설치
```bash
pip install requests
```

### 2. 카카오 API 키 발급
1. [카카오 개발자센터](https://developers.kakao.com/) 접속
2. 애플리케이션 등록
3. 카카오톡 채널/비즈메시지 API 신청
4. API 키 발급

### 3. 사용법
```python
from kakaotalk_multi_sender import KakaoTalkMultiSender

# API 키 설정
sender = KakaoTalkMultiSender("YOUR_API_KEY")

# 전화번호 리스트
phones = ["010-1234-5678", "010-2345-6789"]

# 메시지 발송
results = sender.send_message(phones, "안녕하세요!")
```

## 주요 기능
- 다중 전화번호 발송
- CSV 파일에서 연락처 로드
- 발송 결과 저장 및 관리
- 발송 간격 조절
- 에러 처리 및 로깅

## 법적 고지
- 개인정보보호법 준수 필수
- 수신자 동의 없는 발송 금지
- 광고성 정보 전송시 법적 요건 준수
- 카카오톡 이용약관 및 API 정책 준수

## 연락처 CSV 파일 형식
```csv
전화번호,이름,그룹
010-1234-5678,홍길동,친구
010-2345-6789,김철수,직장
```

## 문의
기술적 문제나 개선사항은 GitHub Issues를 통해 제보해주세요.
