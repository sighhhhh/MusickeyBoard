import threading
import time
import pygame

pygame.mixer.init()

threads = {}

def play_music(sound_file, key):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    start_time = time.time()

    while time.time() - start_time < 5:
        if not threads[key]["playing"]:
            break
        time.sleep(0.1)

    pygame.mixer.music.stop()
    threads[key]["playing"] = False

def key_pressed(key, sound_file):
    if key in threads and threads[key]["playing"]:
        return
    threads[key] = {
        "playing": True,
        "thread": threading.Thread(target=play_music, args=(sound_file, key))
    }
    threads[key]["thread"].start()

def key_released(key):
    if key in threads:
        threads[key]["playing"] = False
        threads[key]["thread"].join()

def simulate_key_press(key, sound_file):
    print(f"pressed key : {key}")
    key_pressed(key, sound_file)

def simulate_key_release(key):
    print(f"release key : {key}")
    key_released(key)

sound_file = ""
