import pandas as pd
import os
import copy
from tqdm import tqdm
import crepe

### 경로와 포맷 지정 ###
# IMPORTANT:
# Windows의 경우 경로를 '\\' 기호를 사용해야만 에러가 발생하지 않음, 
# r'path', '\', '/' 사용불가

ROOT_PATH = "E:\\Dataset2"
VOCAL_PATH=os.path.join(ROOT_PATH, "vocal")
PREDICT_OUT_PATH=os.path.join(ROOT_PATH, "predict_full")
PREDICT_RESULT_PATH=ROOT_PATH
REFINE_OUT_PATH=os.path.join(ROOT_PATH, "refine_full")
#MODEL_SIZE: "tiny", "small", "medium", "large", "full"중 선택
MODEL_SIZE="full"

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
  for root, dirs, files in os.walk(path):
    print("Exporting prediction results...")
    for file in tqdm(files):
      labelname, ext = os.path.splitext(file)
      predict_val=pd.read_csv(os.path.join(root, file))

      # 데이터 정제:
      # C2(65Hz) ~ G5(784Hz)를 벗어나는 값 버림
      predict_val.loc[predict_val.frequency<65, 'frequency']=None
      predict_val.loc[predict_val.frequency>784, 'frequency']=None

      # confidance 값이 0.7 이하일 경우 해당 pitch값 버림
      predict_val.loc[predict_val.confidence<0.5, 'frequency']=None

      # refine_out_path 파라미터가 존재할 경우 정제값 csv로 저장
      if refine_out_path is not None:
        predict_val.to_csv(os.path.join(refine_out_path, labelname)+".csv", mode='w', encoding="utf-8-sig")

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
    skip_duplicates=0
    files_n=copy.deepcopy(files)
    
    for file in files:
      # vocal 파일만 탐색
      if not "_vocals" in file:
        files_n.remove(file)
        skip_n+=1

      elif "_accompaniment" in file:
        files_n.remove(file)
        skip_n+=1
      
      #이미 예측결과 파일이 있는지 확인해서 제외
      labelname, ext = os.path.splitext(file)
      if os.path.isfile(os.path.join(out_path, labelname+".f0.csv")):
        print("Result exists, skipping", file)
        files_n.remove(file)
        skip_duplicates+=1

    # 로그 출력
    if verbose and skip_n>0 :
      print("Skipped %d files," %(skip_n+skip_duplicates))
      print("Not vocal file: %d, Result exists: %d" %(skip_n, skip_duplicates))

    print("Start predicting pitch for %d files..." %(len(files)-skip_n-skip_duplicates))
    
    # 파일 처리
    for file in tqdm(files_n):
      target_path=os.path.join(root, file)

      #seperate vocal and detect pitch 
      # try:
        #add following line in core.py in crepe to ignore true_divide error
        # np.seterr(divide='ignore', invalid='ignore')
      crepe.process_file(target_path,
                        output=out_path,
                        model_capacity=model_size,
                        save_activation=False,
                        save_plot=False,
                        plot_voicing=False,
                        step_size=100,
                        viterbi=True,
                        verbose=False)
      # except Exception as e:
      #   print("prediction failed:", file)
      #   print(e)
      #   continue

if not os.path.isdir(PREDICT_OUT_PATH):
  os.mkdir(PREDICT_OUT_PATH)

if not os.path.isdir(PREDICT_RESULT_PATH):
  os.mkdir(PREDICT_RESULT_PATH)

if not os.path.isdir(REFINE_OUT_PATH):
  os.mkdir(REFINE_OUT_PATH)

if not os.path.isdir(VOCAL_PATH):
  print("No such input directory: %s" %VOCAL_PATH)

#BASE_PATH 내의 vocal 파일들에 대해 변환 수행
else:
  predictPitch(VOCAL_PATH, PREDICT_OUT_PATH, MODEL_SIZE, verbose=True)
  pitch_result=refinePredict(PREDICT_OUT_PATH, REFINE_OUT_PATH)
  pitch_result.to_csv(os.path.join(PREDICT_RESULT_PATH, "pitch_result.csv"), mode='w', encoding="utf-8-sig")
  print("Pitch prediction result saved")