#!/usr/bin/env python3
"""
카카오톡 다중 문자 발송기
주의: 실제 카카오톡 API 키와 승인이 필요합니다.
"""

import requests
import json
import time
import csv
from datetime import datetime

class KakaoTalkMultiSender:
    def __init__(self, api_key=None):
        """
        카카오톡 발송기 초기화
        api_key: 카카오 개발자센터에서 발급받은 API 키
        """
        self.api_key = api_key
        self.base_url = "https://kapi.kakao.com"
        
    def send_message(self, phone_numbers, message, template_type="text"):
        """
        다중 문자 발송
        phone_numbers: 발송할 전화번호 리스트
        message: 발송할 메시지
        template_type: 메시지 타입 (text, image, button 등)
        """
        
        if not self.api_key:
            print("오류: API 키가 설정되지 않았습니다.")
            return False
            
        results = []
        
        for phone_number in phone_numbers:
            try:
                # 실제 카카오톡 비즈니스 API 사용시 필요한 요청 구조
                payload = {
                    "receiver": phone_number,
                    "message": message,
                    "template_type": template_type
                }
                
                # 실제 API 호출 (여기서는 시뮬레이션)
                print(f"발송 시뮬레이션: {phone_number} -> {message[:30]}...")
                
                results.append({
                    "phone_number": phone_number,
                    "status": "success",
                    "sent_at": datetime.now().isoformat()
                })
                
                time.sleep(1)  # 발송 간격 조절
                
            except Exception as e:
                results.append({
                    "phone_number": phone_number,
                    "status": "error",
                    "error": str(e),
                    "sent_at": datetime.now().isoformat()
                })
        
        return results
    
    def load_contacts_from_csv(self, csv_file):
        """CSV 파일에서 연락처 로드"""
        phone_numbers = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and len(row) > 0:
                        phone_numbers.append(row[0])  # 첫 번째 컬럼을 전화번호로 가정
        except Exception as e:
            print(f"CSV 파일 로드 오류: {e}")
            
        return phone_numbers
    
    def save_results(self, results, filename="send_results.json"):
        """발송 결과 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"발송 결과가 {filename}에 저장되었습니다.")

def main():
    """메인 함수 - 사용 예시"""
    
    # API 키 설정 (실제 사용시 카카오 개발자센터에서 발급받으세요)
    api_key = "YOUR_KAKAO_API_KEY"
    
    sender = KakaoTalkMultiSender(api_key)
    
    # 발송할 전화번호 리스트
    phone_numbers = [
        "010-1234-5678",
        "010-2345-6789",
        "010-3456-7890"
    ]
    
    # 또는 CSV에서 로드
    # phone_numbers = sender.load_contacts_from_csv("contacts.csv")
    
    # 발송할 메시지
    message = """
    안녕하세요!
    
    카카오톡 다중 발송 테스트 메시지입니다.
    
    감사합니다.
    """
    
    # 메시지 발송
    print("카카오톡 다중 발송을 시작합니다...")
    results = sender.send_message(phone_numbers, message)
    
    # 결과 저장
    sender.save_results(results)
    
    # 발송 결과 요약
    success_count = len([r for r in results if r["status"] == "success"])
    error_count = len([r for r in results if r["status"] == "error"])
    
    print(f"\n=== 발송 결과 ===")
    print(f"성공: {success_count}건")
    print(f"실패: {error_count}건")
    print(f"총: {len(results)}건")

if __name__ == "__main__":
    main()
