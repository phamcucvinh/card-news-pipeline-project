#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
from phone_data_manager import PhoneDataManager
from kakao_automation import KakaoTalkAutomation

class KakaoContactManagerGUI:
    """카카오톡 연락처 관리 GUI 애플리케이션"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("카카오톡 연락처 자동 추가 도구")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 데이터 관리자 인스턴스
        self.phone_manager = PhoneDataManager()
        self.kakao_automation = None
        
        # 스레드 통신용 큐
        self.log_queue = queue.Queue()
        
        # GUI 컴포넌트 초기화
        self.setup_gui()
        
        # 로그 큐 모니터링 시작
        self.check_log_queue()
    
    def setup_gui(self):
        """GUI 컴포넌트 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 선택 섹션
        self.setup_file_section(main_frame)
        
        # 데이터 정보 섹션
        self.setup_data_info_section(main_frame)
        
        # 설정 섹션
        self.setup_settings_section(main_frame)
        
        # 제어 버튼 섹션
        self.setup_control_section(main_frame)
        
        # 진행 상황 섹션
        self.setup_progress_section(main_frame)
        
        # 로그 섹션
        self.setup_log_section(main_frame)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def setup_file_section(self, parent):
        """파일 선택 섹션"""
        file_frame = ttk.LabelFrame(parent, text="1. 엑셀 파일 선택", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=60).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="파일 선택", command=self.select_file).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="데이터 로드", command=self.load_data).grid(row=0, column=2, padx=5)
    
    def setup_data_info_section(self, parent):
        """데이터 정보 섹션"""
        info_frame = ttk.LabelFrame(parent, text="2. 데이터 정보", padding="5")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 데이터 통계 라벨들
        self.total_records_var = tk.StringVar(value="총 레코드: -")
        self.valid_phones_var = tk.StringVar(value="유효한 전화번호: -")
        self.regions_var = tk.StringVar(value="지역 수: -")
        
        ttk.Label(info_frame, textvariable=self.total_records_var).grid(row=0, column=0, padx=10, sticky=tk.W)
        ttk.Label(info_frame, textvariable=self.valid_phones_var).grid(row=0, column=1, padx=10, sticky=tk.W)
        ttk.Label(info_frame, textvariable=self.regions_var).grid(row=0, column=2, padx=10, sticky=tk.W)
    
    def setup_settings_section(self, parent):
        """설정 섹션"""
        settings_frame = ttk.LabelFrame(parent, text="3. 자동화 설정", padding="5")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 배치 크기 설정
        ttk.Label(settings_frame, text="배치 크기:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.batch_size_var = tk.StringVar(value="10")
        ttk.Entry(settings_frame, textvariable=self.batch_size_var, width=10).grid(row=0, column=1, padx=5)
        
        # 지연 시간 설정
        ttk.Label(settings_frame, text="지연 시간(초):").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.delay_var = tk.StringVar(value="2")
        ttk.Entry(settings_frame, textvariable=self.delay_var, width=10).grid(row=0, column=3, padx=5)
        
        # 처리할 최대 개수
        ttk.Label(settings_frame, text="최대 처리 개수:").grid(row=1, column=0, padx=5, sticky=tk.W)
        self.max_count_var = tk.StringVar(value="1000")
        ttk.Entry(settings_frame, textvariable=self.max_count_var, width=10).grid(row=1, column=1, padx=5)
        
        # 헤드리스 모드
        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="헤드리스 모드", variable=self.headless_var).grid(row=1, column=2, padx=5, sticky=tk.W)
    
    def setup_control_section(self, parent):
        """제어 버튼 섹션"""
        control_frame = ttk.LabelFrame(parent, text="4. 실행 제어", padding="5")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.start_button = ttk.Button(control_frame, text="카카오톡 자동화 시작", command=self.start_automation)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="중지", command=self.stop_automation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="테스트 (5개만)", command=self.test_automation).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="데이터 내보내기", command=self.export_data).grid(row=0, column=3, padx=5)
    
    def setup_progress_section(self, parent):
        """진행 상황 섹션"""
        progress_frame = ttk.LabelFrame(parent, text="5. 진행 상황", padding="5")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 진행률 표시
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # 상태 정보
        self.status_var = tk.StringVar(value="대기 중...")
        ttk.Label(progress_frame, textvariable=self.status_var).grid(row=1, column=0, sticky=tk.W, padx=5)
        
        self.stats_var = tk.StringVar(value="처리됨: 0 / 성공: 0 / 실패: 0")
        ttk.Label(progress_frame, textvariable=self.stats_var).grid(row=1, column=1, sticky=tk.E, padx=5)
        
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(1, weight=1)
    
    def setup_log_section(self, parent):
        """로그 섹션"""
        log_frame = ttk.LabelFrame(parent, text="6. 실행 로그", padding="5")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 로그 지우기 버튼
        ttk.Button(log_frame, text="로그 지우기", command=self.clear_log).grid(row=1, column=0, pady=5)
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def select_file(self):
        """파일 선택 대화상자"""
        filename = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def load_data(self):
        """데이터 로드"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("오류", "파일을 선택해주세요.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "선택한 파일이 존재하지 않습니다.")
            return
        
        try:
            self.log_message("데이터 로딩 중...")
            if self.phone_manager.load_excel_data(file_path):
                # 최대 개수 제한으로 데이터 처리
                max_count = int(self.max_count_var.get()) if self.max_count_var.get() else None
                phones = self.phone_manager.process_phone_data(limit=max_count)
                
                # 통계 정보 업데이트
                total_records = len(self.phone_manager.df) if self.phone_manager.df is not None else 0
                valid_phones = len(phones)
                regions = len(set(p['region'] for p in phones)) if phones else 0
                
                self.total_records_var.set(f"총 레코드: {total_records:,}")
                self.valid_phones_var.set(f"유효한 전화번호: {valid_phones:,}")
                self.regions_var.set(f"지역 수: {regions}")
                
                self.log_message(f"데이터 로드 완료: {valid_phones:,}개의 유효한 전화번호")
                messagebox.showinfo("성공", f"{valid_phones:,}개의 유효한 전화번호를 로드했습니다.")
            else:
                messagebox.showerror("오류", "데이터 로드에 실패했습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"데이터 로드 중 오류: {str(e)}")
    
    def start_automation(self):
        """자동화 시작"""
        if not self.phone_manager.valid_phones:
            messagebox.showerror("오류", "먼저 데이터를 로드해주세요.")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 별도 스레드에서 자동화 실행
        threading.Thread(target=self._run_automation, daemon=True).start()
    
    def test_automation(self):
        """테스트 자동화 (5개만)"""
        if not self.phone_manager.valid_phones:
            messagebox.showerror("오류", "먼저 데이터를 로드해주세요.")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 별도 스레드에서 테스트 자동화 실행
        threading.Thread(target=self._run_automation, args=(5,), daemon=True).start()
    
    def _run_automation(self, limit=None):
        """자동화 실행 (백그라운드 스레드)"""
        try:
            # 설정 값 읽기
            batch_size = int(self.batch_size_var.get())
            delay = float(self.delay_var.get())
            headless = self.headless_var.get()
            
            # 처리할 연락처 목록
            contacts = self.phone_manager.valid_phones[:limit] if limit else self.phone_manager.valid_phones
            
            self.log_queue.put(f"자동화 시작: {len(contacts)}개 연락처 처리 예정")
            
            # 카카오톡 자동화 인스턴스 생성
            self.kakao_automation = KakaoTalkAutomation(headless=headless, delay=delay)
            
            # 카카오톡 웹 열기
            if not self.kakao_automation.open_kakao_web():
                self.log_queue.put("카카오톡 웹 페이지 열기 실패")
                return
            
            # 로그인 대기
            self.log_queue.put("카카오톡 로그인을 기다리는 중... (QR코드 스캔 또는 계정 로그인)")
            if not self.kakao_automation.wait_for_login():
                self.log_queue.put("로그인 시간 초과")
                return
            
            # 연락처 배치 추가
            results = {'success': 0, 'failed': 0, 'errors': []}
            
            for i, contact in enumerate(contacts):
                # 중지 체크
                if hasattr(self, '_stop_automation') and self._stop_automation:
                    self.log_queue.put("사용자에 의해 중지됨")
                    break
                
                # 진행률 업데이트
                progress = (i / len(contacts)) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda: self.status_var.set(f"처리 중... ({i+1}/{len(contacts)})"))
                
                phone = contact.get('phone', '')
                name = contact.get('company', f"연락처{i+1}")
                
                if self.kakao_automation.add_contact_by_phone(phone, name):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append({'phone': phone, 'name': name})
                
                # 통계 업데이트
                stats_text = f"처리됨: {i+1} / 성공: {results['success']} / 실패: {results['failed']}"
                self.root.after(0, lambda t=stats_text: self.stats_var.set(t))
                
                # 배치 간 대기
                if i > 0 and i % batch_size == 0:
                    self.log_queue.put(f"배치 처리 완료: {i+1}/{len(contacts)}")
                
            # 완료 처리
            self.root.after(0, lambda: self.progress_var.set(100))
            self.log_queue.put(f"자동화 완료: 성공 {results['success']}, 실패 {results['failed']}")
            
        except Exception as e:
            self.log_queue.put(f"자동화 중 오류: {str(e)}")
        finally:
            # UI 복원
            self.root.after(0, self._automation_finished)
            if self.kakao_automation:
                self.kakao_automation.close_driver()
    
    def stop_automation(self):
        """자동화 중지"""
        self._stop_automation = True
        self.log_message("중지 요청됨...")
    
    def _automation_finished(self):
        """자동화 완료 후 UI 복원"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("완료")
        self._stop_automation = False
    
    def export_data(self):
        """데이터 내보내기"""
        if not self.phone_manager.valid_phones:
            messagebox.showerror("오류", "내보낼 데이터가 없습니다.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="CSV 파일로 저장",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            if self.phone_manager.export_to_csv(filename):
                messagebox.showinfo("성공", f"데이터를 {filename}에 저장했습니다.")
            else:
                messagebox.showerror("오류", "데이터 내보내기에 실패했습니다.")
    
    def log_message(self, message):
        """로그 메시지 추가"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """로그 지우기"""
        self.log_text.delete(1.0, tk.END)
    
    def check_log_queue(self):
        """로그 큐 모니터링"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_message(message)
        except queue.Empty:
            pass
        
        # 100ms 후 다시 체크
        self.root.after(100, self.check_log_queue)

def main():
    """메인 함수"""
    root = tk.Tk()
    app = KakaoContactManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()