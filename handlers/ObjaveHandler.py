import uuid

from BaseHandler import BaseHandler
from models.models import Objava

from google.appengine.api import users, memcache

class DodajObjavoHandler(BaseHandler):
    def get(self):
        params = {}
        params["csrf_token"] = str(uuid.uuid4())

        memcache.add(params["csrf_token"], True, 600)

        return self.render_template("dodaj_objavo.html", params=params)

    def post(self):
        vrednost_csrf = self.request.get("csrf-token")
        if not memcache.get(vrednost_csrf):
            return self.write("CSRF attack.")

        naslov = self.request.get("title")
        vsebina = self.request.get("text")
        email = users.get_current_user().email()

        nova_objava = Objava(naslov=naslov, vsebina=vsebina, uporabnikEmail=email)

        nova_objava.put()
        return self.redirect("/objava/"+str(nova_objava.key.id()))