import json
from flask import Flask, render_template, request, flash
from utils.load import getMusicList
from utils.load import getMusicInfo
from utils.wavParser import wavParser
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

@app.route('/')
def main(upload=None):
    music_list = getMusicList()
    print(music_list[0], len(music_list))

    if (upload):
        status = upload.filename
    else: status = '음원 파일을 업로드 해주세요'
    
    return render_template('index.html', result=status, \
        music_list_json=[music for music in music_list])

@app.route('/select_music', methods=['POST'])
def select_music():
    if request.method == 'POST':
        music_name = request.get_json()['music_name']
    music_info = getMusicInfo(music_name)
    print(music_info)
    return music_info, 200

@app.route('/upload', methods = ['GET', 'POST'])
def upload_music():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename('upload.wav'))
        wavParser()
        flash('파일 업로드 완료')
    return main(f)

if __name__=='__main__':
    app.run(debug=True)