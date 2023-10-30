#!/usr/bin/python3
"""
Module - reviews
View for Review objects
that handles all default
RESTFul API actions
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_by_place(place_id):
    place = storage.get("Place", place_id)
    reviews = []

    if place is None:
        abort(404)

    for place in place.reviews:
        reviews.append(place.to_dict())
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    """
    obj = storage.get('Review', review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in content:
        return jsonify({'error': 'Missing user_id'}), 400
    elif 'text' not in content:
        return jsonify({'error': 'Missing name'}), 400
    else:
        place = storage.get('Place', place_id)
        user = storage.get('User', content['user_id'])
        if (place is None) or (user is None):
            abort(404)
        content['place_id'] = place.id
        content['user_id'] = user.id
        obj_updt = Review(**content)
        obj_updt.save()
        return jsonify(obj_updt.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    content = request.get_json()
    if not content:
        return jsonify({'error': 'Not a JSON'}), 400

    obj = storage.get('Review', review_id)
    if obj is None:
        abort(404)
    ignore_list = ['id', 'created_at', 'updated_at',
                   'user_id', 'place_id']
    for k, v in content.items():
        if hasattr(obj, k) and k not in ignore_list:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200