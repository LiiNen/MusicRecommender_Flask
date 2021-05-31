from spleeter.separator import Separator
from spleeter.utils import logging
from tqdm import tqdm
import pandas as pd
import os

def separateVocals2():
  separator = Separator("spleeter:2stems")
  file_path = os.getcwd() + '/static/output.wav'
  logging.configure_logger(False)
  labelname, ext = os.path.splitext(file_path)

  try:
    separator.separate_to_file(
      file_path,
      os.getcwd() + '\\static\\output_vocal.wav',
      filename_format=labelname + "_{instrument}.{codec}",
      synchronous=True,
    )
  except Exception as e:
      print('Error processing', e)
  return