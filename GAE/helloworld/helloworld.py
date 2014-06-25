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
