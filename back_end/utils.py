# -*- coding: utf-8 -*-
# Copyright (c) 2022, Shang Luo
# All rights reserved.
#
# Author: 罗尚
# Building Time: 2024/3/16
# Reference: None
# Description: None
import json
import pymysql
import subprocess
# import whisper

from datetime import datetime
from pathlib import Path

audios_path = './audios'
ptr_path = 'data_ptr.json'
cfg_path = '../config.json'
day_gaps = [1, 3, 7, 7, 14, 14, 14, 30]


def read_json(data_path):
    try:
        with open(data_path, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        print(e)
        print(f'{data_path} is Null')
        data = {}
    return data


def execute_cmd(cmd_lines: str, args=None):
    with connection.cursor() as cursor:
        cursor.execute(cmd_lines, args)
        connection.commit()
    return cursor.fetchall()


def update_joke(joke: str):
    update_src_cmd = "INSERT INTO src_jokes (joke) VALUE (%s)"
    execute_cmd(update_src_cmd, joke)
    strs_append(joke)


def strs_append(src_ques_str):
    len_table = execute_cmd("SELECT COUNT(*) FROM joke_queue;")[0][0]
    if len_table == 0:
        queue_init()

    for i, _ in enumerate(day_gaps):
        queue_idx = (ptrs['queue'] + sum(day_gaps[:(i + 1)])) % sum(day_gaps)
        get_ques_cmd = f"SELECT review_list FROM joke_queue WHERE q_id = {(queue_idx + 1)};"
        org_i_ques = execute_cmd(get_ques_cmd)[0][0]

        if len(org_i_ques) != 0:
            comb_strs = [org_i_ques, src_ques_str]
            comb_strs = '|'.join(comb_strs)
        else:
            comb_strs = src_ques_str

        update_table_cmd = "UPDATE joke_queue SET review_list = %s WHERE q_id = %s;"
        execute_cmd(update_table_cmd, (comb_strs, (queue_idx + 1)))


def queue_init():
    init_queue_cmd = "INSERT INTO joke_queue (review_list) VALUE (%s)"
    for _ in range(sum(day_gaps)):
        execute_cmd(init_queue_cmd, "")


def pop_jokes():
    get_jokes_cmd = f"SELECT review_list FROM joke_queue WHERE q_id = {(ptrs['queue'] + 1)};"
    org_jokes = execute_cmd(get_jokes_cmd)[0][0]
    ptrs['queue'] = (ptrs['queue'] + 1) % sum(day_gaps)
    write_json(ptr_path, ptrs)
    if len(org_jokes) != 0:
        jokes_list = parse_ques_strs(org_jokes)
    else:
        jokes_list = []

    return jokes_list


def parse_ques_strs(ques_strs: str):
    ques_strs = ques_strs.split('|')
    return ques_strs


def write_json(file_name, json_dict, mode='w'):
    with open(file_name, mode, encoding='utf-8') as jf:
        json.dump(json_dict, jf)


def convert_weba_to_mp3(weba_data, output_path):
    # 使用ffmpeg的pipe协议将字节流作为输入
    command = [
        'ffmpeg',
        '-i', 'pipe:0',  # 从标准输入读取数据
        '-acodec', 'libmp3lame',  # 指定MP3编码器
        '-f', 'mp3',  # 指定输出格式为MP3
        '-ab', '192k',  # 设定比特率为192k
        '-y',  # 覆盖输出文件
        '-loglevel', 'warning',
        output_path  # 输出文件路径
    ]

    # 启动子进程
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input=weba_data)
    process.stdin.close()
    return_code = process.wait()

    if return_code != 0:
        raise Exception(f"ffmpeg process returned {return_code}")


def process_audios(request_files):
    # audio_to_text = {}
    today_date = datetime.now()
    for key, value in request_files.items():
        file_path = Path(value.filename)
        change_path = (audios_path / file_path.with_name(f'{today_date.strftime("%y_%m_%d")}-' + file_path.name)
                       .with_suffix('.mp3'))
        convert_weba_to_mp3(value.read(), str(change_path))


db_config = read_json(cfg_path)['db_cfg']
connection = pymysql.connect(**db_config)
ptrs = read_json(ptr_path)
# tiny base small medium large
# model = whisper.load_model("medium").to('cuda')

if __name__ == '__main__':
    # n_days = sum(day_gaps) + 1
    # add_new_line = "INSERT INTO ques_queue (ques_strs) VALUES ('')"
    # for _ in range(n_days):
    #     execute_cmd(add_new_line)
    # ceate_new = "CREATE TABLE ques_queue (id INT AUTO_INCREMENT PRIMARY KEY, ques_strs VARCHAR(1023));"
    # print(execute_cmd(ceate_new))
    # ts_list = get_ques()
    ...
