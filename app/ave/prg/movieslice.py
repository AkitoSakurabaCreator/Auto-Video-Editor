import math
import json
from .telop import Telop
from tqdm import tqdm
import whisper
import threading
import time
import random
import cv2
import numpy as np
import os
import ffmpeg
import wave 
import textwrap
import shutil

# with open('data.json') as f:
#     json_data = json.load(f)

class MovieSlice():
    # 動画を読み込み1フレームずつ画像処理をする関数
    def m_slice(self,path, dir, step, messages, teloppos):
        basename = os.path.basename(path)
        in_path = os.path.join(*[dir, path])                # 読み込みパスを作成
        out_path = os.path.join(*[dir, 'out_' + basename])      # 書き込みパスを作成
        movie = cv2.VideoCapture(in_path)                   # 動画の読み込み
        Fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))       # 動画の全フレーム数を計算
        fps = math.ceil(movie.get(cv2.CAP_PROP_FPS))        # 動画のFPS（フレームレート：フレーム毎秒）を取得
        W = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))        # 動画の横幅を取得
        H = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))       # 動画の縦幅を取得
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 動画保存時のfourcc設定（mp4用）

        # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
        video = cv2.VideoWriter(out_path, fourcc, int(fps / step), (W, H))
        ext_index = np.arange(0, Fs, step)  # 動画から静止画（フレーム）を抽出する間隔

        j = 0                               # messages配列から文章と時間を抜き出す指標番号
        section = messages[j]                # フレームに書き込む文章と時間の初期値

        max_message = 0
        for message in messages:
            if max_message < len(message[0]):
                max_message = len(message[0])

        for i in tqdm(range(Fs)):                 # フレームサイズ分のループを回す
            # print(i)
            flag, frame = movie.read()      # 動画から1フレーム読み込む
            check = i == ext_index          # 現在のフレーム番号iが、抽出する指標番号と一致するかチェックする
            time = i / int(fps/step)        # 抽出したフレームの動画内経過時間

            if flag == True:  # フレームを取得できた時だけこの処理をする
                # もしi番目のフレームが静止画を抽出するものであれば、ファイル名を付けて保存する
                if True in check:
                    # ここから動画フレーム処理と動画保存---------------------------------------------------------------------
                    # 抽出したフレームの再生時間がテロップを入れる時間範囲に入っていれば文字入れする
                    if section[1] <= time <= section[2]:
                        # frame = telop(frame, section[0], W, H, max_message)  # テロップを入れる関数を実行
                        telop = Telop()
                        frame = telop.telop(frame, section[0], W, H, teloppos)  # テロップを入れる関数を実行
                    # 再生時間がテロップ入れ開始時間より小さければ待機する
                    elif section[1] > time:
                        pass
                    else:
                        # 用意した文章がなくなったら何もしない
                        if j >= len(messages) - 1:
                            pass
                        # 再生時間範囲になく、まだmessages配列にデータがある場合はjを増分しsectionを更新
                        else:
                            j = j + 1
                            section = messages[j]
                    video.write(frame)                          # 動画を1フレームずつ保存する
                # ここまでが動画フレーム処理と保存---------------------------------------------------------------------
                # i番目のフレームが静止画を抽出しないものであれば、何も処理をしない
                else:
                    pass
            else:
                pass
        return