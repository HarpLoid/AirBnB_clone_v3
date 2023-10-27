#!/usr/bin/python3
"""
Module - index
Index for API
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def api_status():
    """
    returns JSON of status
    """
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """
    Returns the count of all classes
    in storage
    """
    json_dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(json_dict)
