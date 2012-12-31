#!/usr/bin/env python
# -*- set coding: utf-8 -*-
import os, glob
import markdown
from flask import Flask, Markup, render_template, url_for, make_response, abort
from config import *
import utils
import db

application = Flask(__name__, template_folder=PARERGA_TEMPLATE_DIR)
app = application
app.debug = True

# db managing functions
app.before_request_funcs.setdefault(None, []).insert(0, db.before_request)
app.teardown_request_funcs.setdefault(None, []).insert(0, db.teardown_request)
# slugify
app.jinja_env.globals.update(slugify=utils.slugify)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
@app.route("/index/")
def index():
    posts = all_entries()
    return render_template("index.html", **locals())

@app.route("/<int:entry_id>/")
def blog_entry(entry_id):
    try:
        post = utils.Entry(entry_id)
    except EntryException as e:
        abort(404)
    return render_template("entry.html", **locals())

@app.route("/tag/")
def index_tags():
    tags = utils.get_all_tags()
    return render_template("index_tags.html", **locals())

@app.route("/tag/<string:tag>/")
def index_tagged(tag):
    entries = all_entries()
    posts = [e for e in entries if tag in e['tags']]
    return render_template("index_tagged.html", **locals())

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/favicon.png")
def favicon():
    resp = make_response(open(os.path.join(PARERGA_STATIC_DIR, "favicon.png")).read())
    resp.content_type = "image/png"
    return resp

def all_entries():
    return utils.get_all_entries()

if __name__ == '__main__':
    app.run(port=5001)
