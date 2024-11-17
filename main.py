from timer_app import TimerApp
import random

# 定义多套配色方案
COLOR_SCHEMES = [
    {
        # 灵感来自 Apple macOS Mojave 深色主题
        'name': 'Mojave Dark',
        'bg': '#1e1e1e',  # 深空灰
        'text': '#ffffff',  # 纯白
        'accent': '#0a84ff',  # 苹果蓝
        'button': '#323232',  # 深灰
        'button_text': '#ffffff',  # 纯白
        'status_text': '#989898'  # 浅灰
    },
    {
        # 灵感来自 Material Design 2.0
        'name': 'Material Ocean',
        'bg': '#0f111a',  # 深海蓝黑
        'text': '#84ffff',  # 青绿色
        'accent': '#00bcd4',  # 水蓝色
        'button': '#292d3e',  # 深紫蓝
        'button_text': '#82aaff',  # 亮蓝
        'status_text': '#676e95'  # 灰紫色
    },
    {
        # 灵感来自 Dribbble 流行设计
        'name': 'Modern Gradient',
        'bg': '#20123a',  # 深紫色
        'text': '#fff1e6',  # 暖白色
        'accent': '#ff7eb6',  # 粉红色
        'button': '#351c54',  # 中紫色
        'button_text': '#ffa8d5',  # 浅粉色
        'status_text': '#b69ac2'  # 浅紫色
    },
    {
        # 灵感来自 Nord 配色方案
        'name': 'Nord Theme',
        'bg': '#2e3440',  # 极夜蓝黑
        'text': '#eceff4',  # 极光白
        'accent': '#88c0d0',  # 冰川蓝
        'button': '#3b4252',  # 深极夜蓝
        'button_text': '#81a1c1',  # 极光蓝
        'status_text': '#d8dee9'  # 雪白
    },
    {
        # 灵感来自 Solarized Dark
        'name': 'Solarized',
        'bg': '#002b36',  # 深青蓝
        'text': '#fdf6e3',  # 淡米色
        'accent': '#859900',  # 橄榄绿
        'button': '#073642',  # 深青色
        'button_text': '#2aa198',  # 青绿色
        'status_text': '#93a1a1'  # 灰青色
    }
]

if __name__ == "__main__":
    # 随机选择一个配色方案
    color_scheme = random.choice(COLOR_SCHEMES)
    print(f"Using color scheme: {color_scheme['name']}")  # 打印当前使用的配色方案名称
    app = TimerApp(color_scheme)
    app.run()