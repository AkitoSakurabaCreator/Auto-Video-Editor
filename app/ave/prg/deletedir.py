import os
import shutil

class Deletedir():
    def delete_dir (self,dir):
        os.makedirs(dir, exist_ok=True)

        with open('file.txt', 'w') as f:
            f.write('')

        # print(os.listdir('temp/'))
        # ['dir', 'test.txt']

        shutil.rmtree(dir)
        os.mkdir(dir)
        os.remove('temp.wav')
        os.remove('normalized.wav')
        os.remove('out_hello.mp4')
        os.remove('mixed_sounds.wav')
        os.remove('voicevox.wav')