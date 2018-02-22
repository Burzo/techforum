from BaseHandler import BaseHandler

class CookieAlertHandler(BaseHandler):
    def post(self):
        self.response.set_cookie(key="piskotek", value="sprejet")
        return self.redirect_to("main-page")