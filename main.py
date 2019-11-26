from flask import Flask, render_template,url_for,request,flash,redirect
from wtforms import Form,StringField,TextAreaField,TextField,validators,SubmitField
from wtforms.validators import URL
from forms import urlform
from Mongodb import collection
import matplotlib.pyplot as plt
import mpld3
from matplotlib.pyplot import figure
from mpld3 import fig_to_html,plugins

app = Flask(__name__)
app.config['SECRET_KEY'] = '7052493b8c534516ecd055cba285e55b6f7a562b39217cf3d2cec991527411490a68a06cf5f54dec59dd2ef5cf4eb48d49b2'
app.config.from_object(__name__)

@app.route("/",methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/url",methods = ['GET', 'POST'])
def geturl():
    url = request.form['url']
    Paperback_price = list()
    Paperback_date = list()
    Kindle_edition_price = list()
    Kindle_edition_date = list()
    Hardcover_price = list()
    Hardcover_date = list()
    for obj in collection.find({'url':str(url)}):
        for item in obj['Paperback']:
            Paperback_price.append(item['price'])
            Paperback_date.append(item['time'])
        for item in obj['Kindle_Edition']:
            Kindle_edition_price.append((item['price']))
            Kindle_edition_date.append((item['time']))
        for item in obj['Hardcover']:
            Hardcover_price.append(item['price'])
            Hardcover_date.append(item['time'])

    fig = figure()
    ax = fig.gca()

    ax.plot(Hardcover_date,Hardcover_price,'.-')


    mpld3.show(fig)
    return "Hi"
    # print(Paperback_price)
    # print(Kindle_edition_price)
    # print(Hardcover_price)

if __name__ == '__main__':
    app.run(debug=True)