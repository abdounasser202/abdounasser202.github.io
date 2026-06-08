from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("cdm2026.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200
