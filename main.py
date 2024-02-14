import re

from flask import Flask, render_template, request
from graphs import load_graph
import sqlite3
app = Flask(__name__)


@app.route('/')
def render_main() -> str:
    load_graph()
    return render_template('index.html')


@app.route('/registration.html', methods=['POST'])
def registration() -> str:
    email = request.form['email']
    psw = request.form['psw']
    name = request.form['name']
    conn = sqlite3.connect('users/users.db')
    cur = conn.cursor()
    if re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        cur.execute(
            '''
            INSERT INTO names(email,password,name) VALUES(?,?,?)
            ''',
            (email, psw, name)
        )
        cur.execute(
            '''
            INSERT INTO permissions(email,admin,upload,download) VALUES(?,?,?,?)
            ''',
            (email, 0, 0, 1)
        )
        conn.commit()
    else:
        return render_template('error.html')
    conn.close()
    return render_template('index.html')


@app.route('/enter.html', methods=['POST'])
def enter() -> str:
    email = request.form['email']
    psw = request.form['psw']
    conn = sqlite3.connect('users/users.db')
    cur = conn.cursor()
    result = cur.execute(
        '''
        SELECT password, email FROM names
        WHERE password=? AND email=?
        ''',
        (psw, email)
    ).fetchall()
    if not len(result):
        return render_template('error.html')
    return render_template('index.html')


@app.route('/enter.html')
def render_enter() -> str:
    return render_template('enter.html')


@app.route('/registration.html')
def render_registration() -> str:
    return render_template('registration.html')


@app.route('/index.html')
def render_index() -> str:
    return render_template('index.html')


@app.route('/graph.html')
def render_graph() -> str:
    return render_template('graph.html')


if __name__ == '__main__':
    app.run()
