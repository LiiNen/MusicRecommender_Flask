import json
from flask import Flask, render_template, request, flash
from utils.load import getMusicList
from utils.load import getMusicInfo
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

@app.route('/')
def main():
    music_list = getMusicList()
    print(music_list[0], len(music_list))
    return render_template('index.html', result='test', \
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
        f.save(secure_filename(f.filename))
        flash('파일 업로드 완료')
    return  render_template('index.html', result=f.filename)

if __name__=='__main__':
    app.run(debug=True)