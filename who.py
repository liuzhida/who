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
        self.finish()
        # self.redirect("/")


class LoginHandler(tornado.web.RequestHandler):

    # def get(self):
    #    return self.render('login.html')

    def post(self):
        data = self.request.body
        data = json.loads(data)
        mail = data['username']
        passwd = data['password']

        if mail.endswith("@wandoujia.com"):
            mail = mail.rstrip("@wandoujia.com")
        if Auth(mail, passwd):
            user = dict()
            user['email'] = mail + "@wandoujia.com"
            self.set_secure_cookie("user", json.dumps(user))
            self.finish()
            return
        else:
            raise tornado.web.HTTPError(403)
            return


class AreaHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self, name):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        data = c.hgetall("area:" + name)
        members = list()
        if c.exists("member:" + data['name']):
            persons = list(c.smembers("member:" + data['id']))
            for person in persons:
                d = dict()
                d = c.hgetall("person:" + person)
                d['id'] = person
                members.append(d)
            members = sorted(members, key=lambda p: p['edate'])
            data['members'] = members
        if c.exists("productof:" + data['name']):
            data['products'] = list()
            products = c.smembers("productof:" + data['name'])
            for product in products:
                d = dict()
                d = c.hgetall("product:" + product)
                d['id'] = product
                data['products'].append(d)
        owner = data['owner']
        data['owner'] = c.hgetall("person:" + owner)

        self.finish(json.dumps(data))


class ProductHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        data = c.hgetall("product:" + id)
        owner = data['tl']
        if c.exists("person:" + owner):
            data['tl'] = c.hgetall("person:" + owner)
        owner = data['pm']
        if c.exists("person:" + owner):
            data['pm'] = c.hgetall("person:" + owner)
        self.finish(json.dumps(data))


class FunctionHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        data = c.hgetall("function:" + id)
        if c.exists("member:" + id):
            members = list()
            persons = list(c.smembers("member:" + id))
            for person in persons:
                d = dict()
                d = c.hgetall("person:" + person)
                d['id'] = person
                members.append(d)
            data['members'] = members

        # owner = data['tl']
        # if c.exists("person:" + owner):
        #    data['tl'] = c.hgetall("person:" + owner)
        # owner = data['pm']
        # if c.exists("person:" + owner):
        #    data['pm'] = c.hgetall("person:" + owner)
        self.finish(json.dumps(data))


class ListHandler(BaseHandler):

    #@tornado.web.authenticated

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
            result = sorted(result, key=lambda p: p['name'])
        elif name == "product":
            for key in c.keys("product:*"):
                data = c.hgetall(key)
                result.append(data)
            result = sorted(result, key=lambda p: p['name'])
        elif name == "person":
            for key in c.keys("person:*"):
                data = c.hgetall(key)
                data['id'] = key.split(":")[-1]
                result.append(data)
            result = sorted(result, key=lambda p: p['edate'])
            result = result[::-1]
        elif name == "function":
            for key in c.keys("function:*"):
                data = c.hgetall(key)
                if c.exists("member:" + data['id']):
                    data['number'] = len(c.smembers("member:" + data['id']))
                result.append(data)
            result = sorted(result, key=lambda p: p['name'])
 
        self.finish(json.dumps(result))


class PersonHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self, id):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        # email = self.user["email"]
        # name = email.split("@")[0]
        # self.render('index.html', name=name)
        data = c.hgetall("person:" + id)
        data['id'] = id
        if data['manager']:
            manager = data['manager']
            data['manager'] = c.hgetall("person:" + manager)
        if "socials" in data:
            data['socials'] = eval(data['socials'])
        c.zadd("clickofperson", "person:" + id, 1.0)
        self.finish(json.dumps(data))

    #@tornado.web.authenticated
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
        with open("/home/work/who/123", "a") as f:
            f.write(data + "\n")
        data = json.loads(data)
        del data['function']
        del data['PA']
        del data['manager']
        del data['edate']
        if "img" in data:
            del data['img']
        # result = dict()
        # result['name']      = data['name']
        # result['sex']       = data['sex']
        # result['objective']       = data['objective']
        # result['function']  = data['function']
        # result['PA']        = data['PA']
        # result['manager']   = data['manager']
        # result['edate']     = data['edate']
        # result['phone']     = data['phone']
        # result['mail']      = data['mail']
        # result['hometown']  = data['hometown']
        # result['xingzuo']   = data['xingzuo']
        # result['school']    = data['school']
        # result['socials']   = data['socials']

        # for key in data.keys():
        #    c.hset("person:" + id, key, data[key])

        c.hmset("person:" + id, data)
        self.finish()


class QueryHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        word = self.get_argument("word")
        word = word.encode("utf-8")
        key = list()
        data = list()
        ids = list()

        if not word:
            result = dict()
            data.append(result)

        #if "大学" in word:
        #    if c.exists("index:" + word):
        #        key.append("index:" + word)

        for n in seg_txt(word):
            if c.exists("index:" + n):
                key.append("index:" + n)

        if len(key) == 0 and ord(word[0]) <= 127:
            word = word.lower()
            tokenizer = PinyinTokenizer()
            keys = tokenizer.tokenize(word)
            if keys:
                for n in keys:
                    if c.exists("index:" + n):
                        key.append("index:" + n)
                    else:
                        _keys = c.keys("index_p:" + n + "*")
                        key.extend(_keys)
            else:
                _keys = c.keys("index:" + word + "*")
                key.extend(_keys)

        if len(key) == 0:
            _keys = c.keys("index:" + word + "*")
            key.extend(_keys)

        if len(key) == 0:
            result = dict()
            data.append(result)
        elif len(key) == 1:
            ids = c.smembers(key[0])
        else:
            ids = c.sinter(key)

        if not ids:
            result = dict()
            data.append(result)

        for id in ids:
            result = dict()
            result = c.hgetall(id)
            result['id'] = id.split(":")[-1]
            result['type'] = id.split(":")[0]
            data.append(result)

        self.finish(json.dumps(data))


class CurrentHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        email = self.user["email"]
        name = email.split("@")[0]
        data = c.hgetall("person:" + name)
        data['id'] = name
        self.finish(json.dumps(data))


class IndexHandler(BaseHandler):

    #@tornado.web.authenticated

    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.render('index.html')

    #@tornado.web.authenticated
    # def post(self):
    #    if not self.current_user:
    #        raise tornado.web.HTTPError(403)
    #        return
    #    id = self.get_argument("id")
    #    return


class UpdateHandler(BaseHandler):

    #@tornado.web.authenticated

    def post(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        email = self.user["email"]
        id = email.split("@")[0]
        if self.request.files:
            for f in self.request.files['file']:
                type = f['filename'].split(".")[-1]
                import glob
                import os
                os.chdir("/home/work/who/static/img/")
                for files in glob.glob("%s*" % id):
                    os.remove(files)
                with open("/home/work/who/static/img/%s.%s" % (id, type), "w") as w:
                    w.write(f['body'])
                c.hset("person:" + id, "img", "http://who.wandoulabs.com/static/img/%s.%s" % (id, type))
        else:
            raise tornado.web.HTTPError(403)
            return
        self.finish('ok')


def main():
    define("port", default=3088, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
                "static_path": "static",
                #"login_url": "/api/v1/login",
                "cookie_secret": "Zsaz1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="
                }
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        #(r"/", IndexHandler),
        (r"/api/v1/login", LoginHandler),
        (r"/api/v1/logout", LogoutHandler),
        (r"/api/v1/area/(.*)", AreaHandler),
        (r"/api/v1/product/(.*)", ProductHandler),
        (r"/api/v1/function/(.*)", FunctionHandler),
        (r"/api/v1/person/(.*)", PersonHandler),
        (r"/api/v1/list/(.*)", ListHandler),
        (r"/api/v1/query", QueryHandler),
        (r"/api/v1/update", UpdateHandler),
        (r"/api/v1/current_user", CurrentHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
