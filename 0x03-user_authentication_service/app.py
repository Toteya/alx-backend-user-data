#!/usr/bin/env python3
"""
module app: A Flask web application
"""
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Handles POST /users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        output = {"email": "{}".format(email), "message": "user created"}
    except ValueError:
        output = {"message": "email already registered"}
    return jsonify(output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
