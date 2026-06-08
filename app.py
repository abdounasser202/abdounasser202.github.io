from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(
        app.static_folder, path, headers={"X-Content-Type-Options": "nosniff"}
    )


@app.route("/")
def index():
    return render_template("cdm2026.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200
