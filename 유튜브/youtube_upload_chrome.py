"""
YouTube 업로더 - Chrome 기반
Windows에서 직접 실행 가능
"""

import os
import sys
import time
import json
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("필요한 패키지를 설치합니다...")
    os.system("pip install selenium webdriver-manager")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager


class YouTubeUploader:
    YOUTUBE_STUDIO_URL = "https://studio.youtube.com"
    YOUTUBE_UPLOAD_URL = "https://www.youtube.com/upload"

    def __init__(self, video_path, title=None, description="", tags=None, privacy="unlisted"):
        self.video_path = os.path.abspath(video_path)
        self.title = title or Path(video_path).stem
        self.description = description
        self.tags = tags or []
        self.privacy = privacy  # public, unlisted, private
        self.driver = None

    def setup_driver(self):
        """Chrome 드라이버 설정"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # 사용자 프로필 사용 (로그인 상태 유지)
        user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_profile")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def wait_for_element(self, by, value, timeout=30):
        """요소가 나타날 때까지 대기"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def upload(self):
        """영상 업로드 실행"""
        try:
            self.setup_driver()
            print(f"영상 업로드 시작: {self.video_path}")

            # YouTube Studio 접속
            self.driver.get(self.YOUTUBE_UPLOAD_URL)
            time.sleep(3)

            # 로그인 확인
            if "accounts.google.com" in self.driver.current_url:
                print("\n" + "="*50)
                print("Google 계정으로 로그인해주세요.")
                print("로그인 완료 후 Enter를 눌러주세요...")
                print("="*50)
                input()
                time.sleep(2)

            # 파일 선택
            print("파일 업로드 중...")
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(self.video_path)
            time.sleep(5)

            # 제목 입력
            print(f"제목 설정: {self.title}")
            title_input = self.wait_for_element(By.ID, "textbox")
            title_input.clear()
            title_input.send_keys(Keys.CONTROL + "a")
            title_input.send_keys(self.title)
            time.sleep(1)

            # 설명 입력
            if self.description:
                print("설명 입력 중...")
                desc_inputs = self.driver.find_elements(By.ID, "textbox")
                if len(desc_inputs) > 1:
                    desc_inputs[1].click()
                    desc_inputs[1].send_keys(self.description)

            # 아동용 콘텐츠 아님 선택
            try:
                not_for_kids = self.driver.find_element(
                    By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK"
                )
                not_for_kids.click()
                time.sleep(1)
            except:
                pass

            # 다음 버튼 클릭 (3번)
            for i in range(3):
                try:
                    next_btn = self.driver.find_element(By.ID, "next-button")
                    next_btn.click()
                    time.sleep(2)
                    print(f"다음 단계 {i+1}/3")
                except:
                    pass

            # 공개 설정
            print(f"공개 설정: {self.privacy}")
            privacy_map = {
                "public": "PUBLIC",
                "unlisted": "UNLISTED",
                "private": "PRIVATE"
            }
            try:
                privacy_radio = self.driver.find_element(
                    By.NAME, privacy_map.get(self.privacy, "UNLISTED")
                )
                privacy_radio.click()
                time.sleep(1)
            except:
                pass

            # 업로드 완료 대기
            print("업로드 진행 중... (완료까지 대기)")
            time.sleep(5)

            # 완료 버튼 클릭
            try:
                done_btn = self.wait_for_element(By.ID, "done-button", timeout=600)
                # 버튼이 활성화될 때까지 대기
                while done_btn.get_attribute("aria-disabled") == "true":
                    print(".", end="", flush=True)
                    time.sleep(5)
                print()
                done_btn.click()
                print("업로드 완료!")
            except Exception as e:
                print(f"완료 버튼 클릭 실패: {e}")

            time.sleep(3)
            return True

        except Exception as e:
            print(f"오류 발생: {e}")
            return False
        finally:
            if self.driver:
                input("\nEnter를 누르면 브라우저가 종료됩니다...")
                self.driver.quit()


def main():
    print("="*50)
    print("  YouTube 업로더 (Chrome 기반)")
    print("="*50)

    # 테스트 영상 찾기
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    current_dir = os.path.dirname(os.path.abspath(__file__))

    videos = []
    for ext in video_extensions:
        videos.extend(Path(current_dir).glob(f"*{ext}"))

    if not videos:
        print("\n현재 폴더에 영상 파일이 없습니다.")
        video_path = input("영상 파일 경로를 입력하세요: ").strip().strip('"')
    else:
        print("\n발견된 영상 파일:")
        for i, v in enumerate(videos, 1):
            print(f"  {i}. {v.name}")

        choice = input("\n업로드할 영상 번호 (또는 경로 직접 입력): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(videos):
            video_path = str(videos[int(choice)-1])
        else:
            video_path = choice.strip('"')

    if not os.path.exists(video_path):
        print(f"파일을 찾을 수 없습니다: {video_path}")
        return

    title = input(f"영상 제목 (Enter=파일명 사용): ").strip()
    if not title:
        title = Path(video_path).stem

    description = input("영상 설명 (선택사항): ").strip()

    print("\n공개 설정:")
    print("  1. public (공개)")
    print("  2. unlisted (미등록)")
    print("  3. private (비공개)")
    privacy_choice = input("선택 (기본=2): ").strip()
    privacy_map = {"1": "public", "2": "unlisted", "3": "private"}
    privacy = privacy_map.get(privacy_choice, "unlisted")

    print("\n" + "="*50)
    print(f"영상: {video_path}")
    print(f"제목: {title}")
    print(f"공개: {privacy}")
    print("="*50)

    confirm = input("\n업로드를 시작하시겠습니까? (y/n): ").strip().lower()
    if confirm != 'y':
        print("취소되었습니다.")
        return

    uploader = YouTubeUploader(
        video_path=video_path,
        title=title,
        description=description,
        privacy=privacy
    )
    uploader.upload()


if __name__ == "__main__":
    main()
