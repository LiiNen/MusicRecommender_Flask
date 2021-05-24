import json
from flask import Flask, render_template, request
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

@app.route('/select_music', methods=['POST'])
def select_music():
    return True

if __name__=='__main__':
    app.run(debug=True)