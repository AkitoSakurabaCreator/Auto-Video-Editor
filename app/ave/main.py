import math
import json
from .prg.deletedir import Deletedir
from .prg.movieslice import MovieSlice
from .prg.voxconcat import VoxConcat
from .prg.voxloop import VoxLoop
from tqdm import tqdm
from pydub import AudioSegment
import whisper
import threading
import time
import random
import cv2
import numpy as np
import os
import ffmpeg
import uuid
import shutil

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
from app.models import Editor

from celery_progress.backend import ProgressRecorder

# import osos.environ['CUDA_VISIBLE_DEVICES'] = '2,1,0'

title = ""
path = ""
modelName = ""
speacker = ""
teloppos = ""
languageSel = ""
databaseid = ""
translate = ""
global progressScrore
progressScrore = 0

# --- グラフィックボードのメモリ使用上限の指定 --- #
# with open('data.json') as f:
#     json_data = json.load(f)


# ノーマライズ処理
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)
    
def main():
    
    dir = './'      # 動画が保存されているディレクトリ
    # path = path   # ファイル名
    basename = os.path.basename(path)
    basename_without_ext = os.path.splitext(os.path.basename(path))[0]
    # name = os.path.splitext(path)[0]
    step = 1                    # 動画内で処理するフレーム間隔（1より大きい整数だと動画が間引かれる）
    platform = -14

    # 音声ファイルの抽出
    stream = ffmpeg.input(path)  # 入力ファイルの指定
    stream = ffmpeg.output(stream, f'temp_{basename_without_ext}.wav')  # 出力ファイルの指定
    ffmpeg.run(stream)

    model = whisper.load_model(modelName)  # モデルの指定
    # _ = model.half()
    _ = model.cuda()
    # model = whisper.load_model("medium")  # モデルの指定
    # model = whisper.load_model("large") #モデルの指定

    result = model.transcribe(path, verbose=True, fp16=False, language=languageSel, task=translate)  # ファイルの指定
    segments = result["segments"]
    subs = []

    voiceSwitch = False

    # [文章, 開始時間, 終了時間]:ここで指定した動画内時間の範囲にテロップ文章を入れる
    messages = [
        # ['このように', 1, 4],
        # ['動画内のアクションの時間さえわかっていれば', 4.5, 11],
        # ['アクションに合わせたテロップを入れることができます', 12, 17]
    ]

    progressScrore = 20
    # [文章のみ]
    texts = []
    for i in result["segments"]:
        messages.append([i["text"], i["start"], i["end"]])

    
    for i in result["segments"]:
        texts.append([i["text"]])


    text_file = open(f'C:/Users/muramoto/Downloads/Files/Compress/zip/Extract/0728_U22/U22/media/Users/TextFile/{basename_without_ext}.txt', "wt")
    
    for i in texts:
        text_file.write(f"{i}\n")

    text_file.close()

    

    progressScrore = 30
    # Voicevoxの音声を一時的に保存するフォルダ
    vox_path = './temp/vox/'

    # フォルダの作成
    os.makedirs('temp', exist_ok=True)
    os.makedirs(vox_path, exist_ok=True)


    # 動画処理の関数を実行
    movieSlice = MovieSlice()
    movieSlice.m_slice(path, dir, step, messages, teloppos)


    sound = AudioSegment.from_file(f"temp_{basename_without_ext}.wav", "wav")
    normalized_sound = match_target_amplitude(sound, platform)
    normalized_sound.export(f"normalized_{basename_without_ext}.wav", format="wav")

    progressScrore = 40

    vox_output = 'voicevox.wav'
    if speacker != 'None':
        voiceSwitch = True
        # Voicevoxの書き出し
        voxloop = VoxLoop()
        len = voxloop.voxloop(texts, vox_path, speacker)


        inputs = [vox_path + str(n) + '.wav' for n in range(0, len)]
        vox_concat = VoxConcat()

        # 0 <-> len/2
        vox_concat.vox_concat([vox_path + str(n) + '.wav' for n in range(0, math.floor(len / 2))], vox_path + '0' + vox_output)
        # len/2 + 1 <-> len
        vox_concat.vox_concat([vox_path + str(n) + '.wav' for n in range(math.ceil(len / 2), len)], vox_path + '1' + vox_output)

        ffmpeg.concat(ffmpeg.input(vox_path + '0' + vox_output), ffmpeg.input(vox_path + '1' + vox_output), v=0, a=1).output(vox_output).run()


        # pydubによるVOICEVOX音声の音量調整(小さいので大きくしている)
        sourceAudio = AudioSegment.from_wav(vox_output)
        processedAudio = sourceAudio + 15
        processedAudio.export(vox_output, format='wav')

    progressScrore = 50

    # -------------------- 動画ファイルと音声ファイルの合成・結合処理 --------------------
    # 元動画の音声とVOICEVOXの音声合成(Overlay)
    voicePath = f"normalized_{basename_without_ext}.wav"
    sound1 = AudioSegment.from_file(f"normalized_{basename_without_ext}.wav")
    if voiceSwitch:
        sound2 = AudioSegment.from_file(vox_output)
        overlay_output = sound1.overlay(sound2, position=0)
        # 保存先の指定
        overlay_output.export(f"mixed_sounds_{basename_without_ext}.wav", format="wav")
        voicePath = f"mixed_sounds_{basename_without_ext}.wav"

    progressScrore = 80

    # ffmpeg.concat(ffmpeg.input('out_' + path), ffmpeg.input('output'), v=1, a=1).output('result_' + path).run()
    
        
    # ffmpeg.concat(ffmpeg.input('out_' + basename), ffmpeg.input(voicePath), v=1, a=1).output(f'{MEDIA_ROOT}/result_{basename}').run()
    # ffmpeg.concat(ffmpeg.input('out_' + basename), ffmpeg.input(voicePath), v=1, a=1).output(f'result_{basename}').run()
    try:
        ffmpeg.concat(ffmpeg.input('out_' + basename), ffmpeg.input(voicePath), v=1, a=1).output(f'C:/Users/muramoto/Downloads/Files/Compress/zip/Extract/0728_U22/U22/media/Users/MovieEdited/result_{basename}').run()
    except ffmpeg.Error as e:
        print("output")
        print(e.stdout)
        print("err")
        print(e.stderr)

    progressScrore = 90
    # data.edited = f'{MEDIA_ROOT}result_{basename}'
    editorId = databaseid
    data = Editor.objects.get(editorId=editorId)
    # data.edited=(f'{MEDIA_ROOT}result_{basename}')
    
    # edit = (f'Users/MovieEdited/result_{basename}')
    # new_path = shutil.move(f'result_{basename}', f'/media/Users/MovieEdited/')
    
    edit = (f'Users/MovieEdited/result_{basename}')
    text = (f'Users/TextFile/{basename_without_ext}.txt')
    data.edited=edit
    data.textFile=text
    data.save()
    progressScrore = 100
    
    # data = Editor.objects.get(m.databaseid)
    # data(edited=(f'{MEDIA_ROOT}result_{basename}'))
    # data.save()

    
    # ずんだもんと動画の合体
    # ffmpeg.concat(ffmpeg.input('result_' + path), ffmpeg.input('voicevox.wav'), v=1, a=1).output('voicevox_' + path).run()




    # from pathlib import Path
    # BASE_DIR = Path(__file__).resolve().parent.parent
    # 使用したファイルの削除
    # delete_dir = Deletedir()
    # delete_dir.delete_dir(BASE_DIR)
    