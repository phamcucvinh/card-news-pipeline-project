#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카카오톡 올인원 발송기 v1.0
- 모드1: 이름 검색 발송 (pyautogui) - 개인/단톡방 체크박스
- 모드2: Win32API 백그라운드 발송 - 열린 채팅방 자동 감지
- 모드3: 예약 발송 - 지정 시간에 자동 전송
"""

import subprocess
import time
import sys
import json
import threading
import os
from datetime import datetime, timedelta

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, filedialog
except ImportError:
    sys.exit("tkinter 필요")

try:
    import pyautogui
    import pyperclip
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip", "-q"])
    import pyautogui
    import pyperclip

try:
    import win32gui
    import win32con
    import win32api
    import win32clipboard
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

KAKAO_EXE = r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(SCRIPT_DIR, "kakao_contacts.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "kakao_send_log.json")


# ══════════════════════════════════════════════════════
#  Win32 API 함수
# ══════════════════════════════════════════════════════
def find_open_chatrooms():
    if not HAS_WIN32:
        return []
    rooms = []

    def enum_cb(hwnd, results):
        if not win32gui.IsWindowVisible(hwnd):
            return
        cls = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if not title or title in ("\uce74\uce74\uc624\ud1a1", "KakaoTalk"):
            return
        if cls in ("EVA_Window_Dblclk", "EVA_Window"):
            child = win32gui.FindWindowEx(hwnd, 0, "RichEdit20W", None)
            if child:
                results.append({"hwnd": hwnd, "child": child, "title": title})

    win32gui.EnumWindows(enum_cb, rooms)
    return rooms


def win32_send(hwnd, child, message):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(message, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        time.sleep(0.05)
        win32api.SendMessage(child, win32con.WM_PASTE, 0, 0)
        time.sleep(0.05)
        win32api.SendMessage(child, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        time.sleep(0.02)
        win32api.SendMessage(child, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        time.sleep(0.05)
        return True
    except Exception:
        return False


# ══════════════════════════════════════════════════════
#  pyautogui 함수
# ══════════════════════════════════════════════════════
def activate_kakao_pyauto():
    subprocess.Popen([KAKAO_EXE])
    time.sleep(3)
    wins = pyautogui.getWindowsWithTitle("\uce74\uce74\uc624\ud1a1")
    if not wins:
        wins = pyautogui.getWindowsWithTitle("KakaoTalk")
    if not wins:
        return None
    w = wins[0]
    w.activate()
    time.sleep(1)
    return w


def pyauto_send(kakao_win, name, message):
    try:
        kakao_win.activate()
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press("escape")
        time.sleep(0.3)
        return True
    except Exception:
        return False


# ══════════════════════════════════════════════════════
#  메인 GUI
# ══════════════════════════════════════════════════════
class KakaoUltimateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("카카오톡 올인원 발송기 v1.0")
        self.root.geometry("660x920")
        self.root.resizable(False, False)
        self.root.configure(bg="#FEE500")
        self.sending = False
        self.scheduled_timer = None

        # 연락처 데이터
        self.contact_vars = {}
        self.contact_widgets = {}
        self.contact_types = {}
        self.saved_data = self.load_contacts()

        # Win32 채팅방
        self.room_vars = {}
        self.room_data = {}
        self.room_widgets = {}

        self.build_ui()

    # ─── 연락처 저장/로드 ────────────────────
    def load_contacts(self):
        try:
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data and isinstance(data[0], str):
                return [{"name": n, "type": "person"} for n in data]
            return data
        except (FileNotFoundError, json.JSONDecodeError, IndexError):
            return []

    def save_contacts(self):
        data = [{"name": n, "type": self.contact_types.get(n, "person")}
                for n in self.contact_vars.keys()]
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ─── UI ──────────────────────────────────
    def build_ui(self):
        # 헤더
        hdr = tk.Frame(self.root, bg="#FEE500", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text="카카오톡 올인원 발송기", font=("맑은 고딕", 20, "bold"),
                 bg="#FEE500", fg="#3C1E1E").pack()
        tk.Label(hdr, text="이름검색 | Win32 백그라운드 | 예약발송",
                 font=("맑은 고딕", 9), bg="#FEE500", fg="#5D4037").pack()

        # 탭
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("맑은 고딕", 10, "bold"), padding=[12, 4])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        # 탭1: 이름 검색 모드
        self.tab1 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab1, text="  이름 검색 발송  ")
        self.build_tab1()

        # 탭2: Win32 백그라운드
        self.tab2 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab2, text="  Win32 백그라운드  ")
        self.build_tab2()

        # 탭3: 예약 발송
        self.tab3 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab3, text="  예약 발송  ")
        self.build_tab3()

        # 공통 로그
        log_frame = tk.Frame(self.root, bg="white", padx=10, pady=5)
        log_frame.pack(fill="x", padx=8, pady=(0, 4))
        tk.Label(log_frame, text="전송 로그", font=("맑은 고딕", 10, "bold"),
                 bg="white").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=7, font=("Consolas", 9), wrap="word",
            relief="solid", borderwidth=1, state="disabled", bg="#F5F5F5")
        self.log_text.pack(fill="x")

        # 상태바
        self.status_var = tk.StringVar(value="대기 중")
        tk.Label(self.root, textvariable=self.status_var, font=("맑은 고딕", 9),
                 bg="#E0E0E0", anchor="w", padx=10, pady=3).pack(fill="x", side="bottom")

    # ══════════════════════════════════════════
    #  탭1: 이름 검색 발송
    # ══════════════════════════════════════════
    def build_tab1(self):
        p = tk.Frame(self.tab1, bg="white", padx=12, pady=8)
        p.pack(fill="both", expand=True)

        # 필터
        flt = tk.Frame(p, bg="white")
        flt.pack(fill="x")
        tk.Label(flt, text="받는 사람", font=("맑은 고딕", 11, "bold"), bg="white").pack(side="left")

        self.t1_filter = "all"
        self.t1_filter_btns = {}
        for label, key, color in [("전체", "all", "#E0E0E0"), ("개인", "person", "#BBDEFB"),
                                    ("단톡방", "group", "#C8E6C9")]:
            btn = tk.Button(flt, text=label, font=("맑은 고딕", 8), bg=color,
                            relief="flat", padx=6,
                            command=lambda k=key: self.t1_set_filter(k))
            btn.pack(side="left", padx=(5, 0))
            self.t1_filter_btns[key] = btn

        self.t1_count = tk.Label(flt, text="선택: 0명", font=("맑은 고딕", 9, "bold"),
                                  bg="white", fg="#1976D2")
        self.t1_count.pack(side="right")

        # 버튼
        br = tk.Frame(p, bg="white")
        br.pack(fill="x", pady=(2, 0))
        for txt, cmd, bg in [("전체선택", self.t1_select_all, "#E8F5E9"),
                              ("전체해제", self.t1_deselect, "#FFEBEE"),
                              ("선택삭제", self.t1_delete, "#FFF3E0"),
                              ("TXT불러오기", self.t1_load_txt, "#E3F2FD"),
                              ("저장", self.save_contacts, "#F3E5F5")]:
            tk.Button(br, text=txt, font=("맑은 고딕", 8), bg=bg, relief="flat",
                      padx=5, command=cmd).pack(side="left", padx=(0, 2))

        # 검색
        sf = tk.Frame(p, bg="white")
        sf.pack(fill="x", pady=(2, 2))
        tk.Label(sf, text="검색:", font=("맑은 고딕", 9), bg="white").pack(side="left")
        self.t1_search = tk.StringVar()
        self.t1_search.trace_add("write", self.t1_apply_filter)
        tk.Entry(sf, textvariable=self.t1_search, font=("맑은 고딕", 10),
                 relief="solid", borderwidth=1).pack(side="left", fill="x", expand=True, padx=(3, 0))

        # 리스트
        lf = tk.Frame(p, bg="white", relief="solid", borderwidth=1)
        lf.pack(fill="both", expand=True, pady=(0, 3))
        self.t1_canvas = tk.Canvas(lf, bg="white", highlightthickness=0, height=140)
        sb = ttk.Scrollbar(lf, orient="vertical", command=self.t1_canvas.yview)
        self.t1_inner = tk.Frame(self.t1_canvas, bg="white")
        self.t1_inner.bind("<Configure>",
            lambda e: self.t1_canvas.configure(scrollregion=self.t1_canvas.bbox("all")))
        self.t1_canvas.create_window((0, 0), window=self.t1_inner, anchor="nw")
        self.t1_canvas.configure(yscrollcommand=sb.set)
        self.t1_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.t1_canvas.bind_all("<MouseWheel>",
            lambda e: self.t1_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # 추가 영역
        af = tk.LabelFrame(p, text="추가", font=("맑은 고딕", 9, "bold"), bg="white", padx=6, pady=4)
        af.pack(fill="x", pady=(0, 3))
        nr = tk.Frame(af, bg="white")
        nr.pack(fill="x")
        self.t1_add_entry = tk.Entry(nr, font=("맑은 고딕", 10), relief="solid", borderwidth=1)
        self.t1_add_entry.pack(side="left", fill="x", expand=True)
        self.t1_add_entry.bind("<Return>", lambda e: self.t1_add())
        self.t1_type_var = tk.StringVar(value="person")
        tk.Radiobutton(nr, text="개인", variable=self.t1_type_var, value="person",
                        font=("맑은 고딕", 9), bg="white").pack(side="left", padx=(5, 0))
        tk.Radiobutton(nr, text="단톡방", variable=self.t1_type_var, value="group",
                        font=("맑은 고딕", 9), bg="white").pack(side="left")
        tk.Button(nr, text="추가", font=("맑은 고딕", 9, "bold"), bg="#FEE500",
                  relief="flat", padx=10, command=self.t1_add).pack(side="right")

        # 메시지 + 전송
        self.t1_msg = self._build_message_area(p)
        self._build_send_buttons(p, self.on_send_tab1)

        # 기존 연락처 로드
        for item in self.saved_data:
            n = item["name"] if isinstance(item, dict) else item
            t = item.get("type", "person") if isinstance(item, dict) else "person"
            self.t1_add_contact(n, t)
        self.t1_set_filter("all")

    def t1_add_contact(self, name, ctype="person", checked=False):
        if name in self.contact_vars:
            return
        var = tk.BooleanVar(value=checked)
        var.trace_add("write", lambda *a: self.t1_update_count())
        self.contact_types[name] = ctype
        self.contact_vars[name] = var
        row = tk.Frame(self.t1_inner, bg="white")
        badge_bg = "#C8E6C9" if ctype == "group" else "#BBDEFB"
        badge_txt = "단톡" if ctype == "group" else "개인"
        tk.Label(row, text=badge_txt, font=("맑은 고딕", 8), bg=badge_bg,
                 padx=3).pack(side="left", padx=(2, 4))
        tk.Checkbutton(row, text=name, variable=var, font=("맑은 고딕", 10),
                        bg="white", anchor="w").pack(side="left", fill="x", expand=True)
        row.pack(fill="x", padx=2, pady=1)
        self.contact_widgets[name] = row

    def t1_update_count(self):
        c = sum(1 for v in self.contact_vars.values() if v.get())
        p = sum(1 for n, v in self.contact_vars.items() if v.get() and self.contact_types.get(n) == "person")
        g = sum(1 for n, v in self.contact_vars.items() if v.get() and self.contact_types.get(n) == "group")
        parts = []
        if p: parts.append(f"개인 {p}")
        if g: parts.append(f"단톡 {g}")
        self.t1_count.configure(text=f"선택: {c}명" + (f" ({', '.join(parts)})" if parts else ""))

    def t1_set_filter(self, key):
        self.t1_filter = key
        for k, b in self.t1_filter_btns.items():
            b.configure(relief="sunken" if k == key else "flat",
                        font=("맑은 고딕", 8, "bold" if k == key else ""))
        self.t1_apply_filter()

    def t1_apply_filter(self, *a):
        kw = self.t1_search.get().strip().lower()
        for name, w in self.contact_widgets.items():
            ct = self.contact_types.get(name, "person")
            show = (self.t1_filter == "all" or ct == self.t1_filter) and (kw == "" or kw in name.lower())
            w.pack(fill="x", padx=2, pady=1) if show else w.pack_forget()

    def t1_select_all(self):
        for n, v in self.contact_vars.items():
            if self.t1_filter == "all" or self.contact_types.get(n) == self.t1_filter:
                v.set(True)

    def t1_deselect(self):
        for v in self.contact_vars.values(): v.set(False)

    def t1_delete(self):
        for n in [n for n, v in self.contact_vars.items() if v.get()]:
            self.contact_widgets[n].destroy()
            del self.contact_vars[n], self.contact_widgets[n], self.contact_types[n]
        self.t1_update_count()
        self.save_contacts()

    def t1_add(self):
        raw = self.t1_add_entry.get().strip()
        if not raw: return
        for n in [x.strip() for x in raw.replace("\n", ",").split(",") if x.strip()]:
            self.t1_add_contact(n, self.t1_type_var.get(), True)
        self.save_contacts()
        self.t1_add_entry.delete(0, "end")
        self.t1_update_count()
        self.t1_apply_filter()

    def t1_load_txt(self):
        fp = filedialog.askopenfilename(filetypes=[("텍스트", "*.txt"), ("모든 파일", "*.*")])
        if not fp: return
        popup = tk.Toplevel(self.root); popup.title("유형"); popup.geometry("280x100")
        popup.transient(self.root); popup.grab_set(); popup.configure(bg="white")
        tk.Label(popup, text="유형 선택:", font=("맑은 고딕", 10), bg="white").pack(pady=(10, 5))
        bf = tk.Frame(popup, bg="white"); bf.pack()
        def load(ct):
            with open(fp, "r", encoding="utf-8") as f:
                for n in [l.strip() for l in f if l.strip()]:
                    self.t1_add_contact(n, ct)
            self.save_contacts(); self.t1_apply_filter(); popup.destroy()
        tk.Button(bf, text="개인", font=("맑은 고딕", 10, "bold"), bg="#BBDEFB",
                  relief="flat", padx=15, command=lambda: load("person")).pack(side="left", padx=5)
        tk.Button(bf, text="단톡방", font=("맑은 고딕", 10, "bold"), bg="#C8E6C9",
                  relief="flat", padx=15, command=lambda: load("group")).pack(side="left", padx=5)

    # ══════════════════════════════════════════
    #  탭2: Win32 백그라운드
    # ══════════════════════════════════════════
    def build_tab2(self):
        p = tk.Frame(self.tab2, bg="white", padx=12, pady=8)
        p.pack(fill="both", expand=True)

        if not HAS_WIN32:
            tk.Label(p, text="pywin32 미설치 - Win32 모드 사용 불가",
                     font=("맑은 고딕", 12, "bold"), bg="white", fg="red").pack(pady=40)
            return

        # 헤더
        hf = tk.Frame(p, bg="white")
        hf.pack(fill="x")
        tk.Label(hf, text="열린 채팅방", font=("맑은 고딕", 11, "bold"), bg="white").pack(side="left")
        self.t2_refresh_btn = tk.Button(hf, text="새로고침", font=("맑은 고딕", 9, "bold"),
                  bg="#FEE500", relief="flat", padx=10, command=self.t2_refresh)
        self.t2_refresh_btn.pack(side="right")

        tk.Label(p, text="카카오톡에서 채팅방을 열어두면 자동 감지 (백그라운드 전송, 화면제어 없음)",
                 font=("맑은 고딕", 8), bg="white", fg="#999").pack(fill="x", anchor="w")

        br = tk.Frame(p, bg="white")
        br.pack(fill="x", pady=(2, 0))
        tk.Button(br, text="전체선택", font=("맑은 고딕", 8), bg="#E8F5E9", relief="flat",
                  padx=6, command=lambda: [v.set(True) for v in self.room_vars.values()]).pack(side="left", padx=(0, 2))
        tk.Button(br, text="전체해제", font=("맑은 고딕", 8), bg="#FFEBEE", relief="flat",
                  padx=6, command=lambda: [v.set(False) for v in self.room_vars.values()]).pack(side="left")
        self.t2_count = tk.Label(br, text="0개", font=("맑은 고딕", 9, "bold"),
                                  bg="white", fg="#1976D2")
        self.t2_count.pack(side="right")

        # 리스트
        lf = tk.Frame(p, bg="white", relief="solid", borderwidth=1)
        lf.pack(fill="both", expand=True, pady=(2, 3))
        self.t2_canvas = tk.Canvas(lf, bg="white", highlightthickness=0, height=140)
        sb = ttk.Scrollbar(lf, orient="vertical", command=self.t2_canvas.yview)
        self.t2_inner = tk.Frame(self.t2_canvas, bg="white")
        self.t2_inner.bind("<Configure>",
            lambda e: self.t2_canvas.configure(scrollregion=self.t2_canvas.bbox("all")))
        self.t2_canvas.create_window((0, 0), window=self.t2_inner, anchor="nw")
        self.t2_canvas.configure(yscrollcommand=sb.set)
        self.t2_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # 전송 횟수
        of = tk.Frame(p, bg="white")
        of.pack(fill="x", pady=(0, 3))
        tk.Label(of, text="전송 횟수:", font=("맑은 고딕", 10), bg="white").pack(side="left")
        self.t2_repeat = tk.StringVar(value="1")
        ttk.Spinbox(of, from_=1, to=100, textvariable=self.t2_repeat, width=5,
                     font=("맑은 고딕", 10)).pack(side="left", padx=(3, 0))

        # 메시지 + 전송
        self.t2_msg = self._build_message_area(p)
        self._build_send_buttons(p, self.on_send_tab2)

        self.t2_refresh()

    def t2_refresh(self):
        for w in self.t2_inner.winfo_children(): w.destroy()
        self.room_vars.clear(); self.room_data.clear(); self.room_widgets.clear()

        rooms = find_open_chatrooms()
        for r in rooms:
            var = tk.BooleanVar(value=True)
            var.trace_add("write", lambda *a: self.t2_update_count())
            row = tk.Frame(self.t2_inner, bg="white")
            tk.Label(row, text="Win32", font=("맑은 고딕", 7), bg="#E8EAF6",
                     padx=3).pack(side="left", padx=(2, 4))
            tk.Checkbutton(row, text=r["title"], variable=var, font=("맑은 고딕", 10),
                            bg="white", anchor="w").pack(side="left", fill="x", expand=True)
            row.pack(fill="x", padx=2, pady=1)
            self.room_vars[r["title"]] = var
            self.room_data[r["title"]] = r
            self.room_widgets[r["title"]] = row

        self.t2_update_count()
        self.log(f"[Win32] 채팅방 {len(rooms)}개 감지")

    def t2_update_count(self):
        s = sum(1 for v in self.room_vars.values() if v.get())
        self.t2_count.configure(text=f"감지: {len(self.room_vars)} | 선택: {s}")

    # ══════════════════════════════════════════
    #  탭3: 예약 발송
    # ══════════════════════════════════════════
    def build_tab3(self):
        p = tk.Frame(self.tab3, bg="white", padx=12, pady=8)
        p.pack(fill="both", expand=True)

        tk.Label(p, text="예약 발송", font=("맑은 고딕", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(p, text="지정 시간에 탭1(이름검색) 선택된 대상에게 자동 전송",
                 font=("맑은 고딕", 8), bg="white", fg="#999").pack(anchor="w")

        # 시간 설정
        tf = tk.LabelFrame(p, text="예약 시간", font=("맑은 고딕", 10, "bold"),
                           bg="white", padx=10, pady=8)
        tf.pack(fill="x", pady=(8, 5))

        r1 = tk.Frame(tf, bg="white")
        r1.pack(fill="x", pady=(0, 5))
        self.t3_mode = tk.StringVar(value="after")
        tk.Radiobutton(r1, text="지금부터", variable=self.t3_mode, value="after",
                        font=("맑은 고딕", 10), bg="white").pack(side="left")
        self.t3_min = tk.StringVar(value="5")
        ttk.Spinbox(r1, from_=1, to=1440, textvariable=self.t3_min, width=5,
                     font=("맑은 고딕", 10)).pack(side="left", padx=(5, 3))
        tk.Label(r1, text="분 후", font=("맑은 고딕", 10), bg="white").pack(side="left")

        r2 = tk.Frame(tf, bg="white")
        r2.pack(fill="x")
        tk.Radiobutton(r2, text="정확한 시간", variable=self.t3_mode, value="exact",
                        font=("맑은 고딕", 10), bg="white").pack(side="left")
        self.t3_hour = tk.StringVar(value=datetime.now().strftime("%H"))
        self.t3_minute = tk.StringVar(value=datetime.now().strftime("%M"))
        ttk.Spinbox(r2, from_=0, to=23, textvariable=self.t3_hour, width=3,
                     font=("맑은 고딕", 10), format="%02.0f").pack(side="left", padx=(5, 0))
        tk.Label(r2, text=":", font=("맑은 고딕", 10, "bold"), bg="white").pack(side="left")
        ttk.Spinbox(r2, from_=0, to=59, textvariable=self.t3_minute, width=3,
                     font=("맑은 고딕", 10), format="%02.0f").pack(side="left")

        # 방식 선택
        mf = tk.LabelFrame(p, text="전송 방식", font=("맑은 고딕", 10, "bold"),
                           bg="white", padx=10, pady=5)
        mf.pack(fill="x", pady=(5, 5))
        self.t3_method = tk.StringVar(value="pyauto")
        tk.Radiobutton(mf, text="이름검색 (탭1 선택 대상)", variable=self.t3_method,
                        value="pyauto", font=("맑은 고딕", 10), bg="white").pack(anchor="w")
        tk.Radiobutton(mf, text="Win32 백그라운드 (탭2 선택 채팅방)", variable=self.t3_method,
                        value="win32", font=("맑은 고딕", 10), bg="white").pack(anchor="w")

        # 메시지
        self.t3_msg = self._build_message_area(p)

        # 예약 버튼
        bf = tk.Frame(p, bg="white")
        bf.pack(fill="x", pady=(5, 0))
        self.t3_schedule_btn = tk.Button(
            bf, text="예약 등록", font=("맑은 고딕", 13, "bold"),
            bg="#4CAF50", fg="white", relief="flat", padx=20, pady=6,
            cursor="hand2", command=self.on_schedule)
        self.t3_schedule_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.t3_cancel_btn = tk.Button(
            bf, text="예약 취소", font=("맑은 고딕", 13, "bold"),
            bg="#E0E0E0", fg="#555", relief="flat", padx=20, pady=6,
            state="disabled", command=self.on_cancel_schedule)
        self.t3_cancel_btn.pack(side="left", expand=True, fill="x")

        self.t3_timer_label = tk.Label(p, text="", font=("맑은 고딕", 11, "bold"),
                                        bg="white", fg="#E65100")
        self.t3_timer_label.pack(pady=(8, 0))

    # ─── 공용 위젯 빌더 ─────────────────────
    def _build_message_area(self, parent):
        tk.Label(parent, text="메시지", font=("맑은 고딕", 10, "bold"),
                 bg="white", anchor="w").pack(fill="x", pady=(3, 1))
        msg = scrolledtext.ScrolledText(parent, height=3, font=("맑은 고딕", 11),
                                         wrap="word", relief="solid", borderwidth=1)
        msg.pack(fill="x", pady=(0, 3))
        msg.insert("1.0", "안녕하세요, 테스트 메시지입니다")
        return msg

    def _build_send_buttons(self, parent, send_cmd):
        cf = tk.Frame(parent, bg="white")
        cf.pack(fill="x", pady=(0, 3))
        tk.Label(cf, text="간격(초):", font=("맑은 고딕", 9), bg="white").pack(side="left")
        delay = tk.StringVar(value="1.5")
        ttk.Spinbox(cf, from_=0.3, to=10, increment=0.1, textvariable=delay,
                     width=5, font=("맑은 고딕", 9)).pack(side="left", padx=(3, 10))

        send_btn = tk.Button(cf, text="전송", font=("맑은 고딕", 11, "bold"),
                  bg="#FEE500", fg="#3C1E1E", relief="flat", padx=15, pady=3,
                  cursor="hand2", command=lambda: send_cmd(delay))
        send_btn.pack(side="left", padx=(0, 5))

        stop_btn = tk.Button(cf, text="중지", font=("맑은 고딕", 11, "bold"),
                  bg="#E0E0E0", fg="#555", relief="flat", padx=15, pady=3,
                  state="disabled", command=self.on_stop)
        stop_btn.pack(side="left")

        # 버튼 참조 저장
        if send_cmd == self.on_send_tab1:
            self.t1_send_btn, self.t1_stop_btn, self.t1_delay = send_btn, stop_btn, delay
        else:
            self.t2_send_btn, self.t2_stop_btn, self.t2_delay = send_btn, stop_btn, delay

    # ─── 로그 ────────────────────────────────
    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def save_log(self, results):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    # ─── 전송 로직 ──────────────────────────
    def on_stop(self):
        self.sending = False
        self.log("중지됨")
        self.status_var.set("중지됨")
        for btn in [getattr(self, 't1_send_btn', None), getattr(self, 't2_send_btn', None)]:
            if btn: btn.configure(state="normal")
        for btn in [getattr(self, 't1_stop_btn', None), getattr(self, 't2_stop_btn', None)]:
            if btn: btn.configure(state="disabled", bg="#E0E0E0")

    def on_send_tab1(self, delay_var):
        names = [n for n, v in self.contact_vars.items() if v.get()]
        msg = self.t1_msg.get("1.0", "end").strip()
        if not names: return messagebox.showwarning("알림", "받는 사람을 선택하세요.")
        if not msg: return messagebox.showwarning("알림", "메시지를 입력하세요.")
        if not messagebox.askyesno("전송", f"{len(names)}명에게 보내시겠습니까?"): return

        self.sending = True
        self.t1_send_btn.configure(state="disabled")
        self.t1_stop_btn.configure(state="normal", bg="#FF5252", fg="white")
        threading.Thread(target=self._send_pyauto, args=(names, msg, float(delay_var.get())),
                         daemon=True).start()

    def _send_pyauto(self, names, msg, delay):
        self.root.after(0, lambda: self.log(f"[이름검색] {len(names)}명 발송 시작"))
        kw = activate_kakao_pyauto()
        if not kw:
            self.root.after(0, lambda: self.log("[ERROR] 카카오톡 창 없음"))
            self.root.after(0, self.on_stop); return

        ok, fail = 0, 0
        for i, n in enumerate(names, 1):
            if not self.sending: break
            tag = "단톡" if self.contact_types.get(n) == "group" else "개인"
            self.root.after(0, lambda i=i, n=n, t=tag: (
                self.status_var.set(f"[{i}/{len(names)}] [{t}] {n}"),
                self.log(f"[{i}/{len(names)}] [{t}] {n}")
            ))
            if pyauto_send(kw, n, msg):
                ok += 1; self.root.after(0, lambda n=n: self.log(f"  -> {n}: OK"))
            else:
                fail += 1; self.root.after(0, lambda n=n: self.log(f"  -> {n}: FAIL"))
            if i < len(names): time.sleep(delay)

        self.root.after(0, lambda: self.log(f"[완료] 성공 {ok} / 실패 {fail}"))
        self.root.after(0, lambda: self.status_var.set(f"완료 - 성공: {ok} / 실패: {fail}"))
        self.save_log({"mode": "pyauto", "success": ok, "fail": fail,
                       "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.root.after(0, self.on_stop)

    def on_send_tab2(self, delay_var):
        sel = [(t, d) for t, d in self.room_data.items() if self.room_vars.get(t, tk.BooleanVar()).get()]
        msg = self.t2_msg.get("1.0", "end").strip()
        if not sel: return messagebox.showwarning("알림", "채팅방을 선택하세요. '새로고침'으로 감지합니다.")
        if not msg: return messagebox.showwarning("알림", "메시지를 입력하세요.")
        rpt = int(self.t2_repeat.get())
        if not messagebox.askyesno("전송", f"{len(sel)}방 x {rpt}회 전송?"): return

        self.sending = True
        self.t2_send_btn.configure(state="disabled")
        self.t2_stop_btn.configure(state="normal", bg="#FF5252", fg="white")
        threading.Thread(target=self._send_win32, args=(sel, msg, rpt, float(delay_var.get())),
                         daemon=True).start()

    def _send_win32(self, sel, msg, repeat, delay):
        total = len(sel) * repeat
        self.root.after(0, lambda: self.log(f"[Win32] {len(sel)}방 x {repeat}회 발송 시작"))
        ok, fail, cnt = 0, 0, 0
        for r in range(repeat):
            for title, data in sel:
                if not self.sending: break
                cnt += 1
                self.root.after(0, lambda c=cnt, t=title, rn=r+1: (
                    self.status_var.set(f"[{c}/{total}] {t} (#{rn})"),
                    self.log(f"[{c}/{total}] {t} (#{rn})")
                ))
                if win32_send(data["hwnd"], data["child"], msg):
                    ok += 1; self.root.after(0, lambda t=title: self.log(f"  -> {t}: OK"))
                else:
                    fail += 1; self.root.after(0, lambda t=title: self.log(f"  -> {t}: FAIL"))
                time.sleep(delay)

        self.root.after(0, lambda: self.log(f"[완료] 성공 {ok} / 실패 {fail}"))
        self.root.after(0, lambda: self.status_var.set(f"완료 - 성공: {ok} / 실패: {fail}"))
        self.save_log({"mode": "win32", "success": ok, "fail": fail,
                       "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.root.after(0, self.on_stop)

    # ─── 예약 발송 ──────────────────────────
    def on_schedule(self):
        msg = self.t3_msg.get("1.0", "end").strip()
        if not msg:
            return messagebox.showwarning("알림", "메시지를 입력하세요.")

        now = datetime.now()
        if self.t3_mode.get() == "after":
            mins = int(self.t3_min.get())
            target_time = now + timedelta(minutes=mins)
        else:
            h, m = int(self.t3_hour.get()), int(self.t3_minute.get())
            target_time = now.replace(hour=h, minute=m, second=0)
            if target_time <= now:
                target_time += timedelta(days=1)

        wait_sec = (target_time - now).total_seconds()
        method = self.t3_method.get()
        time_str = target_time.strftime("%H:%M:%S")

        self.log(f"[예약] {time_str}에 전송 예약됨 ({method})")
        self.t3_schedule_btn.configure(state="disabled")
        self.t3_cancel_btn.configure(state="normal", bg="#FF5252", fg="white")

        self.scheduled_active = True

        def countdown():
            remaining = (target_time - datetime.now()).total_seconds()
            if not self.scheduled_active:
                return
            if remaining <= 0:
                self.root.after(0, lambda: self.t3_timer_label.configure(text="전송 중..."))
                self.root.after(0, lambda: self.execute_scheduled(method, msg))
                return
            mins, secs = divmod(int(remaining), 60)
            hrs, mins = divmod(mins, 60)
            self.root.after(0, lambda: self.t3_timer_label.configure(
                text=f"전송까지 {hrs:02d}:{mins:02d}:{secs:02d}"))
            self.root.after(1000, countdown)

        self.root.after(100, countdown)

    def on_cancel_schedule(self):
        self.scheduled_active = False
        self.t3_timer_label.configure(text="예약 취소됨")
        self.t3_schedule_btn.configure(state="normal")
        self.t3_cancel_btn.configure(state="disabled", bg="#E0E0E0", fg="#555")
        self.log("[예약] 취소됨")

    def execute_scheduled(self, method, msg):
        self.t3_schedule_btn.configure(state="normal")
        self.t3_cancel_btn.configure(state="disabled", bg="#E0E0E0", fg="#555")
        self.sending = True

        if method == "pyauto":
            names = [n for n, v in self.contact_vars.items() if v.get()]
            if not names:
                self.log("[예약] 탭1에서 선택된 대상이 없습니다"); return
            threading.Thread(target=self._send_pyauto, args=(names, msg, 1.5), daemon=True).start()
        else:
            sel = [(t, d) for t, d in self.room_data.items() if self.room_vars.get(t, tk.BooleanVar()).get()]
            if not sel:
                self.log("[예약] 탭2에서 선택된 채팅방이 없습니다"); return
            threading.Thread(target=self._send_win32, args=(sel, msg, 1, 1.0), daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = KakaoUltimateGUI()
    app.run()
