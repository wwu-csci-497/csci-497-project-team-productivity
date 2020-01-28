from flask import Flask, render_tepmlate, request, Response

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    """Landing page"""
    return render_template('/index.html', title="Test Site")