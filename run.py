from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__, static_folder='app/static', template_folder='app/template')
process = None

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/start", methods=['POST'])
def start():
    global process
    if process is None:
        process = subprocess.Popen(['python', 'app/andrew.py'])
    return redirect(url_for('gif'))

@app.route("/gif")
def gif():
    return render_template('gif.html')

@app.route("/stop", methods=['POST','GET'])
def stop():
    global process
    if process is not None:
        process.terminate()
        process = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
