import pandas as pd
import os
from tqdm import tqdm
import crepe

#경로와 포맷 지정
ROOT_PATH = "E://Dataset2"
VOCAL_PATH=os.path.join(ROOT_PATH, "vocal")
PREDICT_OUT_PAT=+os.path.join(ROOT_PATH, "predict")

# Dataframe for saving result of pitch detection
pitch_column=['filename', 'pitch_mean', 'pitch_max']
pitch_result=pd.DataFrame([], columns=pitch_column)

def getName(meta, n, extend=""):
    """내보낼 파일 이름 생성

    Parameters
    ----------
      meta: meta값
      n: 순번 값
      (option) extend: 덧붙일 문자열
    
    Returns
    ----------
      파일명: String (포맷은 제외)
    """
    n_artist=""
    n_title=""
    if 'artist' in meta:
      n_artist=meta['artist']
    if 'title' in meta:
      n_title=meta['title']

    # remove charactors that might be problem
    removeList=",?!()&$`_'"+'"'
    for x in range(len(removeList)):
      n_artist = n_artist.replace(removeList[x],"")
      n_title=n_title.replace(removeList[x],"")

    return n+"_"+n_artist+"_"+n_title+extend

def refinePredict(path):
  """
  path에 있는 pitch 예측값 csv파일을 읽어 값 정제
  
  Parameters
  ----------
    path: 예측값 csv파일 경로
  
  Returns
  ----------
    pd.dataframe:
    {'filename':out_name, 'pitch_mean':pitch_mean, 'pitch_max':pitch_max}
  """
  pitch_column=['filename', 'pitch_mean', 'pitch_max']
  pitch_result=pd.DataFrame([], columns=pitch_column)
  for root, dirs, files in os.walk(path):
    print("Exporting prediction results...")
    for file in tqdm(files):
      labelname, ext = os.path.splitext(file)
      predict_val=pd.read_csv(os.path.join(root, file))

      # 데이터 정제:
      # C2(65Hz) ~ A5(880Hz)를 벗어나는 값 버림
      predict_val.loc[predict_val.frequency<65, 'frequency']=None
      predict_val.loc[predict_val.frequency>880, 'frequency']=None

      # confidance 값이 0.5 이하일 경우 해당 pitch값 버림
      predict_val.loc[predict_val.confidence<0.5, 'frequency']=None

      pitch_mean=predict_val['frequency'].mean()
      pitch_max=predict_val['frequency'].max()

      out_name=labelname.replace('_vocals.f0', '')+".wav"
      r = {'filename':out_name, 'pitch_mean':pitch_mean, 'pitch_max':pitch_max}

      pitch_result=pitch_result.append(r, ignore_index=True)
  
  return pitch_result

def predictPitch(path, out_path, model_size, verbose=False):
  """path에 있는 wav파일을 읽어 pitch detection 수행 후 target_path로 csv 출력
    
    Parameters
    ----------
      path: input 오디오 폴더 경로
      out_path: 내보낼 폴더 경로
      model_size: tiny, small, medium, large, full
      verbose: 로그 출력, 기본값=False
    
    Returns
    ----------
      csv, {'time', 'frequency', 'confidence'}
  """
  for root, dirs, files in os.walk(path):
    if ".DS_Store" in files:
      files.remove('.DS_Store')

    skip_n=0
    for file in files:
      #이미 예측결과 파일이 있는지 확인해서 제외
      labelname, ext = os.path.splitext(file)
      if os.path.isfile(os.path.join(PREDICT_OUT_PATH, labelname+".f0.csv")):
        print("Skip", file)
        files.remove(file)
        skip_n+=1
      
      # vocal 파일만 탐색
      elif not "_vocals" in file:
        files.remove(file)
        skip_n+=1

      elif "_accompaniment" in file:
        files.remove(file)
        skip_n+=1
    
    # 로그 출력
    if verbose and skip_n>0 :
      print("Skipped %d files" %skip_n)

    print("Start predicting pitch for %d files..." %len(files))
    
    # 파일 처리
    for file in tqdm(files):
      target_path=os.path.join(root, file)

      #seperate vocal and detect pitch 
      try:
        crepe.process_file(target_path, output=out_path,
                                        model_capacity=model_size,
                                        save_activation=False,
                                        save_plot=False,
                                        plot_voicing=False,
                                        step_size=100,
                                        viterbi=True,
                                        verbose=False)
      except:
        print("prediction failed:", file)
        continue

if not os.path.isdir(VOCAL_PATH):
  print("No such input directory: %s" %VOCAL_PATH)

if not os.path.isdir(PREDICT_OUT_PATH):
  os.mkdir(PREDICT_OUT_PATH)

#BASE_PATH 내의 vocal 파일들에 대해 변환 수행
else:
  pitch_result=refinePredict(PREDICT_OUT_PATH)

  pitch_result.to_csv("pitch_result.csv", mode='w', encoding="utf-8-sig")
  print("Pitch prediction result saved")