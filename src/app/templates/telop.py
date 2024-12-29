import math
import json
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
import time # タイムラグをつける

from PIL import Image, ImageFont, ImageDraw
from moviepy.editor import *
from pydub import AudioSegment, effects

class Telop():
    # 画像に文字を入れる関数
    def telop(self,img, messages, W, H, teloppos):
        font_path = 'C:\Windows\Fonts\meiryo.ttc'        # Windowsのフォントファイルへのパス
        max_font_size = 120                                 # フォントサイズ
        min_font_size = 80

        font_size = int(W / len(messages))               # 動画の解像度(横) / 字幕の文字数 フォントサイズの上限あり
        if font_size > max_font_size:
            font_size = max_font_size
    #    font_size = int(W / len(messages))              # 動画の解像度(横) / 字幕の文字数 フォントサイズの上限なし

        font = ImageFont.truetype(font_path, font_size)  # PILでフォントを定義
        img = Image.fromarray(img)                       # cv2(NumPy)型の画像をPIL型に変換
        draw = ImageDraw.Draw(img)                       # 描画用のDraw関数を用意
        w, h = draw.textsize(messages, font)             # .textsizeで文字列のピクセルサイズを取得


        # テロップの位置positionは画像サイズと文字サイズから決定する
        def position(line, font_size):
            if (teloppos == "top"):
                # 横幅中央、縦は上
                return  (int((W - w) / 2), int(h - (font_size * 7)))
            elif (teloppos == "center"):
                # 中央揃え
                # position = (int((W - w) / 2), int((H - h) / 2))
                return int((W - (len(line) * font_size)) / 2), int((line_counter * font_size ) + (H - h) / 2) # y座標を
            elif (teloppos == "bottom"):
                # 横幅中央、縦は下
                # return (int((W - w) / 2), int(H - (font_size * 1.5)))
                return int((W - (len(line) * font_size)) / 2), int((line_counter * font_size ) + 10) # y座標を
            
        def position(font_size):
            if (teloppos == "top"):
            # 横幅中央、縦は上
                return  (int((W - w) / 2), int(h - (font_size * 7)))
            elif (teloppos == "center"):
                # 中央揃え
                return (int((W - w) / 2), int((H - h) / 2))
            elif (teloppos == "bottom"):
                # 横幅中央、縦は下
                return (int((W - w) / 2), int(H - (font_size * 1.5)))

        # テキストを描画（位置、文章、フォント、文字色(BGR+α)を指定）
        # draw.text(position, messages, font=font, fill=(255, 255, 255, 0))
        if len(messages) > 26:
            wrap_list = textwrap.wrap(messages, int(math.ceil(len(messages) / 2)))  # テキストを13文字で改行しリストwrap_listに代入
            line_counter = 0  # 行数のカウンター
            font_size = (font_size * 2) - (len(wrap_list) * 10)
            font = ImageFont.truetype(font_path, font_size)  # PILでフォントを定義
            for line in wrap_list:  # wrap_listから1行づつ取り出しlineに代入
                # position = int((W - (len(line) * font_size)) / 2), int((line_counter * font_size ) + (H - h) / 2) # y座標をline_counterに応じて下げる

                draw.multiline_text(position(line, font_size), line, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))  # 1行分の文字列を画像に描画
                line_counter = line_counter + 1
        else:
            draw.multiline_text(position(font_size), messages, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))

        # PIL型の画像をcv2(NumPy)型に変換
        img = np.array(img)
        return img