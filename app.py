import json
from flask import Flask, render_template, request, flash
from utils.load import getMusicList
from utils.load import getMusicInfo
from utils.wavParser import wavParser2
from werkzeug.utils import secure_filename
from utils.getFeature import getFeature
from utils.modelPredict import modelPredict
import time
import os
from utils.createPitchList2 import createPitchList2
from utils.createPitchList2 import getPitch

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

# 메인
@app.route('/')
def main(upload=None, wav=None, get=None):
    music_list = getMusicList()

    search_input = 'true'
    result_href = ''
    if (upload):
        status = upload.filename
        search_input = 'false'
        result_href = 'upload'
    else: status = '좋아하는 노래를 알려주세요!'
    return render_template('index.html', result=status, \
        music_list_json=[music for music in music_list], \
        search_input_bool=search_input, \
        result_href = result_href)

# 파일 첨부
@app.route('/select_music', methods=['POST'])
def select_music():
    if request.method == 'POST':
        music_name = request.get_json()['music_name']
    music_info = getMusicInfo(music_name)
    return music_info, 200

pitch_mean_max = []
# 파일 업로드 후 메인 호출
@app.route('/upload', methods = ['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename('upload.wav'))
        wav = wavParser2()
        os.system('python utils/separateVocals2.py')
        get = getFeature() # 로딩 필요
        createPitchList2()
    return main(f, wav, get)

# 결과 페이지 호출
@app.route('/result')
def result_page():
    search_type = request.args.get('type')
    result_list = modelPredict(search_type) # 로딩 필요
    pitch_mean_max = getPitch()
    return render_template('result.html', search_type = search_type, \
        predict_result_list = [result for result in result_list], \
        mean_max = [pitch for pitch in pitch_mean_max])

if __name__=='__main__':
    app.run(debug=True)