import os
import librosa
import numpy as np
import configparser

# 设置目录路径和配置文件路径
music_directory = 'music'
config_path = 'parse.ini'
notes_directory = 'notes'

# 定义音符和频率的映射
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


# 将频率转换为最近的音符名称
def frequency_to_note_name(frequency):
    midi = librosa.hz_to_midi(frequency)
    midi = int(np.clip(midi, 21, 108))  # 钢琴音符范围：A0 (21) 到 C8 (108)
    return note_names[midi - 21]


# 读取或创建配置文件
def read_config(config_path):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    return config


# 更新配置文件中的歌曲状态
def update_config(config, config_path, song_name, status):
    config.set('Songs', song_name, status)
    with open(config_path, 'w') as configfile:
        config.write(configfile)


# 获取目录下的所有WAV和MP3文件
def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(('.wav', '.mp3'))]


# 存储解析结果到单独的.ini文件
def save_notes_to_file(file_name, notes):
    # 创建 notes 目录
    if not os.path.exists(notes_directory):
        os.makedirs(notes_directory)

    # 创建配置文件路径
    note_file_path = os.path.join(notes_directory, f"{os.path.splitext(file_name)[0]}.ini")
    note_config = configparser.ConfigParser()
    note_config.add_section('Notes')

    # 将音符列表转化为字符串并存储
    note_config.set('Notes', 'notes_sequence', ', '.join(notes))

    # 保存到 .ini 文件
    with open(note_file_path, 'w') as configfile:
        note_config.write(configfile)


# 解析音频文件
def parse_audio_file(file_path):
    y, sr = librosa.load(file_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    notes = []

    # 提取音符
    for t in range(pitches.shape[1]):
        pitch = pitches[:, t]
        index = pitch.argmax()  # 找到音高最强的索引
        frequency = pitch[index]
        if frequency > 0:  # 如果检测到音高
            note_name = frequency_to_note_name(frequency)
            notes.append(note_name)

    # 打印检测到的音符
    print(f"解析文件: {file_path}")
    print("检测到的音符：", notes)
    return notes


# 主程序
def analysis():
    config = read_config(config_path)

    # 如果配置文件中没有歌曲部分，则添加
    if 'Songs' not in config:
        config.add_section('Songs')

    audio_files = get_audio_files(music_directory)

    for file in audio_files:
        file_path = os.path.join(music_directory, file)

        # 如果文件不在配置文件中，标记为 unparsed
        if file not in config['Songs']:
            config.set('Songs', file, 'unparsed')

        # 检查文件状态
        if config['Songs'][file] == 'unparsed':
            # 解析文件
            notes = parse_audio_file(file_path)
            # 保存解析结果到 notes 目录
            save_notes_to_file(file, notes)
            # 更新文件状态为 parsed
            update_config(config, config_path, file, 'parsed')
        else:
            print(f"跳过已解析文件: {file_path}")
