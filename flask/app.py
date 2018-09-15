#!/usr/bin/python
from flask import Flask, render_template
import psycopg2
from dbconfig import config


app = Flask(__name__, template_folder='templates')

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn

dbconn = connect()


@app.route('/')
def main():
    return render_template('index.html');

if __name__ == '__main__':
    app.run(debug=True)
