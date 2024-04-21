from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_air_quality', methods=['POST'])
def check_air_quality():
    city = request.form['city']
    air_quality_index = get_air_quality(city)
    
    if air_quality_index is not None:
        air_quality_message = is_good_air_quality(air_quality_index)
        return render_template('result.html', city=city, air_quality_message=air_quality_message)
    else:
        return render_template('error.html', city=city)

if __name__ == "__main__":
    app.run(debug=True)