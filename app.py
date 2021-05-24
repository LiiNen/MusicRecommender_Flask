from flask import Flask,render_template
from utils.train import getResult

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', result=getResult(0))

@app.route('/<musicinfo>')
def result(musicinfo):
    return render_template('index.html', result=getResult(int(musicinfo)))

if __name__=='__main__':
    app.run(debug=True)