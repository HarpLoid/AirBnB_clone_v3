#!/usr/bin/python3
"""
Module - users
View for User objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    obj_dict = storage.all('User')
    user_list = []
    for obj in obj_dict.values():
        user_list.append(obj.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """
    Retrieves a User object
    """
    obj = storage.get('User', user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    """
    obj = storage.get('User', user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Creates a User
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'email' not in content:
        return jsonify({'error': 'Missing email'}), 400
    elif 'password' not in content:
        return jsonify({'error': 'Missing password'}), 400
    else:
        obj_updt = User(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('User', user_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at', 'email']
    for k, v in content.items():
        if hasattr(obj, k) and k not in ignore_list:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
