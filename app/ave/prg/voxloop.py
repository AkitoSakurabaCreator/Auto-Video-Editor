import requests # APIを使う
import json # APIで取得するJSONデータを処理する
import pyaudio # wavファイルを再生する
import time # タイムラグをつける

class VoxLoop:
    def voxloop(self,messages, path, speaker):
        cnt = 0
        for message in messages:
            # 音声合成クエリの作成
            res1 = requests.post('http://127.0.0.1:50021/audio_query_from_preset?preset_id=1',params = {'text': message, 'speaker': 1})
            # 音声合成データの作成
            res2 = requests.post('http://127.0.0.1:50021/synthesis',params = {'speaker': speaker},data=json.dumps(res1.json()))
            # wavデータの生成
            with open(f'{path}{cnt}.wav', mode='wb') as f:
                f.write(res2.content)
                f.close()
            cnt += 1
        return cnt