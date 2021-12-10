from flask import Flask, request, jsonify
import warnings
from util.client.JudgeComponent import JudgeComponent
import os

warnings.filterwarnings("ignore")

app = Flask(__name__)


@app.route("/judge", methods=['GET', 'POST'])
def detect_bug():
    json_data = request.get_json()
    info = json_data['word']
    result, pos = JudgeComponent.get_instance().judge(info)
    str_result = 'bug' if result else 'feature'
    return jsonify({'result': str_result, 'probability': pos})


if __name__ == '__main__':
    app.run(debug=True)
