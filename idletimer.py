import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import datetime
import configparser
import sys
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json
from pynput import mouse, keyboard
import threading
import win32api
import win32con
import win32gui
import winreg

class AFKWidget:
    """
    핵심 : AFK (Away From Keyboard) 시간을 추적하고 표시하는 위젯 클래스
    (Windows 환경에서만 동작합니다 - win32api, win32con, win32gui 사용)
    
    주요 기능:
    - 사용자의 마우스/키보드 활동 감지(3분 이상 미활동 시 AFK 시간 증가)
    - 일시정지 기능을 추가해 다른 공간에서 작업해야 할 때 AFK 시간 측정 중지
    - AFK 시간 측정 및 표시
    - 일일 AFK 시간 데이터 저장 및 그래프 표시
    - 자정 자동 리셋과 함께 데이터 저장
    - Exit 버튼 누를시 마지막으로 저장된 위치와 현재 타이머 시각 저장 및 종료
    """

    def __init__(self):
        """
        핵심 : 위젯 초기화 및 기본 설정
        - 윈도우 설정 (투명도, 최상단 표시)
        - 데이터 초기화
        - UI 구성
        - 이벤트 리스너 설정
        """

        # Tkinter 윈도우 설정
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.9)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1a1a1a')
        
        # hwnd(윈도우 핸들)을 가져와서 툴윈도우로 설정
        hwnd = self.root.winfo_id()
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style |= win32con.WS_EX_TOOLWINDOW
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
        
        # AFK 시간 추적을 위한 변수 초기화 + 포맷 설정
        self.is_paused = False
        self.last_activity = time.time()
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.daily_afk_times = self.load_afk_history()
        
        # 오늘의 AFK 시간을 불러오고, 불러오는데 실패했을 시 0으로 초기화
        if self.today in self.daily_afk_times:
            self.afk_time = self.daily_afk_times[self.today]
        else:
            self.afk_time = 0
            
        # UI 구성
        self.setup_ui()
        self.update_timer_display()
        self.load_position()
        
        # 버튼 이벤트 리스너 설정
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        # 시작 프로그램 등록 확인 및 설정
        self.create_registry_file()
        self.check_startup_registry()
        # 스레드로 각종 기능 실행
        self.start_activity_monitoring()
        self.check_midnight_reset()
        self.check_topmost()

    def get_app_directory(self):
        """
        핵심 : 애플리케이션 데이터 디렉토리 경로 반환
        """
        documents_path = os.path.expanduser('~/Documents')
        app_path = os.path.join(documents_path, 'AFKTimer')
    
        # AFKTimer 폴더가 없으면 생성
        if not os.path.exists(app_path):
            os.makedirs(app_path)
        
        return app_path

    def create_registry_file(self):
        """
        핵심 : 현재 실행 경로를 반영한 레지스트리 파일 생성
        """
        # 실행 경로를 가져와서 레지스트리 파일 생성
        if getattr(sys, 'frozen', False):
            current_path = os.path.abspath(sys.executable)
        else:
            current_path = os.path.abspath(sys.argv[0])
        
        current_path = current_path.replace("\\", "\\\\")
        
        # 레지스트리 파일 내용 하드코딩
        reg_content = f"""Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run]
"AFKTimer"="{current_path}"
"""
        reg_path = os.path.join(self.get_app_directory(), "autostart_afktimer.reg")

        # 레지스트리 파일 생성
        with open(reg_path, "w", encoding='utf-8') as f:
            f.write(reg_content)

    def check_startup_registry(self):
        """
        핵심 : 시작 프로그램 등록 여부를 확인하고, 
        등록되지 않았다면 사용자에게 안내
        """

        # 레지스트리 키 경로
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
        # 시작 프로그램 등록 여부 확인
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_READ
            )
        
            try:
                winreg.QueryValueEx(key, "AFKTimer")
                # 이미 등록되어 있음
                return True
            except WindowsError:
                # 등록되어 있지 않음
                response = messagebox.askyesno(
                    "자동 시작 설정",
                    "프로그램이 시작 프로그램에 등록되어 있지 않습니다.\n"
                    "autostart_afktimer.reg 파일을 실행하여 등록할 수 있습니다.\n"
                    "지금 등록 파일을 실행하시겠습니까?"
                )
                if response:
                    history_path = os.path.join(self.get_app_directory(), 'autostart_afktimer.reg')
                    os.startfile(history_path)
                return False
            
        # 레지스트리 키가 없는 경우
        finally:
            winreg.CloseKey(key)


    def setup_ui(self):
        """
        핵심 : 위젯의 UI 구성요소 초기화
        - 타이머 레이블
        - Pause/Resume 버튼
        - AFK 시간 그래프
        - Exit 버튼
        """
        # 타이머 레이블 설정. 기본 폰트인 Arial을 사용하여 윈도우 pc에서의 활용 보장
        self.timer_label = tk.Label(
            self.root,
            text="00:00:00",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 20)
        )
        self.timer_label.pack(pady=10)
        
        # Pause/Resume 버튼 설정
        self.pause_button = tk.Label(
            self.root,
            text="Pause",
            fg="white",
            bg="#1a1a1a",
            cursor="hand2"
        )
        self.pause_button.pack(pady=5)
        self.pause_button.bind('<Button-1>', self.toggle_pause)
        
        # AFK 시간 그래프 설정
        self.setup_graph()
        
        # Exit 버튼 설정
        self.exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.on_exit,
            bg="#1a1a1a",
            fg="white"
        )
        self.exit_button.pack(pady=10)

    def setup_graph(self):
        """
        핵심 : AFK 시간 그래프 설정 및 생성
        - 데이터 범위에 따른 동적 스케일링
        - 시간 포맷 자동 조정
        - 그래프 스타일 설정
        """
        # figsize가 (5, 2)인 Figure 객체 생성
        fig = Figure(figsize=(5, 2), facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_facecolor('white')
        
        # 최근 7일간의 AFK 시간 데이터를 그래프로 표시
        dates = list(self.daily_afk_times.keys())[-7:]
        times = [self.daily_afk_times[date] for date in dates]
        max_time = max(times) if times else 0
        
        def format_time(seconds, pos):
            """
            하위 함수 : 시간 포맷 조정
            - 1시간 미만 : 분, 초
            - 1시간 이상 : 시간, 분
            """
            if max_time < 3600:
                minutes = int(seconds // 60)
                seconds = int(seconds % 60)
                return f'{minutes}m {seconds}s'
            else:
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                return f'{hours}h {minutes}m'
        
        # 그래프 스타일 설정 : 기본 설정은 꺾은선 그래프가 빨강입니다. 포맷팅을 따릅니다!
        ax.plot(dates, times, color='red', marker='o', linewidth=2, markersize=6)
        ax.set_xticklabels(dates, rotation=45)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_time))
        
        # 데이터 범위에 따른 동적 스케일링(유휴 시간의 크기가 차이날때...)
        if max_time < 60:
            ax.yaxis.set_major_locator(plt.MaxNLocator(5))
        elif max_time < 3600:
            ax.yaxis.set_major_locator(plt.MaxNLocator(6))
        else:
            ax.yaxis.set_major_locator(plt.MaxNLocator(8))
        
        # 그래프 스타일 설정 : 레이블, 그리드, 레이아웃
        ax.tick_params(colors='black')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        if max_time > 0:
            ax.set_ylim(0, max_time * 1.1)
        
        fig.tight_layout()
        
        # 그래프를 Tkinter 위젯으로 변환하여 표시
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def start_activity_monitoring(self):
        """
        핵심 : 마우스와 키보드 활동 모니터링 시작
        - 이벤트 리스너 설정
        - AFK 상태 체크 타이머 시작
        """
        def on_activity(*args):
            """
            하위 함수 : 마우스/키보드 활동 감지 시간 업데이트
            - 마지막 활동 시간을 현재 시간으로 업데이트
            """
            # 마지막 활동 시간을 현재 시간으로 업데이트
            self.last_activity = time.time()
        
        # 마우스/키보드 이벤트 리스너 설정
        mouse_listener = mouse.Listener(
            on_move=on_activity,
            on_click=on_activity,
            on_scroll=on_activity
        )
        keyboard_listener = keyboard.Listener(on_press=on_activity)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # AFK 상태 체크 타이머 시작
        self.check_afk()

    def check_afk(self):
        """
        핵심 : AFK 상태 확인 및 타이머 업데이트
        10초 이상 활동이 없으면 AFK 시간 증가
        """
        # 일시정지 상태가 아니라면 AFK 시간 증가
        if not self.is_paused:
            current_time = time.time()
            # 3분 이상 활동이 없으면 AFK 시간 증가(바꾸고 싶을 시 이 부분 숫자를 변경해주세요)
            if current_time - self.last_activity >= 180:
                self.afk_time += 1
                self.update_timer_display()
        
        # 1초마다 AFK 상태 체크
        self.root.after(1000, self.check_afk)

    def check_midnight_reset(self):
        """
        핵심 : 자정이 될 시 리셋 확인 및 처리
        - 데이터 저장
        - 타이머 리셋
        - 그래프 갱신
        """
        # 현재 시간이 자정이면 데이터 저장 및 타이머 리셋
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            self.save_daily_afk()
            self.afk_time = 0
            self.update_timer_display()
            
            # 그래프 갱신(기존 그래프 삭제 후 새로 생성)
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Widget) and widget != self.timer_label and widget != self.pause_button and widget != self.exit_button:
                    widget.destroy()
            
            self.setup_graph()
            self.exit_button.pack_forget()
            self.exit_button.pack(pady=10)
        
        # 자정이 되기 전까지 1분마다 체크
        self.root.after(60000, self.check_midnight_reset)

    def check_topmost(self):
        """
        핵심 : 위젯의 최상단 표시 상태 유지(Z-index상으로 최상단)
        """
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(1000, self.check_topmost)

    def update_timer_display(self):
        """
        핵심 : 타이머 디스플레이 업데이트
        - hh:mm:dd의 포맷을 따르도록 표시
        """
        hours = self.afk_time // 3600
        minutes = (self.afk_time % 3600) // 60
        seconds = self.afk_time % 60
        self.timer_label.config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    def toggle_pause(self, event):
        """
        핵심 : 타이머 일시정지/재개 토글
        (일종의 논리게이트 NOT 연산처럼, 반대 상황으로 변환해줍니다...)
        """
        self.is_paused = not self.is_paused
        self.pause_button.config(
            text="Resume" if self.is_paused else "Pause"
        )

    def load_afk_history(self):
        """
        핵심 : 저장된 AFK 기록 불러오기
        """
        history_path = os.path.join(self.get_app_directory(), 'afk_history.json')
        # 파일이 없거나 JSON 디코딩 에러가 발생하면 빈 딕셔너리 반환
        try:
            with open(history_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_daily_afk(self):
        """
        핵심 : 현재 AFK 시간을 파일에 저장
        (최근 30일간의 데이터만 유지)
        """
        # 오늘 날짜를 키로 하여 AFK 시간을 저장
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.daily_afk_times[today] = self.afk_time
        
        # 최근 30일간의 데이터만 유지
        dates = sorted(self.daily_afk_times.keys())
        if len(dates) > 30:
            for old_date in dates[:-30]:
                del self.daily_afk_times[old_date]
        
        # 파일에 저장
        history_path = os.path.join(self.get_app_directory(), 'afk_history.json')
        with open(history_path, 'w') as f:
            json.dump(self.daily_afk_times, f)

    def get_config_path(self):
        """
        핵심 : Documents 폴더 내 AFKTimer 폴더에서 설정 파일 경로 반환
        """
        documents_path = os.path.expanduser('~/Documents')
        afktimer_path = os.path.join(documents_path, 'AFKTimer')
    
        # AFKTimer 폴더가 없으면 생성
        if not os.path.exists(afktimer_path):
            os.makedirs(afktimer_path)
        
        return os.path.join(afktimer_path, 'widget_config.ini')

    def load_position(self):
        """
        핵심 : Documents/AFKTimer 폴더에서 위젯 위치 불러오기
        """
        config_path = os.path.join(self.get_app_directory(), 'widget_config.ini')
        config = configparser.ConfigParser()

        # 설정 파일이 없으면 새 설정 파일 생성 후 리턴
        if not os.path.exists(config_path):
            self.save_position()
            return
        
        config.read(config_path)
        # 설정 파일에서 x, y 좌표를 불러와서 윈도우 위치 설정
        try:
            x = config.getint('Position', 'x')
            y = config.getint('Position', 'y')
            self.root.geometry(f"+{x}+{y}")
        # 설정 파일이 손상되었을 경우 예외 처리(100, 100 위치로 초기화)
        except:
            self.root.geometry("+100+100")

    def save_position(self):
        """위젯 위치를 Documents/AFKTimer 폴더에 저장"""
        config = configparser.ConfigParser()
        config['Position'] = {
            'x': str(self.root.winfo_x()),
            'y': str(self.root.winfo_y())
        }
    
        config_path = os.path.join(self.get_app_directory(), 'widget_config.ini')
        with open(config_path, 'w') as f:
            config.write(f)

    def start_move(self, event):
        """
        핵심 : 마우스 이벤트에서 위젯 드래그 시작 지점 저장
        (마우스 클릭 지점을 저장해둡니다)
        """
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """
        핵심 : 마우스 이벤트에서 위젯 드래그 이동 처리
        """
        # 이동한 거리만큼 윈도우 위치를 조정
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_exit(self):
        """
        핵심 : 위젯 종료 처리
        - 현재 위치 저장
        - 현재 AFK 시간 저장
        """
        # Exit 버튼 클릭시 종료 처리
        self.save_position()
        self.save_daily_afk()
        self.root.quit()

    def run(self):
        """
        핵심 : 위젯 실행
        """
        # Tkinter 메인 루프 실행
        self.root.mainloop()

if __name__ == "__main__":
    # 위젯 객체 생성 및 실행
    widget = AFKWidget()
    widget.run()
