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
    cities = []
    states = storage.all("State").values()

    for state in states:
        for city in state.cities():
            cities.append(city)
