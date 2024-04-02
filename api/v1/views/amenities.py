#!/usr/bin/python3
""" View that handles all default RESTFul API actions for Amenity objects. """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def allAmenity():
    """ Retrieves the list of all Amenity objects. """
    amenities = storage.all("Amenity")
    amenities = list(obj.to_dict() for obj in amenities.values())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity(amenity_id=None):
    """ Retrieves a single amenity by it's id. """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delAmenity(amenity_id=None):
    """ Deletes an Amenity object. """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    del obj
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def createAmenity():
    """ Creates a new Amenity object. """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, "Missing name")
    new_obj = Amenity(**req)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updateAmenity(amenity_id=None):
    """ Updates an Amenity object. """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404, "Not found")
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    name = req.get('name')
    if name is None:
        abort(400, "Missing name")

    obj.update_obj(req)
    return jsonify(obj.to_dict()), 200
