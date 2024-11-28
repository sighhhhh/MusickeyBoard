import os
import configparser
import sounddevice as sd
import numpy as np
import pygame
import threading
import keyboard
import simpleaudio as sa
from scipy.io.wavfile import read
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from memory_profiler import profile

# 设置音频文件存储目录
config_path = 'parse.ini'  # 解析音符和文件名的配置文件
notes_directory = 'sample'  # 音符音频文件所在目录
song_file_path = 'notes/梁祝.ini'  # 解析的歌曲音符序列文件路径


# 持续时长
def get_sustain():
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    if 'Delay' in config.sections():
        sustain = config.getfloat('Delay', 'sustain')
        return sustain
    else:
        print(f'sustain 未配置')


# 延音时长
def get_fade():
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    if 'Delay' in config.sections():
        fade = config.getfloat('Delay', 'fade')
        return fade
    else:
        print(f'fade 未配置')


# 读取音符和音频文件路径的配置
# {'A0':'/sample/A0.mp3','Bb0':'/sample/Bb0.mp3' }
def load_notes_from_config(config_path, notes_directory):
    config = configparser.ConfigParser()
    config.optionxform = str  # 保持键的大小写
    config.read(config_path, encoding='utf-8')

    notes = {}
    # 读取 [notes] 部分，获取音符与音频文件名的对应关系
    if 'Notes' in config.sections():
        for note, filename in config['Notes'].items():
            note_path = os.path.join(notes_directory, filename)
            if os.path.exists(note_path):
                notes[note] = note_path
            else:
                print(f"音频文件缺失: {note_path}")
    else:
        print("找不到音符")

    return notes


# 读取歌曲的音符序列
# ['A0', 'Bb0', 'B0']
def load_song_notes(song_file_path):
    config = configparser.ConfigParser()
    config.read(song_file_path)

    if 'Notes' in config.sections():
        notes_sequence = config['Notes'].get('sequence', '').split(', ')
        return notes_sequence
    else:
        print("未找到歌曲的音符序列，请解析后重试")
        return []


# 全局音乐播放器类
class NotePlayer:
    def __init__(self, notes, song_notes, song_name, sustain_time, fade_time):
        self.notes = notes  # {'A0':'/sample/A0.mp3','Bb0':'/sample/Bb0.mp3' }
        self.song_notes = song_notes  # ['A0', 'Bb0', 'B0']
        self.song_name = song_name
        self.current_note_index = 0
        self.sustain_time = sustain_time
        self.fade_time = fade_time
        # self.playing_sounds = {}
        self.key_seq = {}
        # self.key_held = False
        self.play_obj = {}
        # self.executor = ThreadPoolExecutor(max_workers=10)
        self.execute = {}
        self.stop_flag = {}
        # self.active_threads = 0
        self.lock = threading.Lock()
        print(f"当前正在演奏:{self.song_name}")

    # 播放音符
    def play_note(self, note, key):
        print(f"stop_flag: {self.stop_flag}")
        if key in self.stop_flag and self.stop_flag[key] is False:
            if note in self.notes:
                ext = os.path.splitext(self.notes[note])[1].lower()
                if ext == ".wav":
                    audio = AudioSegment.from_wav(self.notes[note])
                elif ext == ".mp3":
                    audio = AudioSegment.from_mp3(self.notes[note])
                else:
                    print(ext)
                    raise ValueError(f'Unsupported file format: {ext}')

                # 将音频数据转换为 raw 音频数据
                raw_data = audio.raw_data
                # 获取音频的采样率和声道数等信息
                sample_rate = audio.frame_rate
                num_channels = audio.channels
                sample_width = audio.sample_width

                # if key in self.stop_flag and self.stop_flag[key] is False:
                self.play_obj[key] = sa.play_buffer(raw_data, num_channels, sample_width, sample_rate)
                # self.play_obj[key].wait_done()
            else:
                print(f"无法播放，文件不存在: {note}")

        elif key in self.stop_flag and self.stop_flag[key] is True:
            if self.play_obj[key].is_playing():
                self.play_obj[key].stop()
                del self.stop_flag[key]

    def handle_event(self, event):
        key = event.name
        if self.current_note_index >= len(self.song_notes):
            self.current_note_index = self.current_note_index - len(self.song_notes)

        if event.event_type == 'down':
            if key not in self.key_seq:
                print(f"Pressed {key}:", list(self.key_seq.values()))
                self.key_seq[key] = self.song_notes[self.current_note_index]
                self.current_note_index += 1
                note = self.song_notes[self.current_note_index]
                self.stop_flag[key] = False
                thread = threading.Thread(target=self.play_note, args=(note, key))
                thread.start()
                self.execute[key] = thread
                print(f"Played list: {list(self.key_seq.values())}")

        elif event.event_type == 'up':
            if key in self.key_seq:
                print(f"Release {key}: {self.key_seq[key]}")
                self.stop_flag[key] = True
                self.execute[key].join()
                del self.execute[key]
                del self.key_seq[key]
                print(f"Played list: {list(self.key_seq.values())}")


    def start_listening(self):
        # 启动全局键盘监听器
        try:
            keyboard.hook(self.handle_event)
            keyboard.wait()
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
        # with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #     listener.join()

    # def shutdown(self):
    #     # 当程序结束时，关闭线程池
    #     self.executor.shutdown(wait=True)


# 主程序
@profile(precision=5)
def performance():
    # 读取音符和对应的音频文件
    notes = load_notes_from_config(config_path, notes_directory)
    print(f"检测到的音符: {list(notes.keys())}")

    # 读取歌曲的音符序列
    song_notes = load_song_notes(song_file_path)
    print(f"歌曲音符序列: {song_notes}")

    # 创建 NotePlayer 实例并开始监听
    sustain = get_sustain()
    fade_time = get_fade()
    song_name = '梁祝'
    player = NotePlayer(notes, song_notes, song_name, sustain, fade_time)
    player.start_listening()
