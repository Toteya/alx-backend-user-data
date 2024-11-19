#!/usr/bin/env python3
"""
module app: A Flask web application
"""
from auth import Auth
from flask import Flask, jsonify


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users(email: str, password: str):
    """Handles POST /users"""
    try:
        AUTH.register_user(email=email, password=password)
        output = {"email": "{}", "message": "user created".format(email)}
    except ValueError:
        output = {"message": "email already registered"}
    return jsonify(output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
