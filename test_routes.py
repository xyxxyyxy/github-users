from flask import Flask
import json

from routes import configure_routes


def test_profiles__not_empty_success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/profiles'

    data = {
        "sort": "username",
        "direction": "asc",
        "limit": 25,
        "page": 1
    }

    response = client.get(url, query_string = data)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["data"] != []
    assert data["total"] == 150

def test_profiles__empty__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/profiles'

    data = {
        "sort": "username",
        "direction": "asc",
        "limit": 25,
        "page": 100
    }

    response = client.get(url, query_string = data)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["data"] == []
    assert data["total"] == 150

def test_profiles__empty__not_found():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/profiles'

    data = {
        "sort": "username",
        "direction": "asc",
        "limit": 25,
        "page": 1,
        "username": "leo"
    }

    response = client.get(url, query_string = data)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data["error"] == "no users found"

def test_profiles__empty__query__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/profiles'

    data = {
        "sort": "username",
        "direction": "asc",
        "limit": 25,
        "page": 1,
        "username": "a"
    }

    response = client.get(url, query_string = data)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["total"] == 80

def test_profiles__empty__query__one__user__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/profiles'

    data = {
        "sort": "username",
        "direction": "asc",
        "limit": 25,
        "page": 1,
        "username": "danwrong"
    }

    response = client.get(url, query_string = data)
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["total"] == 1
    assert data["data"][0]["id"] == 110

def test_default__empty__success():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'
    configure_routes(app)
    client = app.test_client()
    url = '/'

    data = {
        "page": 1,
    }

    response = client.get(url, query_string = data)
    assert response.status_code == 200
    assert b'Github Users' in response.data
    assert b'jamesgolick' not in response.data
    assert b'KirinDave' in response.data

def test_default__empty__success2():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'
    configure_routes(app)
    client = app.test_client()
    url = '/'

    data = {
        "page": 1,
    }

    response = client.get(url, query_string = data)
    assert response.status_code == 200
    assert b'Github Users' in response.data
    assert b'jamesgolick' not in response.data
    assert b'KirinDave' in response.data

def test_default__empty__success3():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'
    configure_routes(app)
    client = app.test_client()
    url = '/'

    data = {
        "page": 1,
        "sort": "type",
        "direction": "asc"
    }

    response = client.get(url, query_string = data)
    assert response.status_code == 200
    assert b'Github Users' in response.data
    assert b'Organization' in response.data

def test_default__empty__success3():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'
    configure_routes(app)
    client = app.test_client()
    url = '/'

    data = {
        "page": 1,
        "sort": "type",
        "direction": "desc"
    }

    response = client.get(url, query_string = data)
    assert response.status_code == 200
    assert b'Github Users' in response.data
    assert b'Organization' not in response.data