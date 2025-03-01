import random
import threading
import keyboard
import pygame
import time


note_names = [
    'A0', 'Bb0', 'B0', 'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1', 'Gb1', 'G1', 'Ab1',
    'A1', 'Bb1', 'B1', 'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2',
    'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3',
    'A3', 'Bb3', 'B3', 'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4',
    'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5',
    'A5', 'Bb5', 'B5', 'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6',
    'A6', 'Bb6', 'B6', 'C7', 'Db7', 'D7', 'Eb7', 'E7', 'F7', 'Gb7', 'G7', 'Ab7',
    'A7', 'Bb7', 'B7', 'C8'
]

bpm = 120
beat = (0.25, 0.3, 0.5, 1)


def init():
    global press_count, event_stack, stack_lock
    global stop_flag, current_sound, index
    global press_flag, rhythm, score

    # 开启音效
    press_count = 10
    event_stack = []
    stack_lock = threading.Lock()

    stop_flag = False
    current_sound = pygame.mixer.Sound('sample/D6.mp3')
    index = 0 + note_names.index('D6')

    press_flag = False
    rhythm = 0.5
    score = 0


def get_rhythm():
    global rhythm

    # 默认节拍
    rhythm = beat[2]

    # 随机节拍
    # rhythm = beat[random.randint(0, len(beat)-1)]

    print(rhythm)
    return rhythm


def play(note):
    global current_sound, rhythm
    if current_sound:
        rhythm = get_rhythm()
        time.sleep(rhythm)
        current_sound.stop()
    file = str('sample/{}.mp3'.format(note))
    current_sound = pygame.mixer.Sound(file)
    current_sound.play(loops=0, maxtime=0, fade_ms=0)
    # print(file)


def stop_audio():
    global current_sound
    if current_sound:
        current_sound.stop()
        print("Stopped")


# def key_event_handler():
#     global stop_flag, index
#
#     while True:
#         # if keyboard.is_pressed('a'):
#         event = keyboard.read_event()
#         key = event.name
#         print(event.event_type)
#
#         if key == 'esc':
#             pygame.mixer.quit()
#             exit(0)
#
#         if event.event_type == 'down':
#             if not stop_flag:
#                 stop_flag = True
#                 threading.Timer(0, play, args=(note_names[index],)).start()
#                 # index = (index + 1) % len(note_names)
#                 index = random.randint(0, len(note_names) - 1)
#         elif event.event_type == 'up':
#             stop_flag = False


def playback():
    global press_count, event_stack, index, score

    while True:
        with stack_lock:
            if press_count > 0:
                note = note_names[index]
                # 递增旋律
                index = (index + 1) % len(note_names)
                # 随机旋律
                # index = random.randint(0, len(note_names) - 1)
                press_count -= 1
            else:
                note = None

        if note:
            print("Playing", note, press_count, "Score:", score)
            play(note)

        # time.sleep(0.05)

def key_event_handler():
    global event_stack, stack_lock, press_count
    global press_flag, score

    while True:
        # if keyboard.is_pressed('a'):
        event = keyboard.read_event()
        key = event.name
        print(event.event_type, score)

        if key == 'esc':
            pygame.mixer.quit()
            exit(0)

        if event.event_type == 'down' and press_flag == False:
            with stack_lock:
                press_flag = True
        elif event.event_type == 'up' and press_flag == True:
            with stack_lock:
                press_flag = False
                press_count += 1
                score += 1


def performance():
    init()
    threading.Thread(target=playback, daemon=True).start()
    threading.Thread(target=key_event_handler, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminated.")

# if __name__ == '__main__':
#     init()
#     # keyboard.hook(key_event_handler)
#     # event_thread = threading.Thread(target=key_event_handler)
#     # event_thread.daemon = True
#     # event_thread.start()
#
#     playback = threading.Thread(target=playback)
#     playback.daemon = True
#     playback.start()
#
#     event_thread = threading.Thread(target=key_event_handler)
#     event_thread.daemon = True
#     event_thread.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print('terminated.')



