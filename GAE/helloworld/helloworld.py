# coding=utf-8
import webapp2
import os
import sys
import jinja2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import weather_endpoint

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

MAIN_PAGE_HTML_HEAD = """\
<html>
  <head>
    <title>Simple GAE Project by GHajba</title>
  </head>
  <body>
  	<h1>Welmoe to this all-in-one GAE project</h1>
  	<div>This is a simple web application on the GAE created in Python</div>
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
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
      weather_description = None
      weather_picture = None
      if self.request.get('zip'):
        weather_description, weather_picture = weather_endpoint.get_city_weather(self.request.get('zip'))
      template_values = {
        'weather_description': weather_description,
        'weather_picture': weather_picture
      }
      self.response.headers['Content-Type'] = 'text/html'
      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/weather', MainPage)
], debug=True)
