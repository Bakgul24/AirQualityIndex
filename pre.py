import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

def get_air_quality(city):
    api_token = "7bc45af7380f4262b77dec5734a43682dc5d2950"
    url = f"https://api.waqi.info/feed/{city}/?token={api_token}"

    response = requests.get(url)
    air_quality_data = response.json()

    if 'data' in air_quality_data:
        air_quality_index = air_quality_data['data']['aqi']
        return air_quality_index, air_quality_data
    else:
        return None, None

user_city = input("Enter the city name: ")

aqi, air_quality_data = get_air_quality(user_city)

if aqi is not None:
    pm10 = air_quality_data['data']['iaqi'].get('pm10', {}).get('v', 0)
    pm25 = air_quality_data['data']['iaqi'].get('pm25', {}).get('v', 0)
    o3 = air_quality_data['data']['iaqi'].get('o3', {}).get('v', 0)
    no2 = air_quality_data['data']['iaqi'].get('no2', {}).get('v', 0)
    so2 = air_quality_data['data']['iaqi'].get('so2', {}).get('v', 0)
    co = air_quality_data['data']['iaqi'].get('co', {}).get('v', 0)

    new_input = pd.DataFrame({
        'AQI': [aqi],
        'PM10': [pm10],
        'PM25': [pm25],
        'O3': [o3],
        'NO2': [no2],
        'SO2': [so2],
        'CO': [co]
    })

    loaded_model = joblib.load("air_quality_model_rf.joblib")

    X = new_input.drop('AQI', axis=1)
    y = new_input['AQI']

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X, y)

    predicted_aqi = model.predict(X)
    print(f"Predicted AQI for {user_city} is: {predicted_aqi[0]:.2f}")

else:
    print("Hava kalitesi verisi alınamadı. Lütfen geçerli bir şehir adı girin.")
