import uuid
import cgi
import time
from google.appengine.api import users, memcache
from google.appengine.ext import ndb
from models.models import Objava, Komentar
from BaseHandler import BaseHandler

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

        if users.get_current_user():
            email = users.get_current_user().email()
        else:
            return self.write("You must be logged in to participate.")

        nova_objava = Objava(naslov=naslov, vsebina=vsebina, uporabnikEmail=email)

        nova_objava.put()
        return self.redirect("/objava/"+str(nova_objava.key.id()))

class PoglejObjavoHandler(BaseHandler):
    def get(self, id):
        objava = Objava.get_by_id(int(id))

        komentarji = Komentar.query(Komentar.objavaID == str(objava.key.id())).order(-Komentar.cas_objave).fetch()
        parami = {"id": id, "deleted": objava.cas_izbrisa, "naslov":objava.naslov,"vsebina":objava.vsebina, "cas_objave":objava.cas_objave, "objava": objava, "komentarji": komentarji}

        return self.render_template("detajli.html", params=parami)

    def post(self, id):
        vsebina = cgi.escape(self.request.get("text"))
        Komentar.SHRANI_KOMENTAR(id, vsebina)

        time.sleep(0.1)
        return self.redirect("#")

class DeleteObjavoHandler(BaseHandler):
    def post(self, id):
        user = users.get_current_user()

        if not user:
            return self.write("You must first log in.")
        if not users.is_current_user_admin():
            return self.write("You must be admin to delete topics.")
        else:
            objava = Objava.get_by_id(int(id))
            objava.cas_izbrisa = True
            objava.put()
            time.sleep(0.1)
            return self.redirect("/")

class MojiKomentarjiHandler(BaseHandler):
    def get(self):
        params = {}
        objave = []
        user = users.get_current_user().email()
        vseobjave = Objava.query()
        vsikomentarji = Komentar.query()

        for komentar in vsikomentarji:
            if komentar.uporabnikEmail == user:
                objava = Objava.get_by_id(int(komentar.objavaID))
                #objave[str(objava.naslov)] = objava.key.id()
                if not objava.cas_izbrisa:
                    if not params.get(objava.naslov):
                        params[objava.naslov] = [komentar]
                    else:
                        params[objava.naslov].append(komentar)

        for i in Objava.query():
            objave.append(i)    
                
        wrapper = {"comments": params, "objave": objave}
        return self.render_template("comments.html", wrapper)