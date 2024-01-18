from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from moviepy.config import change_settings
change_settings({"FFMPEG_BINARY":"ffmpeg"})

import numpy as np
import os

in_path = ".\output.mp4"
output_filename = f"crossfade.{os.path.splitext(in_path)[1]}"
codec='libx264'
audio_codec='aac'
temp_audiofile='temp-audio.m4a'
threads=8

def fade():
    fade_duration = 2

    clip1 = VideoFileClip(in_path).subclip("00:00:00", "00:00:02")
    clip1 = clip1.crossfadeout(fade_duration).audio_fadeout(fade_duration)

    duration = clip1.duration
    # print(duration)

    clip2 = VideoFileClip(in_path).subclip("00:00:02", "00:02:19").set_start(duration)
    clip2 = clip2.crossfadein(fade_duration).audio_fadein(fade_duration)
    

    final_clip = CompositeVideoClip([clip1, clip2])

    final_clip.write_videofile(
        f"fade_{output_filename}",
        codec=codec, 
        audio_codec=audio_codec, 
        temp_audiofile=temp_audiofile, 
        remove_temp=True,
        threads=threads
    )

def dissolve():
    def crossdissolve(c1, c2):
        video_fade_duration = 0.3
        audio_fade_duration = 1

        c1 = c1.crossfadeout(video_fade_duration).audio_fadeout(audio_fade_duration)
        duration = c1.duration
        print(duration)
        c2 = c2.set_start(duration - video_fade_duration * 2)
        c2 = c2.crossfadein(video_fade_duration).audio_fadein(audio_fade_duration)


        return CompositeVideoClip([c1, c2])

    clip1 = VideoFileClip(in_path).subclip("00:00:00", "00:00:02")
    clip2 = VideoFileClip(in_path).subclip("00:00:02", "00:02:19")

    final_clip = crossdissolve(clip1, clip2)

    final_clip.write_videofile(
        f"dissolve_{output_filename}",
        codec=codec, 
        audio_codec=audio_codec, 
        temp_audiofile=temp_audiofile, 
        remove_temp=True,
        threads=threads # =CPU Core
    )

def telopAnime():
    video_clip = VideoFileClip("in.mp4").subclip("00:07:20", "00:07:25")
    screensize = video_clip.size # (1280, 720)

    text_clip = TextClip('HAL TOKYO\nRecycle!', color = 'white', font = "フォントをいれろ！！！", kerning = 5, fontsize = 80)
    text_clip = text_clip.set_pos('center')
    cvc = CompositeVideoClip([text_clip], size = screensize)

    # helper function
    rotMatrix = lambda a: np.array( [[np.cos(a), np.sin(a)],
                                    [-np.sin(a), np.cos(a)]] )


    def effect(screenpos, i, nletters):
        
        # damping
        d = lambda t : 1.0/(0.3 + t**8)
        # angle of the movement
        a = i * np.pi / nletters
        
        # using helper function
        v = rotMatrix(a).dot([-1, 0])
        
        if i % 2 : v[1] = -v[1]
            
        # returning the function
        return lambda t: screenpos + 400 * d(t)*rotMatrix(0.5 * d(t)*a).dot(v)
    

    letters = findObjects(cvc) # Returns a list of ImageClips representing each a separate object on the screen.


    text_clip = CompositeVideoClip([letter.set_pos(effect(letter.screenpos, i, len(letters))) for i, letter in enumerate(letters)], size = screensize)
    text_clip = text_clip.subclip(0, 4)
    text_clip.fps = 24


    final_clip = CompositeVideoClip([video_clip, text_clip])  

    final_clip.write_videofile(
        f"fade_{output_filename}",
        codec=codec, 
        audio_codec=audio_codec, 
        temp_audiofile=temp_audiofile, 
        remove_temp=True,
        threads=threads
    )

if __name__ == "__main__":
    # fade()
    # dissolve()
    # telopAnime()