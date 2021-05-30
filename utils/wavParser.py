from pydub import AudioSegment
from pydub.utils import mediainfo
from tqdm import tqdm
import os

FORMAT = "wav"
ROOT_PATH = "/Volumes/My Passport B/Dataset2"
BASE_INPUT_PATH = ROOT_PATH + "/test"
BASE_OUTPUT_PATH = ROOT_PATH + "/out"
SAMPLE_RATE = 16000
t_sec = 1000
t_min = t_sec * 60


def getName(path, n=0, extend=""):
  """내보낼 파일 이름 생성

  Parameters
  ----------
    path: 새 이름을 생성할 원본파일 경로
    n: (option)순번 값
    extend: (option) 덧붙일 문자열

  Returns
  ----------
    파일명: String (포맷은 제외)
  """
  if n < 10000:
    n = str(n).zfill(4)

  n_artist = ""
  n_title = ""
  output = ""
  meta = mediainfo(path)

  if "artist" in meta["TAG"]:
    n_artist = meta["TAG"]["artist"]
  if "title" in meta["TAG"]:
    n_title = meta["TAG"]["title"]

  # remove charactors that might be problem
  removeList = ",?!()&`#_'" + '"'
  for x in range(len(removeList)):
    n_artist = n_artist.replace(removeList[x], "")
    n_title = n_title.replace(removeList[x], "")

  # create new name
  if n != 0:
    output += "{}_".format(n)
  output += "{}_{}{}".format(n_artist, n_title, extend)

  return output


def cut_audio(sound_, sec_start, sec_dur=30, option=0):
  """시작 값에서 지정한 시간만큼 자른 오디오를 반환

  Parameters
  ----------
    sound_: 오디오 객체
    sec_start: 자르기 시작할 시간 (단위: 초)
    sec_dur: 자를 길이 (단위: 초)
    option: default=0, 파일 끝까지=1 (sec_dur 무시)

  Returns
  ----------
    자른 AudioSegment 객체

  args 값이 잘못된 경우 자르지 않고 그대로 반환
  """
  if t_sec * sec_start <= len(sound_):
    if option == 1:
      return sound_[t_sec * sec_start :]
    elif t_sec * (sec_start + sec_dur) > len(sound_):
      return sound_
    else:
      return sound_[t_sec * sec_start : t_sec * (sec_start + sec_dur)]
  else:
    return sound_


def wavParser():
  for root, dirs, files in os.walk(BASE_INPUT_PATH):
    if ".DS_Store" in files:
      files.remove(".DS_Store")
    # 파일 처리
    for n, file in enumerate(tqdm(files)):
      target_path = os.path.join(root, file)
      sound = AudioSegment.from_file(target_path)
      sound_cut = cut_audio(sound, 50, 40)
      sound_name = getName(target_path, n)
      out_path = os.path.join(BASE_OUTPUT_PATH, sound_name + "." + FORMAT)

      try:
        sound_cut.export(
          out_path,
          format=FORMAT,
          tags=mediainfo(target_path)["TAG"],
          parameters=["-ar", str(SAMPLE_RATE), "-ac", "1"],
        )
      except Exception as e:
        print("Error converting {}:".format(file), e)

      # TODO: 태그 한글이 깨짐


if __name__ == "__main__":
  if not os.path.isdir(BASE_INPUT_PATH):
    print("No such directory:", BASE_INPUT_PATH)
  if not os.path.isdir(BASE_OUTPUT_PATH):
    print("Create new output directory:", BASE_OUTPUT_PATH)
    os.mkdir(BASE_OUTPUT_PATH)

  wavParser()
