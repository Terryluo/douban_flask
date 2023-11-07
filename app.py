from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/index')
def index():
    return home()


@app.route('/movies')
def movies():
    movielist = []
    connect = sqlite3.connect('./database/doubantop250.db')
    cursor = connect.cursor()

    sql = '''
        select id, chinese_title, foreign_title, rating, inq, brief_intro from doubantop250
    '''

    try:
        data = cursor.execute(sql)
        for item in data:
            movielist.append(item)
    except Exception as e:
        print('Oh, we faced problem to obtain the movielist', e)
    finally:
        cursor.close()
        connect.close()

    return render_template('movies.html', movielist=movielist)


if __name__ == '__main__':
    app.run()
