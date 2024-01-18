import whisper
import json
import math
import os

from moviepy.editor import *

model = whisper.load_model("small") #モデルの指定
import_file = "./hello.mp4"
filename_no_extension = os.path.splitext(import_file)[0]

# model = whisper.load_model("large") #モデルの指定
result = model.transcribe(import_file, verbose=True, fp16=False, language="ja") #ファイルの指定

scanStart = "カットスタート"
scanStop = "カットストップ"
cutter = [[1], [4]]
flag = False

cnt = 0
for i in result["segments"]:
    if ((i["text"] == scanStart)):
        cutter[cnt][0] = [i["start"]]
    if ((i["text"] == scanStop)):
        cutter[cnt][1] = [i["end"]]
    cnt += 1
print(cutter)
# if (len(cutter[0]) == 0 | len(cutter) % 2 != 0):
#     flag = False

def cut(target, to, start, end):
    video = VideoFileClip(target).subclip(start, end)
    video.write_videofile(to,fps=29) 

# if (flag):
for start, end in cutter[0]:
    cut(import_file, f"{filename_no_extension}-edited.mp4", start, end)