from pydub import AudioSegment
from pydub.utils import mediainfo
import os
import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import csv
import sklearn

FORMAT="wav"
t_sec=1000
t_min=t_sec*60

def cut_audio(sound_, sec_start, sec_dur):
  """
  시작 값에서 지정한 시간만큼 자른 오디오를 반환

  :sound_: 오디오 객체
  :sec_start: 자르기 시작할 시간 (단위: 초)
  :sec_dur: 자를 길이 (단위: 초)
  """
  return sound_[t_sec*sec_start:t_sec*sec_start+t_sec*sec_dur]

def wavParser():
    file_path = os.getcwd() + '/upload.wav'
    print(file_path)

    sound = AudioSegment.from_file(file_path)
    sound_cut = cut_audio(sound, 60, 30)
    try:
        sound_cut.export(os.getcwd() + '\\static\\output.wav', format=FORMAT, tags=None, parameters=["-ar", "22000", "-ac", "1"])
    except Exception as e:
        print('Error processing', e)
    return

if __name__ == '__main__':
    wavParser()