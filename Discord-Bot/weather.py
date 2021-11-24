import requests
import variables

def get_weather(city):
    #api link
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    #reference the variables to param

    p = {'q':city,'appid':variables.WEATHER_API_KEY}

    #make request to api url using base url and params
    r = requests.get(base_url,params=p)

    #unload response to json
    api_data = r.json()

    #parse data
    weather_condition = api_data['weather'][0]['description']
    temparature = round(float((api_data['main']['temp'])-273.15))
    humidity = int(api_data['main']['humidity'])
    wind_speed = float(api_data['wind']['speed'])
    cloudiness = int(api_data['clouds']['all'])
    #rain_1h = api_data['rain']['1h']
    #snow_1h = api_data['snow']['1h']
    city_name = api_data['name']

    final_result = "Weather at "+city_name+"\n"+"Description: "+weather_condition+"\n" +"Temp: "+str(temparature) + " °c"+"\n" +"Humidity: "+ str(humidity) + "%" + "\n" + "Wind speed: " + str(wind_speed) + "m/s" + "\n" + "Cloudiness: " + str(cloudiness)


    #check if reponse is an error and notify about it if so
    if api_data['cod'] == '404':
      return "Invalid city name"
    elif api_data['cod'] == '401':
      return "couldnt call the weather api"
    elif api_data['cod'] == '429':
      return "api can not take more then 60 requests per minute, pls wait"

    #return requested data
    return final_result