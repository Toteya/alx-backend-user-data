#!/usr/bin/env python3
"""
module app: A Flask web application
"""
from auth import Auth
from flask import abort, Flask, jsonify, make_response, request, redirect


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome():
    """Welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Registers a new users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        output = {"email": "{}", "message": "user created"}
    except ValueError:
        output = {"message": "email already registered"}
    return jsonify(output)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Login an existing user - new session
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": "{}".format(email),
                                      "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logs out a user - end a session
    """
    session_id = request.form.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
