#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
from typing import List, Dict
import os

class KakaoTalkAutomation:
    """카카오톡 PC버전 자동화 클래스"""
    
    def __init__(self, headless=False, delay=2):
        self.driver = None
        self.wait = None
        self.delay = delay
        self.setup_logging()
        self.setup_driver(headless)
    
    def setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kakao_automation.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self, headless=False):
        """Chrome WebDriver 설정"""
        try:
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # 프록시 완전 비활성화
            chrome_options.add_argument('--no-proxy-server')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Chrome WebDriver 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"WebDriver 설정 실패: {e}")
            raise
    
    def open_kakao_web(self):
        """카카오톡 웹 페이지 열기"""
        try:
            self.driver.get("https://web.kakao.com/")
            self.logger.info("카카오톡 웹 페이지 열기 완료")
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"카카오톡 웹 페이지 열기 실패: {e}")
            return False
    
    def wait_for_login(self, timeout=300):
        """사용자 로그인 대기"""
        self.logger.info("사용자 로그인을 기다리는 중...")
        self.logger.info("QR코드를 스캔하거나 카카오계정으로 로그인해주세요.")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 채팅 목록이 보이면 로그인 완료
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list_chat")))
                self.logger.info("로그인 완료!")
                return True
            except TimeoutException:
                time.sleep(2)
                continue
        
        self.logger.error("로그인 시간 초과")
        return False
    
    def find_contact_search(self):
        """연락처 검색창 찾기"""
        try:
            # 여러 가능한 검색창 selector 시도
            search_selectors = [
                "input[placeholder*='검색']",
                "input[placeholder*='대화상대']",
                ".search_box input",
                ".input_search"
            ]
            
            for selector in search_selectors:
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_box.is_displayed():
                        return search_box
                except NoSuchElementException:
                    continue
            
            return None
        except Exception as e:
            self.logger.error(f"검색창 찾기 실패: {e}")
            return None
    
    def add_contact_by_phone(self, phone_number: str, name: str = None) -> bool:
        """전화번호로 연락처 추가"""
        try:
            self.logger.info(f"연락처 추가 시도: {phone_number} ({name})")
            
            # 연락처 추가 버튼 클릭
            add_buttons = [
                "button[title*='친구']",
                ".btn_add",
                "[data-testid='add-friend']"
            ]
            
            add_button = None
            for selector in add_buttons:
                try:
                    add_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if add_button.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            
            if not add_button:
                self.logger.warning("연락처 추가 버튼을 찾을 수 없습니다.")
                return False
            
            add_button.click()
            time.sleep(self.delay)
            
            # 전화번호 입력
            phone_input_selectors = [
                "input[placeholder*='전화번호']",
                "input[type='tel']",
                ".input_phone"
            ]
            
            phone_input = None
            for selector in phone_input_selectors:
                try:
                    phone_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if phone_input.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            
            if not phone_input:
                self.logger.warning("전화번호 입력창을 찾을 수 없습니다.")
                return False
            
            phone_input.clear()
            phone_input.send_keys(phone_number)
            time.sleep(self.delay)
            
            # 확인/추가 버튼 클릭
            confirm_buttons = [
                "button[type='submit']",
                ".btn_confirm",
                ".btn_add_friend"
            ]
            
            for selector in confirm_buttons:
                try:
                    confirm_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if confirm_btn.is_displayed():
                        confirm_btn.click()
                        break
                except NoSuchElementException:
                    continue
            
            time.sleep(self.delay * 2)
            self.logger.info(f"연락처 추가 완료: {phone_number}")
            return True
            
        except Exception as e:
            self.logger.error(f"연락처 추가 실패 ({phone_number}): {e}")
            return False
    
    def add_contacts_batch(self, contacts: List[Dict], batch_size: int = 10) -> Dict:
        """연락처 배치 추가"""
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        self.logger.info(f"{len(contacts)}개의 연락처 배치 추가 시작")
        
        for i, contact in enumerate(contacts):
            if i > 0 and i % batch_size == 0:
                self.logger.info(f"배치 처리 중... ({i}/{len(contacts)})")
                time.sleep(5)  # 배치 간 대기시간
            
            phone = contact.get('phone', '')
            name = contact.get('company', f"연락처{i+1}")
            
            if self.add_contact_by_phone(phone, name):
                results['success'] += 1
            else:
                results['failed'] += 1
                results['errors'].append({
                    'phone': phone,
                    'name': name,
                    'error': '추가 실패'
                })
            
            # 각 연락처 추가 후 대기
            time.sleep(self.delay)
        
        self.logger.info(f"배치 추가 완료: 성공 {results['success']}, 실패 {results['failed']}")
        return results
    
    def close_driver(self):
        """WebDriver 종료"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver 종료 완료")
        except Exception as e:
            self.logger.error(f"WebDriver 종료 중 오류: {e}")

# 테스트용 함수
def test_kakao_automation():
    """카카오톡 자동화 테스트"""
    automation = KakaoTalkAutomation(headless=False)
    
    try:
        # 카카오톡 웹 열기
        if not automation.open_kakao_web():
            return
        
        # 로그인 대기
        if not automation.wait_for_login():
            return
        
        # 테스트용 더미 데이터
        test_contacts = [
            {'phone': '01012345678', 'company': '테스트1'},
            {'phone': '01087654321', 'company': '테스트2'}
        ]
        
        # 연락처 추가 테스트
        results = automation.add_contacts_batch(test_contacts, batch_size=5)
        print(f"테스트 결과: {results}")
        
    finally:
        automation.close_driver()

if __name__ == "__main__":
    test_kakao_automation()