#!/usr/bin/python3
"""user module api"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """get all usesrs from db"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())

    return make_response(jsonify(users), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """retrvive user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users', methods=['POST'])
def create_user():
    """create new user"""
    user = request.get_json()
    if not user:
        return make_response("Not a JSON", 400)
    if not user.get('email'):
        return make_response("Missing email", 400)
    if not user.get('password'):
        return make_response("Missing password", 400)
    new_user = User(**user)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update user by id"""
    user = storage.get(User, user_id)
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    new_user = request.get_json()
    if not user:
        abort(404)
    if not new_user:
        return make_response("Not a JSON", 400)
    for key, value in new_user.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)
