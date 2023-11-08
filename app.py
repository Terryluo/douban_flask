from flask import Flask, render_template
import sqlite3
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

app = Flask(__name__)

picture = False
textlength = 0

@app.route('/')
def home():  # put application's code here
    global picture
    if not picture:
        getwords()
        picture = True
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


@app.route('/rating')
def rating():
    ratinglist = []
    countlist = []
    connect = sqlite3.connect('database/doubantop250.db')
    cursor = connect.cursor()

    sql = '''
        select rating, count(rating) from doubantop250 group by rating
    '''
    try:
        rating = cursor.execute(sql)
        for rate in rating:
            ratinglist.append(rate[0])
            countlist.append(rate[1])
    except Exception as e:
        print('Exception was thrown when obtaining the rating data', e)
    finally:
        cursor.close()
        connect.close()

    return render_template('rating.html', ratinglist=ratinglist, countlist=countlist)


@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')


def getwords():
    text = ''
    global textlength
    connect = sqlite3.connect('database/doubantop250.db')
    cursor = connect.cursor()

    sql = '''
        select inq from doubantop250
    '''
    try:
        inq = cursor.execute(sql)
        for sentence in inq:
            text += sentence[0].strip()
        cut = jieba.cut(text)
        textlist = ' '.join(cut).replace('的','').replace('是','').replace('了','')
        textlength = len(textlist)
        # print(textlist)
        # print(len(textlist))

        img = Image.open('static/assets/img/tree.jpg')
        img_array = np.array(img)
        wc = WordCloud(
            background_color='white',
            mask=img_array,
            font_path="STXINWEI.TTF"  # 华文新魏 常规
        )
        wc.generate_from_text(textlist)

        fig = plt.figure(1)
        plt.imshow(wc)
        plt.axis('off')  # don't show the axies
        # plt.show()
        plt.savefig('static/assets/img/wordcloud.jpg', dpi=500)
    except Exception as e:
        print('We faced problem when creating the word cloud', e)
    finally:
        cursor.close()
        connect.close()


if __name__ == '__main__':
    app.run()
