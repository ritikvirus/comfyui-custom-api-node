# api.py

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_command():
    command = request.json.get('command')
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'output': result.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode()}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)

