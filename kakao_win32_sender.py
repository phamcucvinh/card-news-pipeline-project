#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카카오톡 Win32API 다중 발송기
- 백그라운드 동작 (화면 제어 X)
- 열린 채팅방에 메시지 전송
- Win32 SendMessage로 직접 전달
"""

import sys
import time
import json
import os
import ctypes
import ctypes.wintypes
import threading
from datetime import datetime

try:
    import win32gui
    import win32con
    import win32api
    import win32clipboard
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "-q"])
    import win32gui
    import win32con
    import win32api
    import win32clipboard

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except ImportError:
    print("tkinter 필요")
    sys.exit(1)


# ─── Win32 카카오톡 핸들 찾기 ────────────────────────
def find_kakao_main():
    """카카오톡 메인 창 핸들"""
    hwnd = win32gui.FindWindow(None, "카카오톡")
    if not hwnd:
        hwnd = win32gui.FindWindow(None, "KakaoTalk")
    return hwnd


def find_open_chatrooms():
    """열려있는 모든 카카오톡 채팅방 찾기"""
    chatrooms = []

    def enum_callback(hwnd, results):
        if not win32gui.IsWindowVisible(hwnd):
            return
        class_name = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return

        # 카카오톡 채팅창 클래스
        if class_name in ("EVA_Window_Dblclk", "EVA_Window"):
            # 메인 창 제외
            if title in ("카카오톡", "KakaoTalk"):
                return
            # RichEdit20W 자식이 있는지 확인 (채팅 입력창)
            child = win32gui.FindWindowEx(hwnd, 0, "RichEdit20W", None)
            if child:
                results.append({"hwnd": hwnd, "child": child, "title": title})

    win32gui.EnumWindows(enum_callback, chatrooms)
    return chatrooms


def set_clipboard_text(text):
    """클립보드에 텍스트 설정"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


