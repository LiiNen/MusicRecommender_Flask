import tempfile
from pydub import AudioSegment
from pydub.utils import mediainfo
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from multiprocessing import freeze_support
from tqdm import tqdm
import numpy as np
import pandas as pd
import os
import errno
import librosa
import crepe

#경로와 포맷 지정
ROOT_PATH=os.path.join(os.path.expanduser('~'), "audio_root/")
BASE_PATH = ROOT_PATH+"original"
OUT_PATH=ROOT_PATH+"out"
OUT_VOCAL_PATH=ROOT_PATH+"out_v"
FORMAT="wav"
SAMPLE_RATE=16000

class audioConverter:
  t_sec=1000;
  t_min=t_sec*60;

  def __init__(self, src_path):
    """

    Args:
      src_path: 오디오 파일 경로
    """
    self.src_path=src_path
    self.src=AudioSegment.from_file(src_path)
    self.meta=mediainfo(target_path).get('TAG',None)
    self.waveform, _=AudioAdapter.default().load(src_path, sample_rate=SAMPLE_RATE)

  def cut_audio(self, sec_start, sec_dur):
    """시작 값에서 지정한 시간만큼 자른 오디오를 반환

    Args:
      sec_start: 자르기 시작할 시간 (단위: 초)
      sec_dur: 자를 길이 (단위: 초)
    Returns:
      자른 AudioSegment 객체
    """
    return self.src[self.t_sec*sec_start:self.t_sec*sec_start+self.t_sec*sec_dur]

  def extract_vocal_by_file(self, outPath, outName, option=2):
    """오디오에서 보컬과 배경음악을 분리해서 파일로 출력

    Args:
      outPath: 출력 경로
      outName: 출력 이름
      (option) option: 분리할 채널 수, default=2
    """
    #2stems: vocal + background music
    separator = Separator('spleeter:%sstems' %str(option))
    separator.separate_to_file(self.src_path, outPath, filename_format=outName+"_{instrument}.{codec}")

  def extract_vocal(self, option=2):
    """오디오에서 보컬과 배경음악을 분리

    Args:
      outPath: 출력경로
      (option) option: 분리할 채널 수, default=2

    Returns:
      Numpy array가 담긴 dictionary ({'vocals'}, {'accompaniment'})
    """
    freeze_support()
    #2stems: vocal + background music
    separator = Separator('spleeter:%sstems' %str(option))
    prediction = separator.separate(self.waveform)

    return prediction

  def pitch_detect(self, out_name="out", model_size="small"):
    """Pitch값 판단
    
    Args:
      out_name: (optional) 내부에서 임시로 사용할 파일명
      model_capacity: tiny', 'small', 'medium', 'large', 'full'

    Returns: 
      Tuple (time: np.ndarray [shape=(T,)]
        frequency: np.ndarray [shape=(T,)]
        activation: np.ndarray [shape=(T, 360)]
        )
    """

    with tempfile.TemporaryDirectory() as temp_path:
      #temp_path.{out_name}_vocals.wav 이름으로 임시공간에 출력
      self.extract_vocal_by_file(temp_path, out_name)
      temp_path_out=os.path.join(temp_path, out_name+"_vocals.wav")

      #임시공간에 있는 파일로 pitch detect
      prediction = crepe.process_file(temp_path_out, output=temp_path, model_capacity=model_size, save_activation=False, save_plot=False, plot_voicing=False, step_size=100, viterbi=False)
      predicted_path=os.path.join(temp_path, out_name+"_vocals.f0.csv")
      predict_val=np.transpose(np.genfromtxt(predicted_path, delimiter=",", dtype=float, skip_header=1))

    return (predict_val[0], predict_val[1], predict_val[2])

  def getName(self, n, extend=""):
    """내보낼 파일 이름 생성

    Args:
      n: 순번 값
      (option) extend: 덧붙일 문자열
    Returns:
      파일명 String (포맷은 제외)
    """
    n_artist=self.meta['artist']
    n_title=self.meta['title']

    # remove charactors that might be problem
    removeList=",?!()&`_'"+'"'
    for x in range(len(removeList)):
      n_artist = n_artist.replace(removeList[x],"")
      n_title=n_title.replace(removeList[x],"")

    return n+"_"+n_artist+"_"+n_title+extend

if __name__ == '__main__':
  # Dataframe for saving result of pitch detection
  pitch_column=['filename', 'pitch_mean', 'pitch_max']
  pitch_result=pd.DataFrame([], columns=pitch_column)

  if not os.path.isdir(OUT_PATH):
    os.mkdir(OUT_PATH)

  if not os.path.isdir(BASE_PATH):
    print("No such input directory: %s" %BASE_PATH)

  #BASE_PATH 내의 오디오 파일들에 대해 변환 수행
  else:
    for root, dirs, files in os.walk(BASE_PATH):

      if ".DS_Store" in files:
        files.remove('.DS_Store')

      # 파일 처리
      for n, file in enumerate(tqdm(files)):
        n=str(n).zfill(4)
        labelname, ext = os.path.splitext(file)
        target_path=os.path.join(root, file)
        meta=mediainfo(target_path).get('TAG',None)

        # import audio file
        ac=audioConverter(target_path)

        #set names
        out_name=ac.getName(n)
        out_name_f=out_name+"."+FORMAT
        out_path=os.path.join(OUT_PATH, out_name_f)
        out_path_v=os.path.join(OUT_VOCAL_PATH, out_name_f)

        """
        # 이름 출력에 문제없고 이미 변환된 파일이 out폴더에 존재할 경우 변환 SKIP
        if out_name and os.path.isfile(out_path):
          print("Skipping", out_name)
          continue
        """
        #seperate vocal and detect pitch
        pitch_time, pitch_val, pitch_act=ac.pitch_detect(out_name)

        pitch_mean=pitch_val.mean()
        pitch_max=pitch_val.max()

        r = {'filename':out_name_f, 'pitch_mean':pitch_mean, 'pitch_max':pitch_max}
        pitch_result = pitch_result.append(r, ignore_index=True)

        #convert & export wav
        sound_cut=ac.cut_audio(60, 60)
        try:
          sound_cut.export(out_path, format=FORMAT, tags=meta, parameters=["-ar", str(SAMPLE_RATE), "-ac", "1"])
        except TypeError as t:
          print('TypeError in parameter:', t)
        except Exception as e:
          #이름 출력에 문제있는 경우
          if e.errno and e.errno == errno.EISDIR:
            print("Directory Error:")
            print(e)
          #그 밖의 경우
          else:
            print("Error processing ", n, "\n", e)

  pitch_result.to_csv("pitch_result.csv", mode='w')
  print("Pitch result saved")