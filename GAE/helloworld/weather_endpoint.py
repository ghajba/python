from suds.client import Client

#create the client endpoint
client = Client('http://wsf.cdyne.com/WeatherWS/Weather.asmx?WSDL')
#print client

#request the current weather of Chicago, IL
chicago = client.service.GetCityWeatherByZIP(60637)
#print chicago

#request the weather information
weathers = client.service.GetWeatherInformation()

#weather_information = [elem for elem in weathers[0] if elem['WeatherID'] == chicago['WeatherID']][0]

#print 'The weather in Chicago, IL is currently: %s' % weather_information['Description']


def get_city_weather(zip_code):
    city = client.service.GetCityWeatherByZIP(zip_code)
    weather_information = [elem for elem in weathers[0] if elem['WeatherID'] == city['WeatherID']][0]
    return 'The weather in %s, %s is currently: %s' % (city['City'], city['State'], weather_information['Description']), \
           weather_information['PictureURL']


def get_chicago_weather():
    return get_city_weather(60637)