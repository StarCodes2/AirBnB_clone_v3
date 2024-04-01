#!/usr/bin/python3
""" Route that returns json status response """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Returns the count of objects in storage by class """
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }

    res = {}
    for key, value in classes.items():
        res[value] = storage.count(key)
    return jsonify(res)
