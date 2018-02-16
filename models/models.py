from google.appengine.ext import ndb

class Objava(ndb.Model):
    vsebina = ndb.TextProperty()
    naslov = ndb.StringProperty()
    uporabnikEmail = ndb.StringProperty()
    cas_objave = ndb.DateTimeProperty(auto_now_add=True)
    cas_poosodobitve = ndb.DateTimeProperty(auto_now=True)
    cas_izbrisa = ndb.BooleanProperty(default=False)

class Komentar(ndb.Model):
    vsebina = ndb.TextProperty()
    objavaID = ndb.StringProperty()
    uporabnikEmail = ndb.StringProperty()
    cas_objave = ndb.DateTimeProperty(auto_now_add=True)
    cas_poosodobitve = ndb.DateTimeProperty(auto_now=True)
    cas_izbrisa = ndb.BooleanProperty(default=False)