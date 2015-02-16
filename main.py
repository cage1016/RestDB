import webapp2
import endpoints

from api import RestDBApi


class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('Hello world!')


route = [
  ('/', MainHandler)
]

APPLICATION = webapp2.WSGIApplication(route, debug=True)

API = endpoints.api_server([
  RestDBApi
])



