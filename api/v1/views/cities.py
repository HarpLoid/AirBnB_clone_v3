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
    # all_cities = storage.all(City)
    state = storage.get("State", state_id)
    cities = []

    if state is None:
        abort(404)

    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """
    Retrieves a City object
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    """
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400
    else:
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        content['state_id'] = state_id
        obj_updt = City(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    for k, v in content.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200