def send_to_chatroom(hwnd, child_hwnd, message):
    """Win32 API로 채팅방에 메시지 전송 (백그라운드)"""
    try:
        # 클립보드에 메시지 복사
        set_clipboard_text(message)
        time.sleep(0.05)

        # 채팅 입력창에 붙여넣기 (WM_PASTE)
        win32api.SendMessage(child_hwnd, win32con.WM_PASTE, 0, 0)
        time.sleep(0.05)

        # Enter 키 전송 (WM_KEYDOWN + WM_KEYUP)
        win32api.SendMessage(child_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        time.sleep(0.02)
        win32api.SendMessage(child_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        time.sleep(0.05)

        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


# ─── GUI ─────────────────────────────────────────────
class KakaoWin32GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("카카오톡 Win32 발송기 (백그라운드)")
        self.root.geometry("580x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#FEE500")
        self.sending = False
        self.chat_vars = {}
        self.chat_data = {}
        self.build_ui()

    def build_ui(self):
        # 헤더
        header = tk.Frame(self.root, bg="#FEE500", pady=8)
        header.pack(fill="x")
        tk.Label(header, text="카카오톡 Win32 발송기", font=("맑은 고딕", 18, "bold"),
                 bg="#FEE500", fg="#3C1E1E").pack()
        tk.Label(header, text="백그라운드 동작 | 화면 제어 없음 | Win32API",
                 font=("맑은 고딕", 9), bg="#FEE500", fg="#5D4037").pack()

        main = tk.Frame(self.root, bg="white", padx=15, pady=10)
        main.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # ─── 채팅방 목록 ───
        room_header = tk.Frame(main, bg="white")
        room_header.pack(fill="x")
        tk.Label(room_header, text="열린 채팅방 선택", font=("맑은 고딕", 11, "bold"),
                 bg="white").pack(side="left")

        self.refresh_btn = tk.Button(
            room_header, text="새로고침", font=("맑은 고딕", 9, "bold"),
            bg="#FEE500", fg="#3C1E1E", relief="flat", padx=10, pady=2,
            cursor="hand2", command=self.refresh_chatrooms)
        self.refresh_btn.pack(side="right")

        tk.Label(main, text="카카오톡에서 채팅방을 열어두면 자동으로 감지됩니다",
                 font=("맑은 고딕", 8), bg="white", fg="#999").pack(fill="x", anchor="w")

        # 버튼 줄
        btn_row = tk.Frame(main, bg="white")
        btn_row.pack(fill="x", pady=(3, 0))
        tk.Button(btn_row, text="전체선택", font=("맑은 고딕", 8),
                  bg="#E8F5E9", relief="flat", padx=6,
                  command=self.select_all).pack(side="left", padx=(0, 3))
        tk.Button(btn_row, text="전체해제", font=("맑은 고딕", 8),
                  bg="#FFEBEE", relief="flat", padx=6,
                  command=self.deselect_all).pack(side="left")

        self.count_label = tk.Label(btn_row, text="감지: 0개 | 선택: 0개",
                                     font=("맑은 고딕", 9, "bold"),
                                     bg="white", fg="#1976D2")
        self.count_label.pack(side="right")

        # 체크박스 리스트
        list_frame = tk.Frame(main, bg="white", relief="solid", borderwidth=1)
        list_frame.pack(fill="both", expand=True, pady=(3, 5))

        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0, height=180)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg="white")
        self.inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # ─── 메시지 ───
        tk.Label(main, text="메시지 내용", font=("맑은 고딕", 11, "bold"),
                 bg="white", anchor="w").pack(fill="x", pady=(5, 2))

        self.message_text = scrolledtext.ScrolledText(
            main, height=5, font=("맑은 고딕", 11), wrap="word",
            relief="solid", borderwidth=1)
        self.message_text.pack(fill="x", pady=(0, 5))
        self.message_text.insert("1.0", "안녕하세요, 테스트 메시지입니다")

        # ─── 옵션 ───
        opt_frame = tk.Frame(main, bg="white")
        opt_frame.pack(fill="x", pady=(0, 5))

        tk.Label(opt_frame, text="전송 횟수:", font=("맑은 고딕", 10),
                 bg="white").pack(side="left")
        self.count_var = tk.StringVar(value="1")
        ttk.Spinbox(opt_frame, from_=1, to=100, increment=1,
                     textvariable=self.count_var, width=5,
                     font=("맑은 고딕", 10)).pack(side="left", padx=(3, 10))

        tk.Label(opt_frame, text="간격(초):", font=("맑은 고딕", 10),
                 bg="white").pack(side="left")
        self.delay_var = tk.StringVar(value="1.0")
        ttk.Spinbox(opt_frame, from_=0.1, to=10, increment=0.1,
                     textvariable=self.delay_var, width=5,
                     font=("맑은 고딕", 10)).pack(side="left", padx=(3, 0))

        # ─── 전송 버튼 ───
        ctrl_frame = tk.Frame(main, bg="white")
        ctrl_frame.pack(fill="x", pady=(0, 5))

        self.send_btn = tk.Button(
            ctrl_frame, text="전송 시작", font=("맑은 고딕", 13, "bold"),
            bg="#FEE500", fg="#3C1E1E", relief="flat", padx=20, pady=6,
            cursor="hand2", command=self.on_send)
        self.send_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.stop_btn = tk.Button(
            ctrl_frame, text="중지", font=("맑은 고딕", 13, "bold"),
            bg="#E0E0E0", fg="#555", relief="flat", padx=20, pady=6,
            state="disabled", command=self.on_stop)
        self.stop_btn.pack(side="left", expand=True, fill="x")

        # ─── 로그 ───
        tk.Label(main, text="전송 로그", font=("맑은 고딕", 10, "bold"),
                 bg="white", anchor="w").pack(fill="x", pady=(3, 2))

        self.log_text = scrolledtext.ScrolledText(
            main, height=6, font=("Consolas", 9), wrap="word",
            relief="solid", borderwidth=1, state="disabled", bg="#F5F5F5")
        self.log_text.pack(fill="x")

        # 상태바
        self.status_var = tk.StringVar(value="대기 중 - '새로고침'을 눌러 채팅방을 감지하세요")
        tk.Label(self.root, textvariable=self.status_var, font=("맑은 고딕", 9),
                 bg="#E0E0E0", anchor="w", padx=10, pady=3).pack(fill="x", side="bottom")

        # 자동 새로고침
        self.refresh_chatrooms()

    def refresh_chatrooms(self):
        for w in self.inner.winfo_children():
            w.destroy()
        self.chat_vars = {}
        self.chat_data = {}

        rooms = find_open_chatrooms()
        for room in rooms:
            title = room["title"]
            var = tk.BooleanVar(value=True)
            var.trace_add("write", lambda *a: self.update_count())

            row = tk.Frame(self.inner, bg="white")
            row.pack(fill="x", padx=3, pady=1)

            tk.Checkbutton(row, text=title, variable=var,
                          font=("맑은 고딕", 10), bg="white",
                          activebackground="#FFF9C4", anchor="w"
                          ).pack(side="left", fill="x", expand=True)

            tk.Label(row, text=f"hwnd:{room['hwnd']}",
                     font=("Consolas", 7), bg="white", fg="#BBB").pack(side="right")

            self.chat_vars[title] = var
            self.chat_data[title] = room

        self.update_count()
        self.log(f"채팅방 {len(rooms)}개 감지됨")
        self.status_var.set(f"채팅방 {len(rooms)}개 감지 | 체크 후 전송하세요")

    def update_count(self):
        total = len(self.chat_vars)
        selected = sum(1 for v in self.chat_vars.values() if v.get())
        self.count_label.configure(text=f"감지: {total}개 | 선택: {selected}개")

    def select_all(self):
        for v in self.chat_vars.values():
            v.set(True)

    def deselect_all(self):
        for v in self.chat_vars.values():
            v.set(False)

    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def on_send(self):
        selected = [(t, d) for t, d in self.chat_data.items()
                     if self.chat_vars.get(t, tk.BooleanVar()).get()]
        message = self.message_text.get("1.0", "end").strip()

        if not selected:
            messagebox.showwarning("알림", "채팅방을 선택하세요.\n'새로고침'으로 열린 채팅방을 감지합니다.")
            return
        if not message:
            messagebox.showwarning("알림", "메시지를 입력하세요.")
            return

        names = [t for t, d in selected]
        count = int(self.count_var.get())

        if not messagebox.askyesno("전송 확인",
                f"{len(names)}개 채팅방 x {count}회 = 총 {len(names)*count}건\n\n"
                f"채팅방: {', '.join(names[:5])}{'...' if len(names)>5 else ''}\n"
                f"메시지: {message[:80]}{'...' if len(message)>80 else ''}\n\n"
                f"전송하시겠습니까?"):
            return

        self.sending = True
        self.send_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal", bg="#FF5252", fg="white")
        threading.Thread(target=self.send_thread,
                         args=(selected, message, count), daemon=True).start()

    def on_stop(self):
        self.sending = False
        self.log("중지됨")
        self.status_var.set("중지됨")
        self.send_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled", bg="#E0E0E0", fg="#555")

    def send_thread(self, selected, message, count):
        delay = float(self.delay_var.get())
        total = len(selected) * count
        self.root.after(0, lambda: self.log(f"=== 발송 시작: {len(selected)}방 x {count}회 ==="))

        success, fail, sent = 0, 0, 0
        for round_num in range(count):
            if not self.sending:
                break

            for title, data in selected:
                if not self.sending:
                    break

                sent += 1
                self.root.after(0, lambda s=sent, t=title, r=round_num+1: (
                    self.status_var.set(f"[{s}/{total}] {t} (#{r})"),
                    self.log(f"[{s}/{total}] {t} (#{r})")
                ))

                if send_to_chatroom(data["hwnd"], data["child"], message):
                    success += 1
                    self.root.after(0, lambda t=title: self.log(f"  -> {t}: OK"))
                else:
                    fail += 1
                    self.root.after(0, lambda t=title: self.log(f"  -> {t}: FAIL"))

                time.sleep(delay)

        s, f = success, fail
        self.root.after(0, lambda: self.log(f"=== 완료: 성공 {s} / 실패 {f} ==="))
        self.root.after(0, lambda: self.status_var.set(f"완료 - 성공: {s} / 실패: {f}"))
        self.root.after(0, lambda: self.send_btn.configure(state="normal"))
        self.root.after(0, lambda: self.stop_btn.configure(state="disabled", bg="#E0E0E0", fg="#555"))
        self.sending = False

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = KakaoWin32GUI()
    app.run()
