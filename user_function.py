from datetime import datetime
import pytz
import requests
import json
import os
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# Set up OpenWeatherMap API key and base URL
WEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/"

def get_current_time(timezone='Asia/Ho_Chi_Minh'):
    """
    Get the current time in the specified timezone.
    Default timezone is Asia/Ho_Chi_Minh (Ha Noi, Vietnam).

    :param timezone: str, the timezone to get the current time for
    :return: str, the current time in the format 'YYYY-MM-DD HH:MM:SS'
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return current_time.strftime("%Y-%m-%d")
    except pytz.UnknownTimeZoneError:
        return "Invalid timezone specified."

def get_current_weather(city_name="Ha Noi"):
        """Lấy thông tin thời tiết hiện tại."""
        url = f"{WEATHER_BASE_URL}weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=vi"
        response = requests.get(url)
        if response.status_code != 200:
            return "Không thể lấy thông tin thời tiết."
        
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }

def get_location_by_ip():
    try:
        res = requests.get("https://ipinfo.io")
        location = res.json()
        city = location.get("city", "unknown")
        return city
    except:
        return "Ha Noi"

def initialize_ai():
    """Creates the initial AI description with the user profile."""
    date = get_current_time()
    return [
        {
            "role": "system",
            "instruction": (
                f"""You are a helpful assistant who responds to my request in a fun, friendly but professional way. 

                    Today's date is""" + date +
                    f"""
                    My location is """ + get_location_by_ip() +
                    f"""
                    the weather is """+ json.dumps(get_current_weather(get_location_by_ip())) + 
                    f"""
                    You are a personal assistant, you can help user with daily tasks, take note, search for information, and play music.
                    Start conversation with check Dailytask list, daily email, calendar to summarise for user, then give me some task list to perform
                    today task: 
                    \n{read_daily_file(date)}\n
                    User profile information: \n 
                """ + json.dumps(load_user_profile())
            ),
        }
    ]

def read_daily_file(date):
    file_path = f'daily_task/{date}.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            print(f"File '{file_path}' content:")
            return data
        except Exception as e:
            print(f"Error reading file: {e}")
            return "this day does not have any task, please create a new task for today"
    else:
        print(f"File '{file_path}' does not exist.")
        return "This day does not have any task, please create a new task for today"
    
def load_user_profile(filename: str = "user-profile.txt") -> dict:
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    
# Example usage
if __name__ == "__main__":
    print(get_current_time())  # Default timezone
    print(get_current_time('UTC'))  # UTC timezone