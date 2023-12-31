#!/usr/bin/python3
"""
Module - places
View for Place objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_city(city_id):
    city = storage.get("City", city_id)
    places = []

    if city is None:
        abort(404)

    for city in city.places:
        places.append(city.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """
    Retrieves a Place object
    """
    city = storage.get('Place', place_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object
    """
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in content:
        return jsonify({'error': 'Missing user_id'}), 400
    elif 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400
    else:
        city = storage.get('City', city_id)
        user = storage.get('User', content['user_id'])
        if (city is None) or (user is None):
            abort(404)
        content['city_id'] = city.id
        content['user_id'] = user.id
        obj_updt = Place(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at',
                   'user_id', 'city_id']
    for k, v in content.items():
        if hasattr(obj, k) and k not in ignore_list:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
