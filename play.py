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


def init():
    global stop_flag, index, current_sound
    pygame.init()
    pygame.mixer.init()

    stop_flag = False
    index = 0 + note_names.index('D6')
    current_sound = pygame.mixer.Sound('sample/D6.mp3')


def play(note):
    global current_sound, current_thread
    if current_sound:
        current_sound.stop()
    file = str('sample/{}.mp3'.format(note))
    current_sound = pygame.mixer.Sound(file)

    current_sound.play(loops=0, maxtime=0, fade_ms=0)
    print("Playing", file)


def stop_audio():
    global current_sound
    if current_sound:
        current_sound.stop()
        print("Stopped")


def key_event_handler():
    global stop_flag, index
    while True:
        if keyboard.is_pressed('a'):
            if not stop_flag:
                stop_flag = True
                play(note_names[index])
                threading.Timer(1.8, stop_audio).start()
                index = (index + 1) % len(note_names)
        elif not keyboard.is_pressed('a') and stop_flag:
            stop_flag = False
        time.sleep(0.1)


if __name__ == '__main__':
    init()
    event_thread = threading.Thread(target=key_event_handler)
    event_thread.daemon = True
    event_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('terminated.')



