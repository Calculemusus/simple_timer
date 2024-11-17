import tkinter as tk
from tkinter import ttk, messagebox
import locale
from datetime import datetime
import os
from audio_player import AudioPlayer
from config import Config
from i18n import get_translations

class TimerApp:
    def __init__(self, color_scheme):
        self.root = tk.Tk()
        self.config = Config()
        self.color_scheme = color_scheme
        
        # 设置语言
        system_lang = locale.getdefaultlocale()[0][:2]
        self.translations = get_translations(system_lang)
        
        # 初始化音频播放器
        self.audio_player = AudioPlayer()
        
        # 初始化状态和时间
        self.is_working = True
        self.remaining_time = self.config.work_duration * 60
        self.alert_active = False  # 提示音状态标志
        
        # 设置窗口样式
        self.setup_styles()
        
        # 设置UI
        self.setup_ui()
        
    def update_time_display(self):
        """更新显示的时间"""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label['text'] = f"{minutes:02d}:{seconds:02d}"
        
    def setup_styles(self):
        # 设置现代化的样式
        self.root.configure(bg=self.color_scheme['bg'])
        self.style = ttk.Style()
        
        # 时间显示样式
        self.style.configure('Timer.TLabel', 
                           font=('Helvetica', 72, 'bold'),
                           foreground=self.color_scheme['text'],
                           background=self.color_scheme['bg'])
        
        # 状态显示样式
        self.style.configure('Status.TLabel', 
                           font=('Helvetica', 14),
                           foreground=self.color_scheme['status_text'],
                           background=self.color_scheme['bg'])
        
        # 按钮样式
        self.style.configure('Modern.TButton', 
                           font=('Helvetica', 12),
                           padding=10)
        
        # 设置窗口样式
        self.root.option_add('*TButton*background', self.color_scheme['button'])
        self.root.option_add('*TButton*foreground', self.color_scheme['button_text'])
        
    def setup_ui(self):
        self.root.title(self.translations['app_title'])
        self.root.geometry("350x280")
        self.root.resizable(False, False)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style='Main.TFrame')
        
        # 计时器显示
        self.time_label = ttk.Label(
            main_frame, 
            style='Timer.TLabel'
        )
        self.time_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        self.update_time_display()
        
        # 状态显示
        self.status_label = ttk.Label(
            main_frame,
            text=self.translations['working'],
            style='Status.TLabel'
        )
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2)
        button_frame.configure(style='Main.TFrame')
        
        # 控制按钮
        self.control_button = ttk.Button(
            button_frame,
            text=self.translations['start'],
            command=self.toggle_timer,
            style='Modern.TButton'
        )
        self.control_button.grid(row=0, column=0, padx=5)
        
        # 设置按钮
        self.settings_button = ttk.Button(
            button_frame,
            text=self.translations['settings'],
            command=self.show_settings,
            style='Modern.TButton'
        )
        self.settings_button.grid(row=0, column=1, padx=5)
        
        # 帮助按钮
        self.help_button = ttk.Label(
            main_frame,
            text="?",
            font=("Helvetica", 12),
            foreground=self.color_scheme['status_text'],
            background=self.color_scheme['bg']
        )
        self.help_button.grid(row=0, column=2, sticky="ne", padx=(10, 0))
        self.help_button.bind("<Enter>", self.show_help)
        self.help_button.bind("<Leave>", self.hide_help)
        
    def toggle_timer(self):
        if self.control_button['text'] == self.translations['start']:
            self.start_timer()
        else:
            self.pause_timer()
            
    def start_timer(self):
        self.control_button['text'] = self.translations['pause']
        self.update_timer()
        
    def pause_timer(self):
        self.control_button['text'] = self.translations['start']
        
    def update_timer(self):
        if self.control_button['text'] == self.translations['pause']:
            if self.remaining_time > 0:
                minutes = self.remaining_time // 60
                seconds = self.remaining_time % 60
                self.time_label['text'] = f"{minutes:02d}:{seconds:02d}"
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)
            else:
                # 时间结束，显示提示对话框
                next_mode = 'rest' if self.is_working else 'work'
                self.show_alert_dialog(next_mode)

    def show_alert_dialog(self, next_mode):
        """显示提示音对话框"""
        alert_window = tk.Toplevel(self.root)
        alert_window.title(self.translations['alert'])
        alert_window.geometry("300x150")
        alert_window.resizable(False, False)
        alert_window.configure(bg=self.color_scheme['bg'])
        
        # 确保窗口始终在最前面
        alert_window.attributes('-topmost', True)
        
        # 消息文本
        message = self.translations['work_complete'] if self.is_working else self.translations['rest_complete']
        ttk.Label(
            alert_window,
            text=message,
            style='Status.TLabel',
            wraplength=250
        ).pack(pady=20)
        
        # 确认按钮
        ttk.Button(
            alert_window,
            text=self.translations['confirm'],
            command=lambda: self.handle_alert_confirm(alert_window, next_mode),
            style='Modern.TButton'
        ).pack(pady=10)
        
        # 禁用主窗口，直到处理完提示
        alert_window.transient(self.root)
        alert_window.grab_set()
        
        # 开始播放提示音
        self.alert_active = True
        self.audio_player.play_alert()
        
    def handle_alert_confirm(self, alert_window, next_mode):
        """处理提示音确认"""
        self.alert_active = False
        self.audio_player.stop_alert()
        alert_window.destroy()
        
        # 切换到下一个模式
        if next_mode == 'work':
            self.start_work()
        else:
            self.start_rest()
            
    def start_work(self):
        """开始工作时间"""
        self.is_working = True
        self.status_label['text'] = self.translations['working']
        self.remaining_time = self.config.work_duration * 60
        self.update_timer()
        
    def start_rest(self):
        """开始休息时间"""
        self.is_working = False
        self.status_label['text'] = self.translations['resting']
        self.remaining_time = self.config.rest_duration * 60
        self.audio_player.play_random_music()
        self.update_timer()
                
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self.translations['settings'])
        settings_window.geometry("350x250")
        settings_window.resizable(False, False)
        settings_window.configure(bg=self.color_scheme['bg'])
        
        # 设置框架
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        settings_window.columnconfigure(0, weight=1)
        settings_window.rowconfigure(0, weight=1)
        
        # 时间设置框架
        time_frame = ttk.Frame(settings_frame)
        time_frame.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0,15))
        
        # 工作时间设置（更紧凑的布局）
        ttk.Label(time_frame, 
                 text="工作",
                 style='Status.TLabel').grid(row=0, column=0, padx=(0,5))
        work_duration = ttk.Entry(time_frame, width=5)
        work_duration.insert(0, str(self.config.work_duration))
        work_duration.grid(row=0, column=1)
        ttk.Label(time_frame, 
                 text="分钟",
                 style='Status.TLabel').grid(row=0, column=2, padx=(2,15))
        
        # 休息时间设置
        ttk.Label(time_frame, 
                 text="休息",
                 style='Status.TLabel').grid(row=0, column=3, padx=(0,5))
        rest_duration = ttk.Entry(time_frame, width=5)
        rest_duration.insert(0, str(self.config.rest_duration))
        rest_duration.grid(row=0, column=4)
        ttk.Label(time_frame, 
                 text="分钟",
                 style='Status.TLabel').grid(row=0, column=5, padx=(2,0))
        
        # 提示音选择
        sound_frame = ttk.Frame(settings_frame)
        sound_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0,15))
        
        ttk.Label(sound_frame, 
                 text="提示音：",
                 style='Status.TLabel').grid(row=0, column=0, sticky='w')
        
        alert_var = tk.StringVar(value=self.audio_player.current_alert)
        alert_combo = ttk.Combobox(sound_frame, 
                                 textvariable=alert_var,
                                 values=list(self.audio_player.alert_sounds.keys()),
                                 state='readonly',
                                 width=10)
        alert_combo.grid(row=0, column=1, padx=(5,0))
        
        # 播放测试按钮
        test_button = ttk.Label(
            sound_frame,
            text="▶",
            font=("Helvetica", 12),
            foreground=self.color_scheme['accent']
        )
        test_button.grid(row=1, column=1, pady=(5,0), sticky='w')
        test_button.bind('<Button-1>', lambda e: self.test_alert(alert_var.get()))
        test_button.bind('<Enter>', lambda e: test_button.configure(cursor='hand2'))
        test_button.bind('<Leave>', lambda e: test_button.configure(cursor=''))
        
        # 保存按钮
        save_button = ttk.Button(
            settings_frame,
            text=self.translations['save'],
            command=lambda: self.save_settings(
                settings_window, 
                work_duration.get(), 
                rest_duration.get(), 
                alert_var.get()
            ),
            style='Modern.TButton',
            width=15
        )
        save_button.grid(row=2, column=0, columnspan=2, pady=(10,0))
        
        # 设置初始焦点
        work_duration.focus_set()
        
        # 使窗口居中
        settings_window.transient(self.root)
        settings_window.grab_set()
        self.root.wait_window(settings_window)

    def test_alert(self, alert_name):
        """测试提示音"""
        self.audio_player.set_alert(alert_name)
        self.audio_player.play_alert()
        self.root.after(3000, self.audio_player.stop_alert)

    def save_settings(self, window, work_time, rest_time, alert_name):
        """保存设置"""
        try:
            work_time = int(work_time)
            rest_time = int(rest_time)
            if work_time <= 0 or rest_time <= 0:
                raise ValueError
            
            self.config.work_duration = work_time
            self.config.rest_duration = rest_time
            self.config.save_settings()
            
            if self.is_working:
                self.remaining_time = work_time * 60
            else:
                self.remaining_time = rest_time * 60
            
            self.audio_player.set_alert(alert_name)
            self.update_time_display()
            window.destroy()
            messagebox.showinfo(
                self.translations['settings'],
                self.translations['settings_saved']
            )
        except ValueError:
            messagebox.showerror(
                self.translations['error'],
                self.translations['invalid_input']
            )
        
    def show_help(self, event):
        help_window = tk.Toplevel(self.root)
        help_window.title(self.translations['help'])
        help_window.configure(bg=self.color_scheme['bg'])
        help_text = ttk.Label(
            help_window,
            text=self.translations['help_text'],
            wraplength=300,
            padding=20,
            style='Status.TLabel'
        )
        help_text.pack()
        
    def hide_help(self, event):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
                
    def run(self):
        self.root.mainloop()