import configparser
import os

from analysis import read_config

# 定义88个钢琴音符（示例）
notes = [
    'A0', 'Bb0', 'B0', 'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1', 'Gb1', 'G1', 'Ab1',
    'A1', 'Bb1', 'B1', 'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2',
    'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3',
    'A3', 'Bb3', 'B3', 'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4',
    'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5',
    'A5', 'Bb5', 'B5', 'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6',
    'A6', 'Bb6', 'B6', 'C7', 'Db7', 'D7', 'Eb7', 'E7', 'F7', 'Gb7', 'G7', 'Ab7',
    'A7', 'Bb7', 'B7', 'C8'
]

# 存储匹配的音符和文件名
matched = {}
directory = 'sample'
config_path = 'parse.ini'


def tuning():
    # 读取配置文件时调整 configparser 的大小写处理行为
    config = configparser.ConfigParser()
    config.optionxform = str  # 保持键的大小写
    config.read(config_path)

    if 'Notes' not in config:
        config.add_section('Notes')

    # 遍历目录下的文件
    for filename in os.listdir(directory):
        for note in notes:
            if note in filename:
                matched[note] = filename

    # 输出匹配的音符和文件名
    for note in matched:
        # print(f"{note}:{matched[note]}")
        if note not in config['Notes']:
            config.set('Notes', note, matched[note])

    # 输出没有匹配到的音符
    unmatched = [note for note in notes if note not in matched]
    if unmatched:
        print('\nNo Found:')
    for note in unmatched:
        print(note)

    with open(config_path, 'w') as configfile:
        config.write(configfile)