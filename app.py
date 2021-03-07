from flask import Flask
from routes import configure_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b^DFxM7Z?7s3ZByu5C%JN7%8*8dbxS_'

configure_routes(app)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)