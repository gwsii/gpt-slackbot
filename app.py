import os
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
FlaskJSON(app)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/get_time')
def get_time():
    return json_response(time='now')

@app.route('/slack/event', methods=['POST'])
def slack_event():
    print(request.json['event'])
    return json_response("OK")

@app.route('/get_value')
@as_json
def get_value():
    return dict(value=42)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)