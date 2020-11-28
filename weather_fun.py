import json
import urlib

class Weather_function:


    def def_min_max_day(city,country):

        api_key = "c34fa0019d8e4461a92ce998d5ee1e11"
        url = "https://api.weatherbit.io/v2.0/forecast/daily?"
        final_url = url + "city=" + city + "&country=" + country + "&key=" + api_key
        final_url = final_url.replace(" ", "%20")
        json_obj = urllib.request.urlopen((final_url))
        js = json.load(json_obj)


        for items in js["data"]:
            print (items["datetime"])
            print (items["weather"]["description"])
            print("min_temp:", items["min_temp"])
            print("max_temp:", items["max_temp"])
            print ("------")









