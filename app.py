from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Test app OK"


@app.route("/health")
def health():
    return {"status": "ok"}, 200
