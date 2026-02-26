#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""카카오톡 창 UI 구조 분석"""
import sys, time
sys.stdout.reconfigure(encoding='utf-8')

from pywinauto import Application

KAKAO_EXE = r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"

try:
    app = Application(backend='uia').connect(path=KAKAO_EXE, timeout=5)
    wins = app.windows()
    print(f"=== 발견된 창: {len(wins)}개 ===")
    for w in wins:
        print(f"  Window: [{w.window_text()}] class=[{w.class_name()}]")

    main_win = wins[0] if wins else None
    if not main_win:
        print("메인 창을 찾을 수 없습니다.")
        sys.exit(1)

    print(f"\n=== 메인 창: {main_win.window_text()} ===")
    print(f"=== 1단계 자식 요소 ===")
    children = main_win.children()
    for c in children:
        try:
            txt = c.window_text().strip()
            ctype = c.element_info.control_type
            cname = c.class_name()
            print(f"  [{ctype}] class={cname} text=[{txt[:50]}]")
        except:
            pass

    print(f"\n=== 2단계 descendants (최대 100개) ===")
    descs = main_win.descendants()
    count = 0
    for d in descs:
        if count >= 100:
            print("  ... (100개 초과, 생략)")
            break
        try:
            txt = d.window_text().strip()
            ctype = d.element_info.control_type
            if txt and len(txt) >= 1:
                print(f"  [{ctype}] text=[{txt[:60]}]")
                count += 1
        except:
            pass

    print(f"\n총 텍스트 있는 요소: {count}개")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
