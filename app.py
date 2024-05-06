from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signopen():
    if request.method == 'POST':
        name = request.form['signup_name']
        email = request.form['signup_email']
        city = request.form['signup_city']
        password = request.form['signup_password']
        
        vt = sqlite3.connect('database/airquality.db')
        im = vt.cursor()
        
        sql = """INSERT INTO Users (name, email, city, password) VALUES (?, ?, ?, ?)"""
        values = (name, email, city, password)
        
        im.execute(sql, values)
        
        vt.commit()
        vt.close()
        return render_template('login.html')
    return "ERROR!!! TRY AGAIN"

@app.route('/authenticate', methods = ['POST'])
def loginin():
        email = request.form['login_email']
        password = request.form['login_password']

        vt = sqlite3.connect('database/airquality.db')
        im = vt.cursor()

        sql = """SELECT * FROM Users WHERE email = ?"""
        im.execute(sql, (email,))
        
        user = im.fetchone()
        
        if user and user[3] == password:
            return render_template('login.html', logged_in = True, name = user[0], email = user[1], city = user[2], quality = is_good_air_quality(get_air_quality(user[2])))
        else:
            return "Invalid email or password"

def get_air_quality(city):
    api_token = "7bc45af7380f4262b77dec5734a43682dc5d2950"
    url = f"https://api.waqi.info/feed/{city}/?token={api_token}"

    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        air_quality_index = data['data']['aqi']
        return air_quality_index
    else:
        return None

def is_good_air_quality(air_quality_index):
    if air_quality_index is not None:
        if(air_quality_index <= 50):
            return "Good"
        if(air_quality_index <= 100):
            return "Medium"
        if(air_quality_index <= 150):
            return "Sensetive"
        if(air_quality_index <= 200):
            return "Unhealty"
        if(air_quality_index <= 300):
            return "Bad"
        if(air_quality_index <= 500):
            return "Dangerious"
    return ""

@app.route('/check_air_quality', methods = ['POST'])
def check_air_quality():
    city = request.form['city']
    air_quality_index = get_air_quality(city)
    
    if air_quality_index is not None:
        air_quality_message = is_good_air_quality(air_quality_index)
        return render_template('result.html', city = city, air_quality_message = air_quality_message)
    else:
        return render_template('error.html', city = city)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/anasayfa')
def anasayfa():
    return render_template('anasayfa.html')

if __name__ == "__main__":
    app.run(debug = True)