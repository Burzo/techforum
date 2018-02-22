from handlers.BaseHandler import BaseHandler
from google.appengine.api import mail


class MailWorker(BaseHandler):
    def post(self):
        email_avtorja_objave = self.request.get("email_avtorja_objave")
        email_avtorja_komentarja = self.request.get("email_avtorja_komentarja")

        mail.send_mail("test@example.com",
                       email_avtorja_objave,
                       "Somebody commented on your topic",
                       "<b>%s</b> has commented on your topic." % email_avtorja_komentarja)