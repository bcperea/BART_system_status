import requests
from lxml import etree
import json
import pandas as pd


def call_BART(cmd_class, my_cmd, data_tags, my_key="QT4P-PWE4-9YAT-DWE9"):
    '''Submits a REST API request to api.bart.gov and returns the response as a dict.'''
    # Initialize data dictionary
    data = dict.fromkeys(data_tags)

    # Build API request
    call = "http://api.bart.gov/api/{cmd_class}.aspx?cmd={cmd}&key={key}".format(cmd_class=cmd_class, cmd=my_cmd, key=my_key)

    # Submit request to server
    r = requests.get(call)

    if r.status_code == requests.codes.ok:
        # Parse XML
        root = etree.XML(r.content)
        for element in root.iter():
            if element.tag in data_tags:
                data[element.tag] = element.text
        return(data)

    else:
        raise Exception('Exception with status code {0}'.format(r.status_code))


def call_OpenWeatherMap(city_id, my_key="3b098e706196a06f885f5160d33ff872"):
    '''Submits a REST API request to api.openweathermap.org and returns the response as a dict.'''

    # Build API request
    call = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}".format(city_id=city_id, api_key=my_key)
    
    # Submit request to server
    r = requests.get(call)

    if r.status_code == requests.codes.ok:
        # Parse json
        root = json.loads(r.text)["weather"][0]["main"]
        data = {"weather": root}
        return(data)

    else:
        raise Exception('Exception with status code {0}'.format(r.status_code))


def merge_dicts(x, y):
    '''Merge two dicts into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return(z)

if __name__ == "__main__":

    my_key = "XXXX-XXXX-XXXX-XXXX"

    base_tags = ["date", "time", "type", "description", "posted"]
    traincount_tags = ["traincount"]

    bsa_cmd_class = "bsa"

    base_cmd = "bsa"
    traincount_cmd = "count"


    base_data = call_BART(bsa_cmd_class, base_cmd, base_tags)
    train_data = call_BART(bsa_cmd_class, traincount_cmd, traincount_tags)

    data = merge_dicts(base_data, train_data)

    # Supplemental elevator status data
    elevator_tags = ["description"]
    elev_cmd = "elev"

    elev_data = call_BART(bsa_cmd_class, elev_cmd, elevator_tags)
    # Rename description to elev_status and add to data dict
    data["elev_status"] = elev_data["description"]


    
    # ADD IN WEATHER DATA
    
    sanfrancisco_id = "5391959"

    weather_data = call_OpenWeatherMap(sanfrancisco_id, my_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    data = merge_dicts(data, weather_data)


    # Write to csv file using pandas
    #cols = base_tags.extend(traincount_tags).append("elev_status")
    cols = ["date", "time", "type", "description", "posted", "traincount", "elev_status", "weather"]
    df = pd.DataFrame(data, columns=cols, index=[0]).sort_index(axis=1)

    df.to_csv('C:\\path_to_data\\BART_data.csv', mode='a', header=False, index=False)

    print("Success! Data collected on {date} at {time}.".format(date=data["date"], time=data["time"]))
