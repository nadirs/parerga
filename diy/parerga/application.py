#!/usr/bin/env python
# -*- set coding: utf-8 -*-

import os, glob
from flask import (Flask, Markup, render_template, url_for, send_from_directory,
        abort, redirect)
from config import *
import utils
import db

application = Flask(__name__, template_folder=PARERGA_TEMPLATE_DIR)
app = application
app.debug = True
app.root_path = os.path.dirname(app.root_path)

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

@app.route("/articles/<int:entry_id>/")
@app.route("/articles/<int:entry_id>/<string:entry_title>/")
def blog_entry(entry_id, entry_title=""):
    try:
        post = utils.Entry(entry_id)
        expected_title = utils.slugify(post['title'])
        if entry_title != expected_title:
            return redirect(url_for('.blog_entry', entry_id=entry_id, entry_title=expected_title))
    except utils.EntryException as e:
        abort(404)
    return render_template("entry.html", **locals())

@app.route("/tags/")
def index_tags():
    tags = utils.get_all_tags()
    return render_template("index_tags.html", **locals())

@app.route("/tags/<string:tag>/")
def index_tagged(tag):
    entries = all_entries()
    posts = [e for e in entries if tag in e['tags']]
    return render_template("index_tagged.html", **locals())

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/static/favicon.png")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.png', mimetype='image/png')

@app.route("/sitemap.xml")
def sitemap():
    response = make_response(open(os.path.join(PARERGA_STATIC_DIR, "sitemap.xml")).read())
    response.headers["Content-Type"] = "application/xml"
    return response

def all_entries():
    return utils.get_all_entries()

if __name__ == '__main__':
    app.run(port=5001)
