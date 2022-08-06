"""
Run script using python scripts/weather_api_call.py in a suitable env
This will update the weather datasets with the latest historical data
"""

from datetime import datetime
import time
import json
from click import format_filename
import schedule
import pandas as pd
import requests
import pytz
import yaml
import os


# get the path to the config.yml file
path = os.getcwd()
configfile= 'scripts/config.yml'
file_path = os.path.join(path,configfile)


# read in the config file
with open(file_path, 'r') as file:
    data_config = yaml.safe_load(file)


# input raw data link
df_data_link = data_config['input_data']


# ----- Functions -----
def create_6days_list(no_of_days=6):
    """
    Create a list of timestamps with the first being the immediate timestamp and\
         the remaining 5 for the 5 previous days.

    Keyword arguments:
    no_of_days -- the total number of days you want timestamps for (default 6)
    """
    a_day = 86400
    day0 = datetime.timestamp(datetime.now())
    past_6_days = []

    for i in range(no_of_days):
        one_day = int(day0) - int(a_day * i)
        past_6_days.append(one_day)
    return past_6_days

past_6_days_list = create_6days_list(6)


def get_historical_weather(
    lat=51.17,
    lon=10.45,
    api_key=data_config['api_key'],
    past_6_days=past_6_days_list,
):
    """
    Returns a dataframe with dt and temp columns.

    Keyword arguments:
    lat -- the latitude (default 51.17)
    lon -- the longitude (default 10.45)
    api_key -- api key gotten from openweathermap
    past_6_days -- a list of timestamps for the 6 days you want historical data for
    """
    new_df = pd.DataFrame()
    past_6_days_df = pd.DataFrame()

    for day in past_6_days:
        url = (
            "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=%s&lon=%s&dt=%s&units=metric&appid=%s"
            % (lat, lon, day, api_key)
        )
        response = requests.get(url)
        data = json.loads(response.text)
        hourly_data = data["hourly"]

        for entry in hourly_data:
            temp = pd.DataFrame.from_dict(pd.json_normalize(entry), orient="columns")

            # select only nec. columns
            columns = ["dt", "temp"]
            temp = temp[columns]

            # transform dt column
            temp["dt"] = datetime.fromtimestamp(entry["dt"], pytz.utc)
            new_df = new_df.append(temp, ignore_index=True)

        # concatenate each day in a new dataframe
        past_6_days_df = pd.concat(
            [past_6_days_df, new_df], axis=0, ignore_index=False
        ).drop_duplicates()

    return past_6_days_df


# Run this to append new entries

def job():
    """
    Prints 'Almost there' when the function has been invoked.
    If 'All done' prints, this means the datasets have been\
updated with the latest historical temp data.
    You can change the data_path below.
    """

    print("Almost there!")

    data_path = df_data_link

    germany = get_historical_weather(
        api_key=data_config['api_key'], lat=51.17, lon=10.45
    )
    pd.read_csv(data_path + data_config['germany_weather_data'], index_col=False).set_index(
        ["dt"]
    ).append(germany.set_index(["dt"])).drop_duplicates().to_csv(
        data_path + data_config['germany_weather_data']
    )

    netherlands = get_historical_weather(
        api_key=data_config['api_key'], lat=52.13, lon=5.29
    )
    pd.read_csv(data_path + data_config['netherlands_weather_data'], index_col=False).set_index(
        ["dt"]
    ).append(netherlands.set_index(["dt"])).drop_duplicates().to_csv(
        data_path + data_config['netherlands_weather_data']
    )

    uk = get_historical_weather(
        api_key=data_config['api_key'], lat=52.35, lon=-1.17
    )
    pd.read_csv(data_path + data_config['uk_weather_data'], index_col=False).set_index(["dt"]).append(
        uk.set_index(["dt"])
    ).drop_duplicates().to_csv(data_path + data_config['uk_weather_data'])

    print("All done!")

# Run job once
job()


# # Schedule Jobs ----- SCHEDULER -----
# # schedule.every().day.at("15:49").do(job)
# schedule.every(5).seconds.do(job)
# # schedule.every().day.at("11:07").do(job)
# # schedule.every(240).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(5)
