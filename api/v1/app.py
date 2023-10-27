#!/usr/bin/python3
"""
Module - app
Flask app instance
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def teardown():
    """
    Removes the current SQLAlchemy Session after
    each request
    """
    storage.close()


if __name__ == "__main__":
    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST,
                port=int(HBNB_API_PORT),
                debug=True, threaded=True)
    app.run(host='0.0.0.0',
            port=5000,
            debug=True, threaded=True)
