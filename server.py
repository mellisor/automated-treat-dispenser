import flask
import subprocess

python_path = '/home/pi/.local/share/virtualenvs/automated-treat-dispenser-ezxVUOZ3/bin/python3.9'
script_path = '/home/pi/dev/automated-treat-dispenser/motor.py'

app = flask.Flask(__name__)

@app.route('/')
def dispense_treat():
    subprocess.call([python_path, script_path, '512', '-d', '45'])
    return ''
