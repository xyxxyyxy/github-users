from flask import Flask, render_template, Markup, url_for, request, redirect, session
from flask_table import Table, Col
from flask_paginate import Pagination, get_page_parameter
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'



class ItemTable(Table):
    classes = ['table', 'is-bordered', 'is-striped', 'is-narrow', 'is-hoverable', 'is-fullwidth']
    id = Col('ID')
    username = Col('Username')
    image = Col('Image', allow_sort=False)
    type = Col('Type')
    allow_sort = True
    def sort_url(self, col_key, reverse=reverse):
        reverse = not reverse
        return url_for('index', sort=col_key, reverse=reverse)


class User(object):
    def __init__(self, id, username, image, type, link):
        self.id = id
        self.username = Markup('<a href="{}">{}</button>'.format(link, username))
        self.image = Markup('<figure class="image is-32x32"><img src="{}"></figure>'.format(image))
        self.type = type



@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return url_for('index')


@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
        limit = request.form['limit']
        return redirect(url_for('index', limit=limit))
    sort = request.args.get('sort', None)
    direction = request.args.get('direction', None)
    limit = request.args.get('limit', type=int, default=None)
    page = request.args.get('page', type=int, default=None)
    reverse = request.args.get('reverse', None)
    print(session)

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
        if reverse:
            if direction == 'asc':
                direction = 'desc'
            else:
                direction = 'asc'
            session['direction'] = direction
    else:
        if not sort:
            sort = "id"
        if not direction:
            direction = "desc"
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
    query = "SELECT * from user ORDER BY {} {} LIMIT {} OFFSET {}"
    res = c.execute(query.format(sort, direction, limit, offset))
    items = [User(*x) for x in res]
    table = ItemTable(items)
    queryCount = "SELECT count(*) from user"
    res2 = c.execute(queryCount)
    pagination = Pagination(page=page, per_page=limit, total=c.fetchone()[0], search=None, record_name='Users', css_framework='bulma')
    return render_template('index.html', table=table, pagination=pagination)


if __name__ == '__main__':
    app.run(host='0.0.0.0')