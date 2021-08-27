from flask import Flask
import flask
from flask.helpers import flash

app = flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)