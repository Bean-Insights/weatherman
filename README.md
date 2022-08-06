# weatherman_october_2021
This repository is designed to reduce the processing time and cost of purchasing openweather's data for UK, Germany and Netherlands by scraping data from openweather using openweather API.



## Scripts

### Web scraper

Web scrape OpenWeather website using **"weather_api_call.py"**. This script scrapes for UK, Germany and Netherlands. The output of this are transformed and updated dataframes which are appended to the datasets below:

- germany_weather.csv
- netherlands_weather.csv
- uk_weather.csv



To run the script above in Git bash:
`# change the wd to where your script is located in the config.yml file`
`cd 'C:\Users\AndreaC\OneDrive - Ceuta Group\Documents\Python Scripts\Weather'`

`# activate the venv`
`. ~/.virtualenvs/AndreaC-0Sg8PFSf/Scripts/activate`

`# replace the input_data in the config file to the current wd`

`# run the python script`
`python scripts/weather_api_call.py`

`# cancel the script during scheduling, when you see 'All done!'`
`Ctrl + C`


### Data Transformer

**"Weather_Data_Processing.py"** script transforms the (uk_weather.csv) above to a dataset which contains the following variables:

- week_ending: the first day of the week, usually Monday to Sunday.
- temp: average temperature during the week
- temp_min: lowest temp during the week
- temp_max: highest temp during the week



## To-do 

- Write unit tests
- Automate web scraping and data transformation using cloud resources.


## Contacts 

- Tayo Ososanya - Data Scientist
- Andrea Ciufo - Data Scientist



## License

- Copyright belongs to CollidaScope Limited. The contents of this repository must not be reused without permission.

