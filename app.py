from flask import Flask, request, g, redirect, url_for, render_template, flash, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = "rajsiosorqwnejrq39834tergm4"
app.config['DATABASE'] = 'flaskr.db'
app.config['DEBUG'] = True

# connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
# close database connection

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/register')
def register():
    return render_template('register.html')
    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/<page_name>')
def other_page(page_name):
    response = make_response(render_template('404.html'), 404)
    return response
    
if __name__ == '__main__':
    app.run(debug=True)