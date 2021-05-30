from spleeter.separator import Separator
from spleeter.utils import logging
from tqdm import tqdm
import pandas as pd
import os

# 경로와 포맷 지정
ROOT_PATH = "E://Dataset2"
INPUT_PATH = os.path.join(ROOT_PATH, "out")
VOCAL_OUT_PATH = os.path.join(ROOT_PATH, "vocal")
FORMAT = "wav"
SAMPLE_RATE = 16000

# Dataframe for saving result of pitch detection
pitch_column = ["filename", "pitch_mean", "pitch_max"]
pitch_result = pd.DataFrame([], columns=pitch_column)

if not os.path.isdir(VOCAL_OUT_PATH):
  os.mkdir(VOCAL_OUT_PATH)

if not os.path.isdir(INPUT_PATH):
  print("No such input directory: %s" % INPUT_PATH)

# INPUT_PATH 내의 오디오 파일들에 대해 보컬분리 수행
else:
  if __name__ == "__main__":
    separator = Separator("spleeter:2stems")
    logging.configure_logger(False)
    for root, dirs, files in os.walk(INPUT_PATH):

      if ".DS_Store" in files:
        files.remove(".DS_Store")

      # 파일 처리
      for n, file in enumerate(tqdm(files)):
        labelname, ext = os.path.splitext(file)
        target_path = os.path.join(root, file)

        out_path = os.path.join(VOCAL_OUT_PATH, labelname)
        # 이름 출력에 문제없고 이미 변환된 파일이 out폴더에 존재할 경우 변환 SKIP
        if os.path.isfile(
          os.path.join(VOCAL_OUT_PATH, labelname + "_vocals.wav")
        ):
          print("Skipping", file)
          continue

        try:
          separator.separate_to_file(
            target_path,
            VOCAL_OUT_PATH,
            filename_format=labelname + "_{instrument}.{codec}",
            synchronous=False,
          )
        except Exception as e:
          print("Error processing file", file)
          print(e)
          
