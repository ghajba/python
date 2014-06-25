# coding=utf-8
from suds.client import Client

#create the client endpoint
client = Client('http://wsf.cdyne.com/WeatherWS/Weather.asmx?WSDL')

#request the weather information
weathers = client.service.GetWeatherInformation()

def get_city_weather(zip_code):
    city = client.service.GetCityWeatherByZIP(zip_code)
    if not city['Success']:
    	return city['ResponseText'], None
    weather_information = [elem for elem in weathers[0] if elem['WeatherID'] == city['WeatherID']][0]
    return u'The weather in %s, %s is currently: %s with %s°F' % (city['City'], city['State'], weather_information['Description'], city['Temperature']), \
           weather_information['PictureURL']
