#!/usr/bin/python3
"""
    Flask App
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def td_storage(e):
    """ This method .close() after each request """
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """ Handles error 404. """
    msg = {"error": "Not found"}
    headers = e.__str__().split()[0]
    return make_response(jsonify(msg), headers)


@app.errorhandler(400)
def handle_400(e):
    """ Handles error 400. """
    msg = {"error": e.description}
    headers = e.__str__().split()[0]
    return make_response(jsonify(msg), headers)


if __name__ == "__main__":
    """ Runs the Flask App """
    app.run(host=host, port=port, threaded=True)
