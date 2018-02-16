from google.appengine.ext import ndb
from models.models import Objava
from BaseHandler import BaseHandler

class PoglejObjavoHandler(BaseHandler):
    def get(self, id):
        objava = Objava.get_by_id(int(id))
        parami = {"naslov":objava.naslov,"vsebina":objava.vsebina, "cas_objave":objava.cas_objave}
        return self.render_template("detajli.html", params=parami)