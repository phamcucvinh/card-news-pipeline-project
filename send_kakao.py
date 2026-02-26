#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""카카오톡 PC앱 다중 메시지 발송기 (pyautogui)"""

import subprocess
import time
import sys
import json
from datetime import datetime

try:
    import pyautogui
    import pyperclip
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip"])
    import pyautogui
    import pyperclip


def activate_kakao():
    """카카오톡 창 활성화 (한 번만)"""
    subprocess.Popen([r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"])
    time.sleep(3)

    kakao_windows = pyautogui.getWindowsWithTitle("카카오톡")
    if not kakao_windows:
        kakao_windows = pyautogui.getWindowsWithTitle("KakaoTalk")

    if not kakao_windows:
        print("[ERROR] 카카오톡 창을 찾을 수 없습니다. 로그인 상태를 확인하세요.")
        return None

    kakao_win = kakao_windows[0]
    kakao_win.activate()
    time.sleep(1)
    return kakao_win


def send_to_one(kakao_win, chat_name, message):
    """한 명에게 메시지 전송"""
    try:
        kakao_win.activate()
        time.sleep(0.5)

        # 채팅 검색
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)

        # 이전 검색어 지우기
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)

        # 이름 입력
        pyperclip.copy(chat_name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        # 채팅방 열기
        pyautogui.press("enter")
        time.sleep(1)

        # 메시지 입력
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)

        # 전송
        pyautogui.press("enter")
        time.sleep(0.5)

        # 검색창 닫기
        pyautogui.press("escape")
        time.sleep(0.3)

        return True
    except Exception as e:
        print(f"  [FAIL] {chat_name}: {e}")
        return False


def send_kakao_multi(recipients, message, delay=1.5):
    """
    여러 명에게 카카오톡 메시지 전송

    Args:
        recipients: 받는 사람 리스트 ["이름1", "이름2", ...]
        message: 보낼 메시지
        delay: 전송 간 대기시간(초)
    """
    print(f"=== 카카오톡 다중 발송 ===")
    print(f"받는 사람: {len(recipients)}명")
    print(f"메시지: {message[:50]}{'...' if len(message) > 50 else ''}")
    print(f"{'='*30}")

    kakao_win = activate_kakao()
    if not kakao_win:
        return

    results = {"success": [], "fail": [], "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    for i, name in enumerate(recipients, 1):
        print(f"[{i}/{len(recipients)}] {name} 전송 중...", end=" ")

        if send_to_one(kakao_win, name, message):
            print("OK")
            results["success"].append(name)
        else:
            print("FAIL")
            results["fail"].append(name)

        if i < len(recipients):
            time.sleep(delay)

    # 결과 출력
    print(f"\n{'='*30}")
    print(f"[결과] 성공: {len(results['success'])}명 / 실패: {len(results['fail'])}명")
    if results["fail"]:
        print(f"[실패 목록] {', '.join(results['fail'])}")

    # 결과 저장
    with open("kakao_send_log.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results


# ============================================================
# 여기서 받는 사람과 메시지를 수정하세요
# ============================================================
if __name__ == "__main__":

    # 받는 사람 목록 (카카오톡 채팅방 이름 또는 친구 이름)
    recipients = [
        "나",           # 나에게 보내기
        # "홍길동",     # 친구 이름 추가
        # "가족방",     # 그룹채팅방 이름
        # "회사팀",     # 채팅방 이름
    ]

    # 보낼 메시지
    message = "안녕하세요, 테스트 메시지입니다"

    # 전송 (delay: 전송 간 대기시간, 초)
    send_kakao_multi(recipients, message, delay=1.5)
