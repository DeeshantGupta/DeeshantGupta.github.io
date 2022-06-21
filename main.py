import webapp2
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **par):
        t = jinja_env.get_template(template)
        return t.render(par)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Decryptor(Handler):
    a = ""

    def get(self):
        self.render("decryptor.html", t=self.a)

    def post(self):
        t = self.request.get("text")
        for i in t:
            if (ord(i) in range(97, 110)) or (ord(i) in range(65, 77)):
                self.a += chr(ord(i)+13)
            elif (ord(i) in range(110, 123)) or (ord(i) in range(77, 91)):
                self.a += chr(ord(i)-13)
            else:
                self.a += i
        self.render("decryptor.html", t=self.a)


class FizzBuzz(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = int(n)
        self.render("FizzBuzz.html", n=n)


class MainPage(Handler):
    def get(self):
        items = self.request.get_all('food')
        self.render("shoppingList.html", items=items)

# class Calculator(webapp2.RequestHandler):
#     def post(self):
#         # a = self.request.get("q")
#         # b = self.request.get("p")
#         # c = int(a) + int(b)
#         self.response.headers['Content-Type'] = 'text/plain'
#         # self.response.write("<h1>result: {ans}</h1>".format(ans=c))
#         self.response.write(self.request)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/FizzBuzz', FizzBuzz),
    ('/encryptor', Decryptor)], debug=True)
