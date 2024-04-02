#!/usr/bin/python3
""" View that handles all default RESTFul API actions for State objects. """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def allStates():
    """ Retrieves the list of all State objects. """
    states = storage.all("State")
    states = list(obj.to_dict() for obj in states.values())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state(state_id):
    """ Retrieves a single state by it's id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delState(state_id):
    """ Deletes a State object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    del state
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def createState():
    """ Creates a new State object. """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, "Missing name")
    state = State(**req)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updateState(state_id=None):
    """ Updates a State object. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not found")
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    name = req.get('name')
    if name is None:
        abort(400, "Missing name")

    state.update_obj(req)
    return jsonify(state.to_dict()), 200
