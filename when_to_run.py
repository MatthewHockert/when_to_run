import requests
import pandas as pd
import argparse
import os
from datetime import datetime, timedelta

api_key = os.getenv("WEATHER_API_KEY")
API_KEY = api_key
LAT, LON = 44.974323, -93.19316 

ideal_temp = (45, 65)
max_humidity = 70
max_precip = 20

def get_day(day):
    if day == "today":
        return 0
    else:
        return 1

def get_weather(day):
    day_i = get_day(day)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LAT},{LON}&days=2&aqi=no&alerts=no"
    response = requests.get(url).json()
    forecast = response['forecast']['forecastday'][day_i]['hour']
    forecast_date = datetime.strptime(forecast[0]['time'], '%Y-%m-%d %H:%M').date()

    if day == "today":
        print(f"You want to see today's weather: {forecast_date}")
    else:
        print(f"Tomorrows weather: {forecast_date}")

    return forecast

def score_hour(run_type,hour):
    # print(entry)
    temp = hour['temp_f']
    humidity = hour['humidity']
    dew_point = hour.get('dewpoint_f', 0)
    precip = hour.get('chance_of_rain', 0)
    wind = hour['wind_mph']
    dt = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
    # print(f"print raw precip {precip}")
    score = 100
    if not (ideal_temp[0] <= temp <= ideal_temp[1]):
        score -= abs(temp - sum(ideal_temp) / 2)
    if humidity > max_humidity:
        score -= (humidity - max_humidity) * 0.5
    if dew_point > 65:
        score -= (dew_point - 65) * 1.2    
    if precip > max_precip:
        score -= (precip - max_precip) * 1.5
    if run_type == 'tempo' and temp > 70:
        score -= (temp - 70) * 1.5
    if run_type == 'long' and wind > 15:
        score -= (wind - 15) * 2

    return {
        'datetime': dt,
        'score': round(score, 1),
        'temp_f': temp,
        'humidity': humidity,
        'dew_point': dew_point,
        'precip_chance': precip,
        'wind_mph': wind
    }
    
def find_best_time(run_type,day):
    forecast = get_weather(day)
    hourly_scores = [
        score_hour(run_type,hour)
        for hour in forecast
        if 6 <= datetime.strptime(hour['time'], '%Y-%m-%d %H:%M').hour <= 20
    ]
    df = pd.DataFrame(hourly_scores)
    best = df.sort_values(by='score', ascending=False).head(3)
    print(f" The top three best times to run are: {best}")
    print(best.to_string(index=False))


    best_time = best.iloc[0]['datetime']
    print(f" The best time to run is at: {best_time}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="When should you run?")
    run_types = ["tempo", "easy", "interval", "long"]
    day_choices =["today","tomorrow"]

    parser.add_argument("-r","--run_type", type=str,required=True, choices=run_types)
    parser.add_argument("-d","--day", type=str,required=True, choices=day_choices)

    args = parser.parse_args()

    find_best_time(args.run_type,args.day)
    # Testing commits