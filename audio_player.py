import pygame
import os
import random
from threading import Thread
import time

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_sound = None
        self.is_playing = False
        self.is_alert_playing = False
        self.music_folder = "D:\\Development\\simple_timer\\sounds\\compressed"
        
        # Windows 系统提示音（使用中文名称）
        self.alert_sounds = {
            '编钟': 'C:\\Windows\\Media\\Alarm01.wav',
            '和旋': 'C:\\Windows\\Media\\Alarm02.wav',
            '清音': 'C:\\Windows\\Media\\Alarm03.wav',
            '悠扬': 'C:\\Windows\\Media\\Alarm04.wav',
            '铃声': 'C:\\Windows\\Media\\Alarm05.wav',
        }
        self.current_alert = '编钟'  # 默认提示音
        
    def play_random_music(self):
        if self.is_playing:
            self.stop_music()
            
        sound_files = [f for f in os.listdir(self.music_folder) 
                      if f.endswith(('.mp3', '.wav'))]
        if sound_files:
            sound_file = random.choice(sound_files)
            self.play_music(os.path.join(self.music_folder, sound_file))
            
    def play_music(self, sound_file):
        def fade_in():
            self.current_sound = pygame.mixer.Sound(sound_file)
            self.current_sound.set_volume(0.0)
            self.current_sound.play(-1)  # 循环播放
            
            # 淡入
            for vol in range(0, 10):
                if self.current_sound:  # 检查是否被停止
                    self.current_sound.set_volume(vol / 10.0)
                    time.sleep(0.1)
            self.is_playing = True
            
        Thread(target=fade_in).start()
        
    def stop_music(self):
        def fade_out():
            if self.current_sound and self.is_playing:
                # 淡出
                for vol in range(10, -1, -1):
                    if self.current_sound:  # 检查是否被停止
                        self.current_sound.set_volume(vol / 10.0)
                        time.sleep(0.1)
                if self.current_sound:
                    self.current_sound.stop()
                self.is_playing = False
                self.current_sound = None
                
        Thread(target=fade_out).start()

    def play_alert(self):
        """播放提示音（循环）"""
        def alert_loop():
            self.is_alert_playing = True
            alert_sound = pygame.mixer.Sound(self.alert_sounds[self.current_alert])
            while self.is_alert_playing:
                alert_sound.play()
                time.sleep(2)  # 每次播放间隔2秒
                
        Thread(target=alert_loop).start()
        
    def stop_alert(self):
        """停止提示音"""
        self.is_alert_playing = False
        
    def set_alert(self, alert_name):  # 修改方法名称
        """设置提示音"""
        if alert_name in self.alert_sounds:
            self.current_alert = alert_name