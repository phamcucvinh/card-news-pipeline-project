#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""카카오톡 PC앱 다중 메시지 발송기 - GUI 버전 (개인+단톡방 체크박스)"""

import subprocess
import time
import sys
import json
import threading
import os
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, filedialog
except ImportError:
    print("tkinter를 찾을 수 없습니다.")
    sys.exit(1)

try:
    import pyautogui
    import pyperclip
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip"])
    import pyautogui
    import pyperclip


KAKAO_EXE = r"C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(SCRIPT_DIR, "kakao_contacts.json")


class KakaoSenderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("카카오톡 다중 발송기")
        self.root.geometry("640x900")
        self.root.resizable(False, False)
        self.root.configure(bg="#FEE500")
        self.sending = False
        self.contact_vars = {}    # {name: BooleanVar}
        self.contact_widgets = {} # {name: Frame}
        self.contact_types = {}   # {name: "person"|"group"}
        self.saved_data = self.load_contacts()
        self.current_filter = "all"  # all, person, group
        self.build_ui()

    # ─── 연락처 저장/로드 ────────────────────────────
    def load_contacts(self):
        """Load contacts: [{name, type}] or legacy [name]"""
        try:
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # legacy format: list of strings
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
        self.saved_data = data

    # ─── UI 빌드 ─────────────────────────────────────
    def build_ui(self):
        # 헤더
        header = tk.Frame(self.root, bg="#FEE500", pady=8)
        header.pack(fill="x")
        tk.Label(header, text="카카오톡 다중 발송기", font=("맑은 고딕", 18, "bold"),
                 bg="#FEE500", fg="#3C1E1E").pack()
        tk.Label(header, text="개인 + 단톡방 동시 발송", font=("맑은 고딕", 9),
                 bg="#FEE500", fg="#5D4037").pack()

        # 메인
        main = tk.Frame(self.root, bg="white", padx=15, pady=10)
        main.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # ─── 받는 사람 탭 ───
        tk.Label(main, text="받는 사람", font=("맑은 고딕", 11, "bold"),
                 bg="white").pack(fill="x", anchor="w")

        # 필터 버튼 (전체/개인/단톡방)
        filter_frame = tk.Frame(main, bg="white")
        filter_frame.pack(fill="x", pady=(3, 0))

        self.filter_btns = {}
        for label, key, color in [("전체", "all", "#E0E0E0"),
                                   ("개인", "person", "#BBDEFB"),
                                   ("단톡방", "group", "#C8E6C9")]:
            btn = tk.Button(filter_frame, text=label, font=("맑은 고딕", 9),
                            bg=color, relief="flat", padx=10, pady=2,
                            command=lambda k=key: self.set_filter(k))
            btn.pack(side="left", padx=(0, 3))
            self.filter_btns[key] = btn

        self.selected_label = tk.Label(filter_frame, text="선택: 0명",
                                        font=("맑은 고딕", 9, "bold"),
                                        bg="white", fg="#1976D2")
        self.selected_label.pack(side="right")

        # 버튼 줄
        btn_row = tk.Frame(main, bg="white")
        btn_row.pack(fill="x", pady=(3, 0))

        tk.Button(btn_row, text="전체선택", font=("맑은 고딕", 8),
                  bg="#E8F5E9", relief="flat", padx=6, pady=1,
                  command=self.select_all).pack(side="left", padx=(0, 2))
        tk.Button(btn_row, text="전체해제", font=("맑은 고딕", 8),
                  bg="#FFEBEE", relief="flat", padx=6, pady=1,
                  command=self.deselect_all).pack(side="left", padx=(0, 2))
        tk.Button(btn_row, text="선택삭제", font=("맑은 고딕", 8),
                  bg="#FFF3E0", relief="flat", padx=6, pady=1,
                  command=self.delete_selected).pack(side="left", padx=(0, 2))
        tk.Button(btn_row, text="TXT 불러오기", font=("맑은 고딕", 8),
                  bg="#E3F2FD", relief="flat", padx=6, pady=1,
                  command=self.on_load_txt).pack(side="left", padx=(0, 2))
        tk.Button(btn_row, text="목록저장", font=("맑은 고딕", 8),
                  bg="#F3E5F5", relief="flat", padx=6, pady=1,
                  command=self.save_contacts).pack(side="left")

        # 검색
        search_frame = tk.Frame(main, bg="white")
        search_frame.pack(fill="x", pady=(3, 3))
        tk.Label(search_frame, text="검색:", font=("맑은 고딕", 9), bg="white").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.apply_filter)
        tk.Entry(search_frame, textvariable=self.search_var, font=("맑은 고딕", 10),
                 relief="solid", borderwidth=1).pack(side="left", fill="x", expand=True, padx=(5, 0))

        # 체크박스 리스트
        list_frame = tk.Frame(main, bg="white", relief="solid", borderwidth=1)
        list_frame.pack(fill="both", expand=True, pady=(0, 5))

        self.canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg="white")

        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        # ─── 추가 영역 ───
        add_frame = tk.LabelFrame(main, text="연락처 추가", font=("맑은 고딕", 9, "bold"),
                                   bg="white", padx=8, pady=5)
        add_frame.pack(fill="x", pady=(0, 5))

        # 이름 입력
        name_row = tk.Frame(add_frame, bg="white")
        name_row.pack(fill="x", pady=(0, 3))
        tk.Label(name_row, text="이름:", font=("맑은 고딕", 9), bg="white", width=6,
                 anchor="w").pack(side="left")
        self.add_entry = tk.Entry(name_row, font=("맑은 고딕", 10), relief="solid", borderwidth=1)
        self.add_entry.pack(side="left", fill="x", expand=True)
        self.add_entry.bind("<Return>", lambda e: self.on_add())

        # 타입 선택 + 추가 버튼
        type_row = tk.Frame(add_frame, bg="white")
        type_row.pack(fill="x")
        tk.Label(type_row, text="유형:", font=("맑은 고딕", 9), bg="white", width=6,
                 anchor="w").pack(side="left")
        self.type_var = tk.StringVar(value="person")
        tk.Radiobutton(type_row, text="개인", variable=self.type_var, value="person",
                        font=("맑은 고딕", 9), bg="white").pack(side="left")
        tk.Radiobutton(type_row, text="단톡방", variable=self.type_var, value="group",
                        font=("맑은 고딕", 9), bg="white").pack(side="left", padx=(5, 0))

        tk.Button(type_row, text="추가", font=("맑은 고딕", 9, "bold"),
                  bg="#FEE500", fg="#3C1E1E", relief="flat", padx=12,
                  command=self.on_add).pack(side="right")

        # 저장된 연락처 표시
        for item in self.saved_data:
            name = item["name"] if isinstance(item, dict) else item
            ctype = item.get("type", "person") if isinstance(item, dict) else "person"
            self.add_contact(name, ctype, checked=False)

        # ─── 메시지 ───
        tk.Label(main, text="메시지 내용", font=("맑은 고딕", 11, "bold"),
                 bg="white", anchor="w").pack(fill="x", pady=(0, 2))

        self.message_text = scrolledtext.ScrolledText(
            main, height=4, font=("맑은 고딕", 11), wrap="word",
            relief="solid", borderwidth=1)
        self.message_text.pack(fill="x", pady=(0, 5))
        self.message_text.insert("1.0", "안녕하세요, 테스트 메시지입니다")

        # ─── 옵션 + 전송 ───
        ctrl_frame = tk.Frame(main, bg="white")
        ctrl_frame.pack(fill="x", pady=(0, 5))

        tk.Label(ctrl_frame, text="간격(초):", font=("맑은 고딕", 10),
                 bg="white").pack(side="left")
        self.delay_var = tk.StringVar(value="1.5")
        ttk.Spinbox(ctrl_frame, from_=0.5, to=10, increment=0.5,
                     textvariable=self.delay_var, width=5,
                     font=("맑은 고딕", 10)).pack(side="left", padx=(3, 10))

        self.send_btn = tk.Button(
            ctrl_frame, text="전송 시작", font=("맑은 고딕", 12, "bold"),
            bg="#FEE500", fg="#3C1E1E", relief="flat", padx=15, pady=4,
            cursor="hand2", command=self.on_send)
        self.send_btn.pack(side="left", padx=(0, 5))

        self.stop_btn = tk.Button(
            ctrl_frame, text="중지", font=("맑은 고딕", 12, "bold"),
            bg="#E0E0E0", fg="#555", relief="flat", padx=15, pady=4,
            state="disabled", command=self.on_stop)
        self.stop_btn.pack(side="left")

        # ─── 로그 ───
        tk.Label(main, text="전송 로그", font=("맑은 고딕", 10, "bold"),
                 bg="white", anchor="w").pack(fill="x", pady=(3, 2))

        self.log_text = scrolledtext.ScrolledText(
            main, height=5, font=("Consolas", 9), wrap="word",
            relief="solid", borderwidth=1, state="disabled", bg="#F5F5F5")
        self.log_text.pack(fill="x")

        # 상태바
        self.status_var = tk.StringVar(value="대기 중")
        tk.Label(self.root, textvariable=self.status_var, font=("맑은 고딕", 9),
                 bg="#E0E0E0", anchor="w", padx=10, pady=3).pack(fill="x", side="bottom")

        # 초기 필터 표시
        self.set_filter("all")

    # ─── 연락처 체크박스 ─────────────────────────────
    def add_contact(self, name, ctype="person", checked=False):
        if name in self.contact_vars:
            return

        var = tk.BooleanVar(value=checked)
        var.trace_add("write", lambda *a: self.update_count())

        self.contact_types[name] = ctype
        self.contact_vars[name] = var

        row = tk.Frame(self.inner, bg="white")

        # 타입 배지
        badge_text = "단톡" if ctype == "group" else "개인"
        badge_bg = "#C8E6C9" if ctype == "group" else "#BBDEFB"
        badge = tk.Label(row, text=badge_text, font=("맑은 고딕", 8),
                         bg=badge_bg, fg="#333", padx=4, pady=0)
        badge.pack(side="left", padx=(3, 5))

        cb = tk.Checkbutton(row, text=name, variable=var,
                            font=("맑은 고딕", 10), bg="white",
                            activebackground="#FFF9C4", anchor="w")
        cb.pack(side="left", fill="x", expand=True)

        row.pack(fill="x", padx=2, pady=1)
        self.contact_widgets[name] = row

    def update_count(self):
        count = sum(1 for v in self.contact_vars.values() if v.get())
        persons = sum(1 for n, v in self.contact_vars.items()
                      if v.get() and self.contact_types.get(n) == "person")
        groups = sum(1 for n, v in self.contact_vars.items()
                     if v.get() and self.contact_types.get(n) == "group")
        parts = []
        if persons:
            parts.append(f"개인 {persons}")
        if groups:
            parts.append(f"단톡 {groups}")
        detail = f" ({', '.join(parts)})" if parts else ""
        self.selected_label.configure(text=f"선택: {count}명{detail}")

    def set_filter(self, key):
        self.current_filter = key
        for k, btn in self.filter_btns.items():
            if k == key:
                btn.configure(relief="sunken", font=("맑은 고딕", 9, "bold"))
            else:
                btn.configure(relief="flat", font=("맑은 고딕", 9))
        self.apply_filter()

    def apply_filter(self, *args):
        keyword = self.search_var.get().strip().lower()
        for name, widget in self.contact_widgets.items():
            ctype = self.contact_types.get(name, "person")
            match_filter = (self.current_filter == "all" or ctype == self.current_filter)
            match_search = (keyword == "" or keyword in name.lower())
            if match_filter and match_search:
                widget.pack(fill="x", padx=2, pady=1)
            else:
                widget.pack_forget()

    def select_all(self):
        for name, v in self.contact_vars.items():
            ctype = self.contact_types.get(name, "person")
            if self.current_filter == "all" or ctype == self.current_filter:
                v.set(True)

    def deselect_all(self):
        for v in self.contact_vars.values():
            v.set(False)

    def delete_selected(self):
        to_del = [n for n, v in self.contact_vars.items() if v.get()]
        if not to_del:
            return
        for name in to_del:
            self.contact_widgets[name].destroy()
            del self.contact_vars[name]
            del self.contact_widgets[name]
            del self.contact_types[name]
        self.update_count()
        self.save_contacts()

    def on_add(self):
        raw = self.add_entry.get().strip()
        if not raw:
            return
        ctype = self.type_var.get()
        names = [n.strip() for n in raw.replace("\n", ",").split(",") if n.strip()]
        for name in names:
            self.add_contact(name, ctype, checked=True)
        self.save_contacts()
        self.add_entry.delete(0, "end")
        self.update_count()
        self.apply_filter()

    def on_load_txt(self):
        filepath = filedialog.askopenfilename(
            title="연락처 파일 선택",
            filetypes=[("텍스트", "*.txt"), ("CSV", "*.csv"), ("모든 파일", "*.*")])
        if not filepath:
            return

        # 타입 선택 팝업
        popup = tk.Toplevel(self.root)
        popup.title("유형 선택")
        popup.geometry("300x120")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg="white")

        tk.Label(popup, text="파일의 연락처 유형을 선택하세요:",
                 font=("맑은 고딕", 10), bg="white").pack(pady=(15, 5))
        btn_f = tk.Frame(popup, bg="white")
        btn_f.pack()

        def load_as(ctype):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    names = [line.strip() for line in f if line.strip()]
                for name in names:
                    self.add_contact(name, ctype, checked=False)
                self.save_contacts()
                self.apply_filter()
                self.log(f"[{ctype}] {len(names)}명 불러옴")
            except Exception as e:
                messagebox.showerror("오류", str(e))
            popup.destroy()

        tk.Button(btn_f, text="개인", font=("맑은 고딕", 11, "bold"),
                  bg="#BBDEFB", relief="flat", padx=20, pady=5,
                  command=lambda: load_as("person")).pack(side="left", padx=5)
        tk.Button(btn_f, text="단톡방", font=("맑은 고딕", 11, "bold"),
                  bg="#C8E6C9", relief="flat", padx=20, pady=5,
                  command=lambda: load_as("group")).pack(side="left", padx=5)

    # ─── 로그 ────────────────────────────────────────
    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ─── 전송 ────────────────────────────────────────
    def get_selected(self):
        return [n for n, v in self.contact_vars.items() if v.get()]

    def on_send(self):
        recipients = self.get_selected()
        message = self.message_text.get("1.0", "end").strip()

        if not recipients:
            messagebox.showwarning("알림", "받는 사람을 선택하세요.")
            return
        if not message:
            messagebox.showwarning("알림", "메시지를 입력하세요.")
            return

        persons = [n for n in recipients if self.contact_types.get(n) == "person"]
        groups = [n for n in recipients if self.contact_types.get(n) == "group"]

        detail_lines = []
        if persons:
            detail_lines.append(f"  개인({len(persons)}): {', '.join(persons[:3])}{'...' if len(persons)>3 else ''}")
        if groups:
            detail_lines.append(f"  단톡({len(groups)}): {', '.join(groups[:3])}{'...' if len(groups)>3 else ''}")

        if not messagebox.askyesno("전송 확인",
                f"총 {len(recipients)}명에게 메시지를 보냅니다.\n\n"
                + "\n".join(detail_lines) + "\n\n"
                f"메시지: {message[:80]}{'...' if len(message)>80 else ''}\n\n"
                f"전송하시겠습니까?"):
            return

        self.sending = True
        self.send_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal", bg="#FF5252", fg="white")
        threading.Thread(target=self.send_thread,
                         args=(recipients, message), daemon=True).start()

    def on_stop(self):
        self.sending = False
        self.log("중지됨")
        self.status_var.set("중지됨")
        self.send_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled", bg="#E0E0E0", fg="#555")

    def send_thread(self, recipients, message):
        delay = float(self.delay_var.get())
        self.root.after(0, lambda: self.log(f"=== 발송 시작: {len(recipients)}명 ==="))

        kakao_win = self.activate_kakao()
        if not kakao_win:
            self.root.after(0, lambda: self.log("[ERROR] 카카오톡 창 없음"))
            self.root.after(0, self.on_stop)
            return

        success, fail = 0, 0
        for i, name in enumerate(recipients, 1):
            if not self.sending:
                break

            ctype = self.contact_types.get(name, "person")
            tag = "단톡" if ctype == "group" else "개인"
            total = len(recipients)
            self.root.after(0, lambda idx=i, nm=name, t=tag: (
                self.status_var.set(f"[{idx}/{total}] [{t}] {nm}"),
                self.log(f"[{idx}/{total}] [{t}] {nm}")
            ))

            if self.send_to_one(kakao_win, name, message):
                success += 1
                self.root.after(0, lambda nm=name: self.log(f"  -> {nm}: OK"))
            else:
                fail += 1
                self.root.after(0, lambda nm=name: self.log(f"  -> {nm}: FAIL"))

            if i < total and self.sending:
                time.sleep(delay)

        s, f = success, fail
        self.root.after(0, lambda: self.log(f"=== 완료: 성공 {s} / 실패 {f} ==="))
        self.root.after(0, lambda: self.status_var.set(f"완료 - 성공: {s} / 실패: {f}"))

        log_data = {"success": s, "fail": f,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "recipients": [{"name": n, "type": self.contact_types.get(n, "person")}
                                   for n in recipients]}
        log_path = os.path.join(SCRIPT_DIR, "kakao_send_log.json")
        with open(log_path, "w", encoding="utf-8") as fp:
            json.dump(log_data, fp, ensure_ascii=False, indent=2)

        self.root.after(0, lambda: self.send_btn.configure(state="normal"))
        self.root.after(0, lambda: self.stop_btn.configure(state="disabled", bg="#E0E0E0", fg="#555"))
        self.sending = False

    def activate_kakao(self):
        subprocess.Popen([KAKAO_EXE])
        time.sleep(3)
        wins = pyautogui.getWindowsWithTitle("\uce74\uce74\uc624\ud1a1")
        if not wins:
            wins = pyautogui.getWindowsWithTitle("KakaoTalk")
        if not wins:
            return None
        win = wins[0]
        win.activate()
        time.sleep(1)
        return win

    def send_to_one(self, kakao_win, chat_name, message):
        try:
            kakao_win.activate()
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "f")
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.2)
            pyperclip.copy(chat_name)
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

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = KakaoSenderGUI()
    app.run()
