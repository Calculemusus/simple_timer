import json
import os

class Config:
    def __init__(self):
        self.config_file = "settings.json"
        self.load_settings()
        
    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)
                    self.work_duration = settings.get('work_duration', 45)
                    self.rest_duration = settings.get('rest_duration', 15)
            except:
                self.set_defaults()
        else:
            self.set_defaults()
            
    def set_defaults(self):
        self.work_duration = 45  # 默认工作时间（分钟）
        self.rest_duration = 15  # 默认休息时间（分钟）
        
    def save_settings(self):
        settings = {
            'work_duration': self.work_duration,
            'rest_duration': self.rest_duration
        }
        with open(self.config_file, 'w') as f:
            json.dump(settings, f)