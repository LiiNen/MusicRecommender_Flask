# MusicRecommender_Flask
## Initiation
 - git clone
 - cd project
 - pip install -r requirements.txt

## Web development
 - set FLASK_ENV=development
 - python app.py

## Using Audio Utilities
```
오디오 처리에 사용하는 Spleeter와 Crepe는 **Tensorflow**와 **Keras**를 사용하므로
가상환경을 사용중일 경우 반드시 고려해주세요!
```
- FFmpeg 설치: <https://hello-bryan.tistory.com/230> 링크 참조
- WAV 변환: utils/wavParser.py
  - 기능
    - 지정한 디렉토리 내의 오디오 파일을 원하는 길이만큼 편집
    - 지정한 디렉토리 내의 오디오 파일을 WAV로 변환
  - 변수
    - ROOT_PATH: 상위 폴더 경로 지정
    - BASE_INPUT_PATH: ROOT_PATH 아래의 원본 폴더명
    - BASE_OUTPUT_PATH: 변환한 WAV 출력할 폴더명
- 보컬 분리: utils/separateVocals.py
 - 기능
   - Spleeter를 사용하여 지정한 디렉토리 내의 오디오 파일을 보컬과 배경음악으로 분리
 - 변수
    - ROOT_PATH: 상위 폴더 경로 지정
    - INPUT_PATH: ROOT_PATH 아래의 WAV파일 폴더명
    - VOCAL_OUT_PATH: 보컬 분리한 파일 출력할 폴더명
- 음정 분석: utils/createPitchList.py
 - 기능
   - Crepe를 사용하여 지정한 디렉토리 내의 오디오 파일의 Pitch값을 0.1초 단위로 분석
   - 분석결과 csv로 저장
   - 분석결과에서 더 나은 결과를 위해 데이터 정제 (Optional: 정제값 csv로 저장)
   - 분석결과(혹은 정제결과)를 바탕으로 Pitch mean, max값을 산출하여 단일 csv로 저장
 - 변수
    - ROOT_PATH: 상위 폴더 경로 지정
    - VOCAL_PATH: 보컬 분리된 파일이 있는 폴더명
    - PREDICT_OUT_PATH: 음정 예측을 돌린 csv 파일 저장 폴더명
    - PREDICT_RESULT_PATH: 모든 음정 예측값을 정리한 단일파일 출력 폴더명
    - REFINE_OUT_PATH: (Optional) 음정 예측값을 보정한 후의 csv 파일 저장 폴더명