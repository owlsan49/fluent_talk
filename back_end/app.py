# -*- coding: utf-8 -*-
# Copyright (c) 2022, Shang Luo
# All rights reserved.
# 
# Author: 罗尚
# Building Time: 2024/4/3
# Reference: None
# Description: None
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import (read_json, update_joke, pop_jokes,
                   process_audios)

app = Flask(__name__)
CORS(app)


@app.route('/push_joke', methods=['POST'])
def push_words():
    results = {'resCode': 0}
    joke = request.get_json()['desc']
    print(f"submitted joke: {joke}")
    update_joke(joke)
    return jsonify(results)


@app.route('/get_today_info', methods=['GET'])
def get_today_info():
    results = {'resCode': 0}
    ques = pop_jokes()
    results['jokes_info'] = ques
    print(ques)
    return jsonify(results)

@app.route('/post_audios', methods=['POST'])
def post_audios():
    results = {'resCode': 0}
    process_audios(request.files)
    return jsonify(results)


if __name__ == '__main__':
    port = read_json('../config.json')['flask_port']
    app.run(debug=True, port=port)
