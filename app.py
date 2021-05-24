import json
from flask import Flask,render_template
from utils.train import getResult
from utils.train import json_object
from utils.load import getMusicList

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', result='test', music_list=map(json.dumps, getMusicList()))

@app.route('/<musicinfo>')
def result(musicinfo):
    return render_template('index.html', result=getResult(int(musicinfo)))

if __name__=='__main__':
    app.run(debug=True)