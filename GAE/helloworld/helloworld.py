# coding=utf-8
import webapp2
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import weather_endpoint

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(u'Hello World in Chinese is: 你好世界')
        self.response.write('<hr/>')
        weather_description, weather_picture = weather_endpoint.get_chicago_weather()
        self.response.write('<img src="'+weather_picture+'" /> ')
        self.response.write(weather_description)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
