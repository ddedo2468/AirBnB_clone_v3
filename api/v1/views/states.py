#!/usr/bin/python3
"""handles all default RESTFul API actions for state module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get():
    """retrives states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())

    return make_response(jsonify(states), 200)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state_id(state_id):
    """get state using id"""
    state = storage.get(State, state_id)
    if state:
        return make_response(jsonify(state.to_dict()), 200)
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """delete state using id"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'])
def post_state():
    """create new state"""
    state = request.get_json()

    if not state:
        return make_response("Not a JSON", 400)
    if 'name' not in state:
        return make_response("Missing name", 400)
    new_state = State(**state)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def put_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    ignored_list = ['id', 'created_at', 'updated_at']
    request_data = request.get_json()

    if not state:
        abort(404)
    if not request_data:
        return make_response("Not a JSON", 400)
    for key, value in request_data.items():
        if key not in ignored_list:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
