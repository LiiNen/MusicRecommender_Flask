import json
from flask import Flask, render_template, request, flash
from utils.load import getMusicList
from utils.load import getMusicInfo
from utils.wavParser import wavParser
from werkzeug.utils import secure_filename
from utils.getFeature import getFeature

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

# 메인
@app.route('/')
def main(upload=None):
    music_list = getMusicList()

    search_input = 'true'
    result_href = ''
    if (upload):
        status = upload.filename
        search_input = 'false'
        result_href = 'upload'
    else: status = '음원 파일을 업로드 해주세요'
    
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
    print(music_info)
    return music_info, 200

# 파일 업로드 후 메인 호출
@app.route('/upload', methods = ['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename('upload.wav'))
        wavParser()
        getFeature()
    return main(f)

# 결과 페이지 호출
@app.route('/result')
def result_page():
    search_type = request.args.get('type')
    return render_template('result.html', search_type = search_type)

if __name__=='__main__':
    app.run(debug=True)