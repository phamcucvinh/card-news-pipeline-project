#!/usr/bin/env python3
"""칼라 계산기 - HEX, RGB, HSL 변환 및 색상 미리보기"""

import tkinter as tk
from tkinter import ttk, colorchooser
import colorsys
import re


class ColorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("칼라 계산기")
        self.root.geometry("520x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        self.updating = False

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("맑은 고딕", 11))
        style.configure("TButton", font=("맑은 고딕", 10))
        style.configure("Header.TLabel", font=("맑은 고딕", 16, "bold"), foreground="#61dafb")

        self._build_ui()
        self._set_color_from_hex("3498DB")

    def _build_ui(self):
        # 제목
        ttk.Label(self.root, text="🎨 칼라 계산기", style="Header.TLabel").pack(pady=(15, 10))

        # 색상 미리보기
        self.preview_frame = tk.Frame(self.root, width=480, height=100, bg="#3498DB",
                                      highlightbackground="#555", highlightthickness=2)
        self.preview_frame.pack(padx=20, pady=(0, 10))
        self.preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_frame, text="#3498DB", font=("Consolas", 20, "bold"),
                                      bg="#3498DB", fg="#ffffff")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # 색상 선택 버튼
        pick_btn = tk.Button(self.root, text="🖱 색상 선택기 열기", font=("맑은 고딕", 11),
                             bg="#444", fg="#fff", activebackground="#555", activeforeground="#fff",
                             relief="flat", padx=15, pady=5, command=self._pick_color)
        pick_btn.pack(pady=(0, 15))

        # 입력 영역
        input_frame = tk.Frame(self.root, bg="#2b2b2b")
        input_frame.pack(padx=20, fill="x")

        # HEX
        self._make_row(input_frame, 0, "HEX", "#")
        self.hex_entry = tk.Entry(input_frame, font=("Consolas", 14), width=20, bg="#3c3c3c",
                                  fg="#fff", insertbackground="#fff", relief="flat")
        self.hex_entry.grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.hex_entry.bind("<KeyRelease>", self._on_hex_change)

        # RGB
        self._make_row(input_frame, 1, "R", "")
        self.r_var = tk.IntVar(value=0)
        self.g_var = tk.IntVar(value=0)
        self.b_var = tk.IntVar(value=0)

        rgb_frame = tk.Frame(input_frame, bg="#2b2b2b")
        rgb_frame.grid(row=1, column=2, padx=5, pady=8, sticky="w")

        for i, (label, var) in enumerate([("R", self.r_var), ("G", self.g_var), ("B", self.b_var)]):
            tk.Label(rgb_frame, text=label, font=("맑은 고딕", 10), bg="#2b2b2b",
                     fg={"R": "#ff6b6b", "G": "#51cf66", "B": "#339af0"}[label]).grid(row=0, column=i*2)
            entry = tk.Entry(rgb_frame, textvariable=var, font=("Consolas", 14), width=4,
                             bg="#3c3c3c", fg="#fff", insertbackground="#fff", relief="flat", justify="center")
            entry.grid(row=0, column=i*2+1, padx=(2, 8))
            entry.bind("<KeyRelease>", self._on_rgb_change)

        input_frame.grid_columnconfigure(0, minsize=60)
        # 첫 번째 행 라벨 수정
        for widget in input_frame.grid_slaves(row=1, column=0):
            widget.destroy()
        for widget in input_frame.grid_slaves(row=1, column=1):
            widget.destroy()
        ttk.Label(input_frame, text="RGB").grid(row=1, column=0, sticky="e", padx=(0, 5))

        # HSL
        self._make_row(input_frame, 2, "HSL", "")
        self.h_var = tk.IntVar(value=0)
        self.s_var = tk.IntVar(value=0)
        self.l_var = tk.IntVar(value=0)

        hsl_frame = tk.Frame(input_frame, bg="#2b2b2b")
        hsl_frame.grid(row=2, column=2, padx=5, pady=8, sticky="w")

        for i, (label, var, unit) in enumerate([("H", self.h_var, "°"), ("S", self.s_var, "%"), ("L", self.l_var, "%")]):
            tk.Label(hsl_frame, text=label, font=("맑은 고딕", 10), bg="#2b2b2b", fg="#aaa").grid(row=0, column=i*3)
            entry = tk.Entry(hsl_frame, textvariable=var, font=("Consolas", 14), width=4,
                             bg="#3c3c3c", fg="#fff", insertbackground="#fff", relief="flat", justify="center")
            entry.grid(row=0, column=i*3+1, padx=2)
            entry.bind("<KeyRelease>", self._on_hsl_change)
            tk.Label(hsl_frame, text=unit, font=("맑은 고딕", 9), bg="#2b2b2b", fg="#888").grid(row=0, column=i*3+2, padx=(0, 5))

        for widget in input_frame.grid_slaves(row=2, column=0):
            widget.destroy()
        for widget in input_frame.grid_slaves(row=2, column=1):
            widget.destroy()
        ttk.Label(input_frame, text="HSL").grid(row=2, column=0, sticky="e", padx=(0, 5))

        # 슬라이더 영역
        slider_frame = tk.Frame(self.root, bg="#2b2b2b")
        slider_frame.pack(padx=20, pady=(15, 5), fill="x")

        ttk.Label(slider_frame, text="R").grid(row=0, column=0, padx=(0, 5))
        self.r_slider = tk.Scale(slider_frame, from_=0, to=255, orient="horizontal", length=400,
                                  bg="#2b2b2b", fg="#ff6b6b", troughcolor="#3c3c3c", highlightthickness=0,
                                  showvalue=False, command=lambda v: self._on_slider_change())
        self.r_slider.grid(row=0, column=1, pady=2)

        ttk.Label(slider_frame, text="G").grid(row=1, column=0, padx=(0, 5))
        self.g_slider = tk.Scale(slider_frame, from_=0, to=255, orient="horizontal", length=400,
                                  bg="#2b2b2b", fg="#51cf66", troughcolor="#3c3c3c", highlightthickness=0,
                                  showvalue=False, command=lambda v: self._on_slider_change())
        self.g_slider.grid(row=1, column=1, pady=2)

        ttk.Label(slider_frame, text="B").grid(row=2, column=0, padx=(0, 5))
        self.b_slider = tk.Scale(slider_frame, from_=0, to=255, orient="horizontal", length=400,
                                  bg="#2b2b2b", fg="#339af0", troughcolor="#3c3c3c", highlightthickness=0,
                                  showvalue=False, command=lambda v: self._on_slider_change())
        self.b_slider.grid(row=2, column=1, pady=2)

        # 복사 버튼들
        copy_frame = tk.Frame(self.root, bg="#2b2b2b")
        copy_frame.pack(pady=(15, 10))

        for text, cmd in [("HEX 복사", self._copy_hex), ("RGB 복사", self._copy_rgb),
                          ("HSL 복사", self._copy_hsl)]:
            btn = tk.Button(copy_frame, text=text, font=("맑은 고딕", 10),
                            bg="#444", fg="#fff", activebackground="#555", activeforeground="#fff",
                            relief="flat", padx=12, pady=4, command=cmd)
            btn.pack(side="left", padx=5)

        # 상태 표시
        self.status_label = tk.Label(self.root, text="", font=("맑은 고딕", 9),
                                      bg="#2b2b2b", fg="#888")
        self.status_label.pack()

    def _make_row(self, parent, row, label, prefix):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=(0, 5))
        if prefix:
            tk.Label(parent, text=prefix, font=("Consolas", 14), bg="#2b2b2b", fg="#888").grid(row=row, column=1)

    def _set_color_from_hex(self, hex_str):
        hex_str = hex_str.lstrip("#")
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        if len(hex_str) != 6 or not re.match(r'^[0-9a-fA-F]{6}$', hex_str):
            return
        self.updating = True
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        self._update_all(r, g, b, source="hex")
        self.updating = False

    def _update_all(self, r, g, b, source=""):
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        hex_str = f"{r:02X}{g:02X}{b:02X}"

        h_norm, l_norm, s_norm = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        h = int(h_norm * 360)
        s = int(s_norm * 100)
        l = int(l_norm * 100)

        if source != "hex":
            self.hex_entry.delete(0, tk.END)
            self.hex_entry.insert(0, hex_str)

        if source != "rgb":
            self.r_var.set(r)
            self.g_var.set(g)
            self.b_var.set(b)

        if source != "hsl":
            self.h_var.set(h)
            self.s_var.set(s)
            self.l_var.set(l)

        if source != "slider":
            self.r_slider.set(r)
            self.g_slider.set(g)
            self.b_slider.set(b)

        color = f"#{hex_str}"
        self.preview_frame.configure(bg=color)

        # 텍스트 색상 자동 조절 (밝기 기반)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = "#000000" if brightness > 128 else "#ffffff"
        self.preview_label.configure(bg=color, fg=text_color, text=color)

    def _on_hex_change(self, event=None):
        if self.updating:
            return
        self.updating = True
        val = self.hex_entry.get().strip().lstrip("#")
        if len(val) == 3:
            val = "".join(c * 2 for c in val)
        if len(val) == 6 and re.match(r'^[0-9a-fA-F]{6}$', val):
            r = int(val[0:2], 16)
            g = int(val[2:4], 16)
            b = int(val[4:6], 16)
            self._update_all(r, g, b, source="hex")
        self.updating = False

    def _on_rgb_change(self, event=None):
        if self.updating:
            return
        self.updating = True
        try:
            r = max(0, min(255, self.r_var.get()))
            g = max(0, min(255, self.g_var.get()))
            b = max(0, min(255, self.b_var.get()))
            self._update_all(r, g, b, source="rgb")
        except (tk.TclError, ValueError):
            pass
        self.updating = False

    def _on_hsl_change(self, event=None):
        if self.updating:
            return
        self.updating = True
        try:
            h = max(0, min(360, self.h_var.get()))
            s = max(0, min(100, self.s_var.get()))
            l = max(0, min(100, self.l_var.get()))
            r_f, g_f, b_f = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
            r, g, b = int(r_f * 255), int(g_f * 255), int(b_f * 255)
            self._update_all(r, g, b, source="hsl")
        except (tk.TclError, ValueError):
            pass
        self.updating = False

    def _on_slider_change(self):
        if self.updating:
            return
        self.updating = True
        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()
        self._update_all(r, g, b, source="slider")
        self.updating = False

    def _pick_color(self):
        color = colorchooser.askcolor(title="색상 선택")
        if color and color[1]:
            self._set_color_from_hex(color[1])

    def _copy_hex(self):
        val = f"#{self.hex_entry.get().upper()}"
        self.root.clipboard_clear()
        self.root.clipboard_append(val)
        self._show_status(f"복사됨: {val}")

    def _copy_rgb(self):
        val = f"rgb({self.r_var.get()}, {self.g_var.get()}, {self.b_var.get()})"
        self.root.clipboard_clear()
        self.root.clipboard_append(val)
        self._show_status(f"복사됨: {val}")

    def _copy_hsl(self):
        val = f"hsl({self.h_var.get()}, {self.s_var.get()}%, {self.l_var.get()}%)"
        self.root.clipboard_clear()
        self.root.clipboard_append(val)
        self._show_status(f"복사됨: {val}")

    def _show_status(self, msg):
        self.status_label.configure(text=msg)
        self.root.after(2000, lambda: self.status_label.configure(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorCalculator(root)
    root.mainloop()
