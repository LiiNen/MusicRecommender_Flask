import json
from flask import Flask,render_template
from utils.train import getResult
from utils.train import json_object
from utils.load import getMusicList

app = Flask(__name__)

@app.route('/')
def main():
    music_list = getMusicList()
    print(music_list[0], len(music_list))
    return render_template('index.html', result='test', \
        music_list_json=[music for music in music_list])

@app.route('/<musicinfo>')
def result(musicinfo):
    return render_template('index.html', result=getResult(int(musicinfo)))

if __name__=='__main__':
    app.run(debug=True)