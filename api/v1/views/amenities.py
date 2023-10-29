#!/usr/bin/python3
"""
Module - amenity
View for Amenity objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    obj_dict = storage.all('Amenity')
    amenity_list = []
    for obj in obj_dict.values():
        amenity_list.append(obj.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    Retrieves a Amenity object
    """
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object
    """
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj_updt = Amenity(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at']
    for k, v in content.items():
        if hasattr(obj, k) and k not in ignore_list:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
