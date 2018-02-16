#!/usr/bin/env python
import os
import jinja2
import webapp2
import sys
from handlers.BaseHandler import BaseHandler
from handlers.MainHandler import MainHandler
from handlers.CookieHandler import CookieAlertHandler
from handlers.ObjaveHandler import DodajObjavoHandler
from handlers.PoglejObjavo import PoglejObjavoHandler


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/add', DodajObjavoHandler, name="dodaj_objavo"),
    webapp2.Route(r'/objava/<id:\d+>', PoglejObjavoHandler, name="poglej_objavo"),
], debug=True)
