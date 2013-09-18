#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    search 搜索
"""

import tornado.web
import tornado.database
from settings import db, NAVNUM
from libs import markdown
from tornado.escape import xhtml_escape

md = markdown.Markdown(safe_mode=True)

class BaseHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
        blogdb = tornado.database.Connection(
            host=db["host"] + ":" + db["port"], database=db["db"],
            user=db["user"], password=db["password"])
        return blogdb

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return self.db.get("SELECT * FROM users WHERE id = %s", int(user_id))

class CodeHandler(BaseHandler):
    
    def get(self):
        
        q = xhtml_escape(self.get_argument("q"))
        
        entries = self.db.query("SELECT * FROM entries where title like '%%" + q + "%%' LIMIT 30")
        
        count = len(entries)
        pages = (count - 1) / NAVNUM + 1
        self.render("search.html", entries=entries, pages=pages, counts=count)
