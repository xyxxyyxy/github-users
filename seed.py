#!/usr/bin/env python

import sys, getopt, requests, json, sqlite3

def makeRequest(from_id, page):
    try:
        response = requests.get(
            url="https://api.github.com/users",
            params={
                "accept": "application/vnd.github.v3+json",
                "since": from_id,
                "per_page": page,
            },
        )
        return json.loads(response.content.decode('utf-8'))
    except requests.exceptions.RequestException:
        print("Error fetching resource")
        sys.exit(2)

def addToDB(c, req):
    for user in req:
        insertion = "INSERT INTO users VALUES ({},'{}', '{}','{}','{}')"
        c.execute(insertion.format(user["id"], user["login"], user["avatar_url"], user["type"], user["html_url"]))
        if user == req[-1]:
            return user["id"]

def handlePagination(c, total):
    last_id = 0
    while total > 0:
        if total <= 100:
            addToDB(c, makeRequest(last_id, total))
            total = 0
        else:
            last_id = addToDB(c, makeRequest(last_id, total))
            total -= 100





def main(argv):
    total = 150
    try:
        opts, args = getopt.getopt(argv,"t:",["total="])
        if opts:
            total = int(opts[0][1])
    except getopt.GetoptError:
        print("Usage: seed.py --total=<n>")
        sys.exit(2)
    conn = sqlite3.connect('gh_users.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users(id integer, username text, img_url text, type text, link_url text)")
    handlePagination(c, total)
    conn.commit()
    conn.close()

if __name__=="__main__": 
    main(sys.argv[1:])