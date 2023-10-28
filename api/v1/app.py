#!/usr/bin/python3
"""
Module - app
Flask app instance
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    Removes the Session after
    each request
    """
    storage.close()


@app.errorhandler(404)
def error_404_page(err):
    """
    Returns a JSON-formatted 404 status code response.
    """
    return make_response(jsonify({'error': 'Not found'}),
                         404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True, debug=True)
