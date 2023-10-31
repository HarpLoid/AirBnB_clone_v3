#!/usr/bin/python3
"""
Module - state
View for State objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    obj_dict = storage.all('State')
    state_list = []
    for obj in obj_dict.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """
    Retrieves a State object
    """
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in content:
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj_updt = State(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at']
    for k, v in content.items():
        if hasattr(obj, k) and k not in ignore_list:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
