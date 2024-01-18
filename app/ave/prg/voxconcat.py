import wave

# --- VOICEVOX --- #
class VoxConcat():
    def vox_concat(self,inputs, output):
        '''
        inputs : list of filenames
        output : output filename
        '''
        try:
            fps = [wave.open(f, 'r') for f in inputs]
            fpw = wave.open(output, 'w')

            fpw.setnchannels(fps[0].getnchannels())
            fpw.setsampwidth(fps[0].getsampwidth())
            fpw.setframerate(fps[0].getframerate())

            for fp in fps:
                fpw.writeframes(fp.readframes(fp.getnframes()))
                fp.close()
            fpw.close()

        except wave.Error as e:
            print(e)

        except Exception as e:
            print('unexpected error -> ' + str(e))