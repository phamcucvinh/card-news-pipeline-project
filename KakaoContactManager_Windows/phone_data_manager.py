#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
from typing import List, Dict, Tuple
import logging

class PhoneDataManager:
    """전화번호 데이터 관리 클래스"""
    
    def __init__(self):
        self.df = None
        self.valid_phones = []
        self.setup_logging()
    
    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('phone_processor.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_excel_data(self, file_path: str) -> bool:
        """엑셀 파일에서 전화번호 데이터 로드"""
        try:
            self.logger.info(f"엑셀 파일 로딩 중: {file_path}")
            self.df = pd.read_excel(file_path)
            self.logger.info(f"총 {len(self.df)}개의 데이터 로드 완료")
            return True
        except Exception as e:
            self.logger.error(f"엑셀 파일 로드 실패: {e}")
            return False
    
    def validate_phone_number(self, phone: str) -> bool:
        """전화번호 유효성 검증"""
        if pd.isna(phone):
            return False
        
        phone_str = str(phone).strip()
        # 한국 휴대폰 번호 패턴 (010-XXXX-XXXX)
        pattern = r'^010-\d{4}-\d{4}$'
        return bool(re.match(pattern, phone_str))
    
    def clean_phone_number(self, phone: str) -> str:
        """전화번호 정리 (하이픈 제거 등)"""
        if pd.isna(phone):
            return ""
        
        phone_str = str(phone).strip()
        # 하이픈 제거하고 숫자만 추출
        phone_clean = re.sub(r'[^0-9]', '', phone_str)
        
        # 010으로 시작하는 11자리 번호만 허용
        if phone_clean.startswith('010') and len(phone_clean) == 11:
            return phone_clean
        return ""
    
    def process_phone_data(self, limit: int = None) -> List[Dict]:
        """전화번호 데이터 처리"""
        if self.df is None:
            self.logger.error("데이터가 로드되지 않았습니다.")
            return []
        
        processed_data = []
        df_to_process = self.df.head(limit) if limit else self.df
        
        self.logger.info(f"{len(df_to_process)}개의 데이터 처리 중...")
        
        for idx, row in df_to_process.iterrows():
            phone = row['핸드폰번호']
            
            if self.validate_phone_number(phone):
                clean_phone = self.clean_phone_number(phone)
                if clean_phone:
                    processed_data.append({
                        'index': idx,
                        'company': row['업체명'] if '업체명' in row and not pd.isna(row['업체명']) else f"연락처{idx+1}",
                        'phone': clean_phone,
                        'formatted_phone': phone,
                        'region': row['시도'] if '시도' in row and not pd.isna(row['시도']) else "미분류"
                    })
        
        self.valid_phones = processed_data
        self.logger.info(f"유효한 전화번호 {len(processed_data)}개 처리 완료")
        return processed_data
    
    def get_phones_by_region(self, region: str = None) -> List[Dict]:
        """지역별 전화번호 필터링"""
        if not self.valid_phones:
            return []
        
        if region:
            return [p for p in self.valid_phones if region in p['region']]
        return self.valid_phones
    
    def export_to_csv(self, output_path: str = "processed_phones.csv") -> bool:
        """처리된 데이터를 CSV로 내보내기"""
        try:
            if not self.valid_phones:
                self.logger.warning("내보낼 데이터가 없습니다.")
                return False
            
            df_export = pd.DataFrame(self.valid_phones)
            df_export.to_csv(output_path, index=False, encoding='utf-8-sig')
            self.logger.info(f"데이터를 {output_path}에 저장했습니다.")
            return True
        except Exception as e:
            self.logger.error(f"CSV 내보내기 실패: {e}")
            return False
    
    def get_batch_phones(self, batch_size: int = 100, batch_num: int = 0) -> List[Dict]:
        """배치 단위로 전화번호 가져오기"""
        if not self.valid_phones:
            return []
        
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        return self.valid_phones[start_idx:end_idx]
    
    def get_total_batches(self, batch_size: int = 100) -> int:
        """전체 배치 수 계산"""
        if not self.valid_phones:
            return 0
        return (len(self.valid_phones) + batch_size - 1) // batch_size

# 테스트 코드
if __name__ == "__main__":
    manager = PhoneDataManager()
    
    # 엑셀 파일 로드 (테스트용으로 처음 1000개만)
    if manager.load_excel_data("/mnt/c/Users/SAMSUNG/Desktop/저작권/호참전화번.xlsx"):
        # 처음 1000개만 처리 (테스트용)
        phones = manager.process_phone_data(limit=1000)
        
        print(f"처리된 전화번호: {len(phones)}개")
        if phones:
            print("첫 5개 샘플:")
            for i, phone in enumerate(phones[:5]):
                print(f"{i+1}. {phone['company']}: {phone['formatted_phone']} ({phone['region']})")
        
        # CSV 내보내기
        manager.export_to_csv("test_phones.csv")