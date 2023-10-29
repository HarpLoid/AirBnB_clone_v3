#!/usr/bin/python3
"""
Module - cities
View for City objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id):
    all_cities = storage.all(City)
    state = storage.get("State", state_id)
    cities = []

    if state is None:
        abort(404)

    for city in all_cities.values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)