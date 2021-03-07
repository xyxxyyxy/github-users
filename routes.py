from flask import Flask, render_template, Markup, request, redirect, session, url_for, jsonify
from flask_paginate import Pagination, get_page_parameter
import sqlite3

def toHtml(id, username, image, type, link):
    return (id, Markup('<a href="{}">{}</button>'.format(link, username)),
        Markup('<figure class="image is-32x32"><img src="{}"></figure>'.format(image)), type)
def toDict(id, username, image, type, link):
    return {"id": id, "username": username, "image": image, "link": link, "type": type}



def configure_routes(app):


    @app.route("/logout", methods=['GET'])
    def logout():
        session.clear()
        return redirect("/")


    @app.route("/", methods=['POST','GET'])
    def index():
        if request.method == 'POST':
            limit = request.form['limit']
            return redirect(url_for('index', limit=limit))

        sort = request.args.get('sort', None)
        direction = request.args.get('direction', None)
        limit = request.args.get('limit', type=int, default=None)
        page = request.args.get('page', type=int, default=None)

        if session:
            if not sort:
                sort = session['sort']
            else:
                session['sort'] = sort
            if not direction:
                direction = session['direction']
            else:
                session['direction'] = direction
            if not limit:
                limit = session['limit']
            else:
                session['limit'] = limit
        else:
            if not sort:
                sort = "id"
            if not direction:
                direction = "asc"
            if not limit:
                limit = 25
            session['sort'] = sort
            session['limit'] = limit
            session['direction'] = direction
        
        if not page:
                page = 1
        offset = (page-1)*limit
        direction = direction.upper()
        conn = sqlite3.connect('gh_users.db')
        c = conn.cursor()
        query = "SELECT * FROM user ORDER BY {} COLLATE NOCASE {} LIMIT {} OFFSET {}"
        res = c.execute(query.format(sort, direction, limit, offset))
        users = [toHtml(*x) for x in res]
        queryCount = "SELECT count(*) from user"
        res2 = c.execute(queryCount)
        pagination = Pagination(page=page, per_page=limit, total=c.fetchone()[0], search=None, record_name='Users', css_framework='bulma')
        return render_template('index.html', users=users, pagination=pagination)


    @app.route("/api/profiles", methods=['GET'])
    def profiles():
        sort = request.args.get('sort', "id")
        direction = request.args.get('direction', "asc")
        limit = request.args.get('limit', type=int, default=25)
        page = request.args.get('page', type=int, default=1)
        username = request.args.get('username', default="")
        offset = (page-1)*limit
        direction = direction.upper()
        conn = sqlite3.connect('gh_users.db')
        c = conn.cursor()
        query = "SELECT * FROM user WHERE username LIKE '%{}%'ORDER BY {} COLLATE NOCASE {} LIMIT {} OFFSET {}"
        res = c.execute(query.format(username, sort, direction, limit, offset))
        users = [toDict(*x) for x in res]
        queryCount = "SELECT count(*) from user WHERE username LIKE '%{}%'".format(username)
        res2 = c.execute(queryCount)
        total = c.fetchone()[0]
        if total == 0:
            return jsonify({"error": "no users found"}), 404
        return jsonify({"total": total, "data": users}), 200