#!/usr/bin/env python
#-*-coding:utf-8-*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.auth
from tornado.options import define, options

from ldap_auth import Auth
import json
from config import c
from mmseg import seg_txt
from pinyin_trie import PinyinTokenizer, Trie, TrieNode


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render('login.html')

    def post(self):
        mail = self.get_argument('mail')
        type = self.get_argument('type', None)
        if mail.endswith("@wandoujia.com"):
            mail = mail.strip("@wandoujia.com")
        passwd = self.get_argument("passwd")
        if Auth(mail, passwd):
            user = dict()
            user['email'] = mail + "@wandoujia.com"
            self.set_secure_cookie("user", json.dumps(user))
            if type:
                return self.finish(json.dumps({"ret": 1}))
            else:
                self.redirect("/")
        else:
            if type:
                return self.finish(json.dumps({"ret": 0}))
            else:
                return self.render('login_failed.html')


class AreaHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, name):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        data = c.hgetall("area:" + name)
        if c.exists("member:" + data['name']):
            data['members'] = list(c.smembers("member:" + data['name']))

        self.finish(json.dumps(data))


class ProductHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        data = c.hgetall("product:" + id)
        self.finish(json.dumps(data))


class ListHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, name):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        result = list()
        data = dict()
        if name == "area":
            for key in c.keys("area:*"):
                data = c.hgetall(key)
                if c.exists("member:" + data['name']):
                    data['number'] = len(c.smembers("member:" + data['name']))
                result.append(data)
        elif name == "product":
            for key in c.keys("product:*"):
                data = c.hgetall(key)
                result.append(data)

        self.finish(json.dumps(result))


class PersonHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        # email = self.user["email"]
        # name = email.split("@")[0]
        # self.render('index.html', name=name)
        data = c.hgetall("person:" + id)
        self.finish(json.dumps(data))

    @tornado.web.authenticated
    def post(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        email = self.user["email"]
        name = email.split("@")[0]

        if id != name:
            raise tornado.web.HTTPError(403)
            return
        data = self.request.body
        data = json.loads(data)
        #result['name']      = data[1]
        #result['sex']       = data[2]
        #result['function']  = data[3]
        #result['PA']        = data[4]
        #result['manager']   = data[5]
        #result['phone']     = data[6]
        #result['mail']      = data[7]
        #result['edate']     = data[9]
        #result['hometown']  = data[10]
        #result['xingzuo']   = data[12]
        #result['school']    = data[15]


        # self.render('index.html', name=name)
        #data = c.hgetall("person:" + id)
        self.finish()




class QueryHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        word = self.get_argument("word")
        word = word.encode("utf-8")
        key = list()
        data = list()

        if not word:
            result = dict()
            data.append(result)
            self.finish(json.dumps(data))

        for n in seg_txt(word):
            if c.exists("index:" + n):
                key.append("index:" + n)

        if not key and ord(word[0]) <= 127:
            word = word.lower()
            tokenizer = PinyinTokenizer()
            keys = tokenizer.tokenize(word)
            for n in keys:
                key.append("index:" + n)

        if len(key) == 1:
            ids = c.smembers(key[0])
        elif len(key) == 0:
            result = dict()
            data.append(result)
            self.finish(json.dumps(data))
        else:
            ids = c.sinter(key)
        
        for id in ids:
            result = dict()
            result = c.hgetall(id)
            result['type'] = id.split(":")[0]
            data.append(result)

        self.finish(json.dumps(data))


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        email = self.user["email"]
        name = email.split("@")[0]
        self.render('index.html', name=name)

    @tornado.web.authenticated
    def post(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        id = self.get_argument("id")
        return


def main():
    define("port", default=3088, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
                "static_path": "static", "login_url": "/login",
                "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="
                }
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/api/v1/area/(.*)", AreaHandler),
        (r"/api/v1/product/(.*)", ProductHandler),
        (r"/api/v1/person/(.*)", PersonHandler),
        (r"/api/v1/list/(.*)", ListHandler),
        (r"/api/v1/query", QueryHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
