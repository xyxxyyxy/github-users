from flask import Flask, render_template, Markup, request, redirect, session, url_for
from flask_paginate import Pagination, get_page_parameter
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'


class User(object):
    def __init__(self, id, username, image, type, link):
        self.id = id
        self.username = Markup('<a href="{}">{}</button>'.format(link, username))
        self.image = Markup('<figure class="image is-32x32"><img src="{}"></figure>'.format(image))
        self.type = type



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
    query = "SELECT * from user ORDER BY {} COLLATE NOCASE {} LIMIT {} OFFSET {}"
    res = c.execute(query.format(sort, direction, limit, offset))
    users = [User(*x) for x in res]
    queryCount = "SELECT count(*) from user"
    res2 = c.execute(queryCount)
    pagination = Pagination(page=page, per_page=limit, total=c.fetchone()[0], search=None, record_name='Users', css_framework='bulma')
    return render_template('index.html', users=users, pagination=pagination)


if __name__ == '__main__':
    app.run(host='0.0.0.0')