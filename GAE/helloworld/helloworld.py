# coding=utf-8
import webapp2
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import weather_endpoint

MAIN_PAGE_HTML_HEAD = """\
<html>
  <head>
    <title>Simple GAE Project by GHajba</title>
  </head>
  <body>
  	<h1>Welmoe to this all-in-one GAE project</h1>
  	<div>This is a simple web application on the GAE created in Python</div>
  	<h3>Printing "Hello World" in Chinese:</h3>
"""

MAIN_PAGE_HTML_FOOT = """\
    <hr />
  </body>
</html>
"""

MAIN_PAGE_HTML_WEATHER_FORM = """\
    <hr />
    <form action="/weather" method="get">
      <div>Look up the weather of a US-City by its ZIP-Code:</div>
      <div><input name="zip" type="number" size="10" min="10000" max="99999" required></div>
      <div><input type="submit" value="Ask for the weather"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(MAIN_PAGE_HTML_HEAD)
        self.response.write(u'Hello World in Chinese is: 你好世界')
        self.response.write(MAIN_PAGE_HTML_WEATHER_FORM)
        self.response.write(MAIN_PAGE_HTML_FOOT)

class Weather(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(MAIN_PAGE_HTML_HEAD)
        weather_description, weather_picture = weather_endpoint.get_city_weather(self.request.get('zip'))
        if weather_picture is not None:
            self.response.write('<img src="'+weather_picture+'" /> ')
        self.response.write(weather_description)
        self.response.write(MAIN_PAGE_HTML_WEATHER_FORM)
        self.response.write(MAIN_PAGE_HTML_FOOT)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/weather', Weather)
], debug=True)
