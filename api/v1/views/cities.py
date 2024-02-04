#!/usr/bin/python3
"""cities module API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """get all cities of a certain state"""
    state = storage.get(State, state_id)
    if state:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return make_response(jsonify(cities))
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """return json of certain city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a city based on its city_id"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
def post_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def put_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
    request_data = request.get_json()
    if city is None:
        abort(404)
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ignore_list:
            setattr(city, key, value)
    city.save()
    return make_response(city.to_dict(), 200)
