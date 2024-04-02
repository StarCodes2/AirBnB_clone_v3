#!/usr/bin/python3
""" View that handles all default RESTFul API actions for City objects. """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def citiesInState(state_id):
    """ Retrieves a list of all City objects related to a State Object. """
    state = storage.get(State, state_id)
    cities = list(obj.to_dict() for obj in state.cities)
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city(city_id):
    """ Retrieves a single city by it's id. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delCity(city_id):
    """ Deletes a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    del city
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createCity(state_id=None):
    """ Creates a new City object. """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, "Missing name")
    if storage.get(State, state_id) is None:
        abort(404)
    req["state_id"] = state_id
    city = City(**req)
    city.save()
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updateCity(city_id=None):
    """ Updates a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "Not found")
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    name = req.get('name')
    if name is None:
        abort(400, "Missing name")

    city.update_obj(req)
    return jsonify(city.to_dict())
