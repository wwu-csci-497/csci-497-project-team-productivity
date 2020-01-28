from flask import Flask, url_for, render_tepmlate, request, Response
from flask_static_compress import FlaskStaticCompress

app = Flask(__name__)
app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_STATIC_PREFIX'] = 'static'
app.config['COMPRESSOR_OUTPUT_DIR'] = 'build'
app.static_folder = 'static'
compress = FlaskStaticCompress(app)

@app.route("/", methods=['GET'])
def home():
    """Landing page"""
    return render_template('/index.html', title="Test Site")