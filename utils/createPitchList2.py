import pandas as pd
import os
import copy
from tqdm import tqdm
import crepe
import csv

pitch_column=['filename', 'pitch_mean', 'pitch_max']
MODEL_SIZE="full"

def refinePredict(path, refine_out_path=None):
  """
  path에 있는 pitch 예측값 csv파일을 읽어 값 정제
  
  Parameters
  ----------
    path: 예측값 csv파일 경로
    refine_out_path: (optional) 정제한 값 csv로 저장하고자 할 때의 저장경로
  
  Returns
  ----------
    pd.dataframe:
    {'filename':out_name, 'pitch_mean':pitch_mean, 'pitch_max':pitch_max}
  """
  pitch_column=['filename', 'pitch_mean', 'pitch_max']
  pitch_result=pd.DataFrame([], columns=pitch_column)
  labelname, ext = os.path.splitext(path)
  predict_val=pd.read_csv(path)
  predict_val.loc[predict_val.frequency<65, 'frequency']=None
  predict_val.loc[predict_val.frequency>784, 'frequency']=None
  predict_val.loc[predict_val.confidence<0.5, 'frequency']=None

  pitch_mean=predict_val['frequency'].mean()
  pitch_max=predict_val['frequency'].max()
  pitch_column=['pitch_mean', 'pitch_max']
  pitch_result=pd.DataFrame([], columns=pitch_column)
  r = {'pitch_mean':pitch_mean, 'pitch_max':pitch_max}
  pitch_result=pitch_result.append(r, ignore_index=True)
  return pitch_result

def predictPitch(path, out_path, model_size, verbose=False):
  crepe.process_file(path, output=out_path, model_capacity=model_size, save_activation=False, save_plot=False, plot_voicing=False, step_size=100, viterbi=True, verbose=False)

def createPitchList2():
  predictPitch(os.getcwd() + '/static/output_vocals.wav', os.getcwd() + '/static', MODEL_SIZE, verbose=True)
  pitch_result=refinePredict(os.getcwd() + '/static/output_vocals.f0.csv')
  pitch_result.to_csv(os.getcwd() + "/static/pitch_result.csv", mode='w', encoding="utf-8-sig")

def getPitch():
  with open('./static/pitch_result.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    i = 0
    rdata = []
    for l in r:
      if i == 0:
        i+=1
        continue
      rdata.append(l[1])
      rdata.append(l[2])
  return rdata
