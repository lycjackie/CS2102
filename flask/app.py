#!/usr/bin/python
from flask import Flask, render_template
import psycopg2
from dbconfig import connect


app = Flask(__name__, template_folder='templates')


dbconn = connect()


@app.route('/')
def main():
    return render_template('index.html');

if __name__ == '__main__':
    app.run(debug=True)
