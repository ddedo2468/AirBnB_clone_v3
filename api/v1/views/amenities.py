#!/usr/bin/python3
"""amenities module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """get all amenities"""
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return make_response(jsonify(amenities_list))


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity_id(amenity_id):
    """get the amenity by it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return make_response(jsonify(amenity.to_dict()), 200)
    abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """create a new amenity"""
    amenity = request.get_json()
    if not amenity:
        return make_response("Not a JSON", 400)
    if 'name' not in amenity:
        return make_response("Missing name", 400)
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """update existing amenity"""
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()
    ignored_list = ['id', 'created_at', 'updated_at']
    if not amenity:
        abort(404)
    if not data:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ignored_list:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
