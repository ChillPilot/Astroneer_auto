import threading
import time
from pynput import keyboard
import pyautogui
from tkinter import Tk, Label, Entry, Frame, messagebox

# 全局变量，控制鼠标点击
is_clicking = False
click_interval = 6.0  # 默认循环时间为6秒

def on_press(key):
    global is_clicking
    if key == keyboard.Key.backspace:
        if not is_clicking:
            is_clicking = True
            # 启动一个线程来处理点击
            threading.Thread(target=start_clicking).start()
    else:
        # 如果正在点击，则停止
        is_clicking = False

def start_clicking():
    global click_interval
    while is_clicking:
        pyautogui.click()
        time.sleep(click_interval)  # 根据输入的间隔时间点击

def update_click_interval():
    global click_interval
    try:
        new_interval = float(interval_entry.get())  # 获取输入框中的值
        if new_interval > 0:
            click_interval = new_interval
        else:
            messagebox.showerror("输入错误", "请输入一个大于0的数字")
    except ValueError:
        messagebox.showerror("输入错误", "请输入一个有效的数字")

def create_gui():
    # 设置窗口初始高度和宽度
    height = 150
    width = 300
    root = Tk()
    root.title("Auto Clicker")
    root.geometry(f"{width}x{height}")
    root.maxsize(500, 200)  # 设置窗口最大尺寸
    root.configure(bg="#87CEEB")  # 设置背景颜色为蔚蓝色

    # 右侧布局
    right_frame = Frame(root, bg="#87CEEB")
    right_frame.pack(fill="both", expand=True)

    # 输入框和更新按钮在一行
    input_frame = Frame(right_frame, bg="#87CEEB")
    input_frame.pack(pady=(10, 0))

    # 输入框
    global interval_entry
    interval_entry = Entry(input_frame, font=("幼圆", 10), width=5)
    interval_entry.insert(0, "6")  # 默认值为6秒
    interval_entry.pack(side="left", padx=(0, 5))

    # 更新按钮
    update_button = Label(input_frame, text="更新时间", font=("幼圆", 10, "bold"), bg="#87CEEB", fg="red", cursor="hand2")
    update_button.bind("<Button-1>", lambda e: update_click_interval())
    update_button.pack(side="left")

    # 添加文字说明
    text_label = Label(right_frame, text="使用说明：\n"
                                         "1. 按退格键开始左键单击。\n"
                                         "2. 更新时间可以设置循环间隔。\n"
                                         "3. 循环时，按下任意键停止。\n",
                       font=("幼圆", 10), bg="#87CEEB", fg="black", justify="left")
    text_label.pack(pady=(10, 0))

    # 启动键盘监听
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    root.mainloop()

if __name__ == "__main__":
    create_gui()