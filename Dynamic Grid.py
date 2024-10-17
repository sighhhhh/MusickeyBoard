import threading
import time
from time import sleep
import threading
import keyboard

ext = {}  # 记录正在执行的线程
stop_flag = {}
seq = {}  # 记录按下的按键和对应的 array 元素
array = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
current = 0
lock = threading.Lock()


def play(key):
    global stop_flag
    with lock:
        if key in stop_flag and stop_flag[key] is False:
            print(stop_flag[key])
            if key in stop_flag and stop_flag[key] is False:
                sleep(0.5)
                print(current)
        elif key in stop_flag and stop_flag[key] is True:
            print(stop_flag[key])
            del stop_flag[key]


def handle_event(event):
    global current
    global stop_flag
    key = event.name
    current = current if current < len(array) else current - len(array)
    if event.event_type == 'down':
        with lock:
            if key not in seq:
                seq[key] = array[current]
                current += 1
                stop_flag[key] = False
                thread = threading.Thread(target=play, args=(key,))
                thread.start()
                ext[key] = thread
                # print(f"Pressed {key}: {seq[key]}")
                print("Current output:", list(seq.values()))

    elif event.event_type == 'up':
        with lock:
            if key in seq:
                # print(f"Release {key}: {seq[key]}")
                stop_flag[key] = True
                ext[key].join()
                del ext[key]
                del seq[key]
                print("Current output:", list(seq.values()))


try:
    # 监听所有按键事件
    keyboard.hook(handle_event)

    # 保持程序运行，直到用户终止
    keyboard.wait()

except KeyboardInterrupt:
    # 捕获用户中断（Ctrl + C）以优雅退出
    print("\nProgram terminated by user.")
