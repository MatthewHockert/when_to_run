A simple command-line tool that helps you decide the best time to run today or tomorrow, based on weather conditions in your city.

Powered by the [WeatherAPI](https://www.weatherapi.com/) and [OpenStreetMap Nominatim](https://nominatim.org/), this script scores each hour of the day using temperature, humidity, dew point, precipitation chance, and wind.

---

## Features

- Scores each hour of the day from 6 AM to 8 PM  
- Takes into account run type (e.g., tempo, long, easy, interval)  
- Supports any city name (uses geocoding for coordinates)  
- Optionally uses environment variables for sensitive information  
- Outputs a table of the top 3 recommended run times and the best time to run

## Getting Started

### 1. Clone/fork the repo

```bash
git clone https://github.com/MatthewHockert/when-to-run.git
cd when-to-run
```

### 2. Install dependencies

```python 
pip install pandas requests argparse os datetime
```

### 3. Set up your environment variables

You’ll need a WeatherAPI key and optionally a default lat/lon pair.

Place in your .bash_profile or .zshrc

```bash 
export WEATHER_API_KEY=your_api_key
export LAT_LON="38.3234,-75.9463" #example
export EMAIL=your_email@example.com 
```

Then reload your shell:

```bash
source ~/.bash_profile
```

## How to use

```bash
python when_to_run.py -r [run_type] -d [day] [-l "City, State"]
```

Required:
	•	-r, --run_type: one of tempo, easy, interval, long
	•	-d, --day: today or tomorrow

 Optional:
	•	-l, --location: any city name (e.g., "Seattle, WA"). If omitted, uses the default coordinates from LAT_LON that you need to set. Can also use the city name alone.

```bash
 python when_to_run.py -r tempo -d today -l "Seattle, WA"
```

## Output

```
You want to see today's weather: 2025-04-21
 The top three best times to run are: 
           datetime  score  temp_f  humidity  dew_point  precip_chance  wind_mph
2025-04-21 13:00:00  100.0    51.4        68       40.8              0       5.1
2025-04-21 14:00:00  100.0    52.7        55       38.1              0       6.7
2025-04-21 15:00:00  100.0    53.6        58       39.4              0       7.4
 The best time to run is at: 2025-04-21 13:00:00
 ```














