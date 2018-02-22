from google.appengine.ext import ndb
from google.appengine.api import users, taskqueue

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

    @staticmethod
    def SHRANI_KOMENTAR(objava_id, vsebina):
        uporabnik = users.get_current_user()
        email = uporabnik.email()
        nov_komentar = Komentar(vsebina=vsebina,
                                uporabnikEmail=email,
                                objavaID=objava_id)
        nov_komentar.put()

        objava =  Objava.get_by_id(int(objava_id))
        taskqueue.add(url='/task/send-comment-mail',
                        params={
                            "email_avtorja_objave": objava.uporabnikEmail,
                            "email_avtorja_komentarja": email
                        })