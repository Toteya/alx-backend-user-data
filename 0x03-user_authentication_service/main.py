#!/usr/bin/env python3
"""
main module: Test the user authentication API
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Test user registration
    """
    payload = {'email': email, 'password': password}
    api_endpoint = 'http://localhost:5000/users'
    response = requests.post(url=api_endpoint, data=payload)
    output = response.json()
    assert output == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test user login attempt with an incorrect password
    """
    payload = {'email': email, 'password': password}
    api_endpoint = 'http://localhost:5000/sessions'
    response = requests.post(url=api_endpoint, data=payload)
    output = response.status_code
    assert output == 401


def log_in(email: str, password: str) -> str:
    """ Test user login
    """
    payload = {'email': email, 'password': password}
    api_endpoint = 'http://localhost:5000/sessions'
    response = requests.post(url=api_endpoint, data=payload)
    output = response.json()
    assert output == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test unlogged profile
    """
    api_endpoint = 'http://localhost:5000/profile'
    response = requests.get(url=api_endpoint)
    output = response.status_code
    assert output == 403


def profile_logged(session_id: str) -> None:
    """ Test logged in profile
    """
    cookies = {'session_id': session_id}
    api_endpoint = 'http://localhost:5000/profile'
    response = requests.get(url=api_endpoint, cookies=cookies)
    output = response.json()
    assert output == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Test user logging
    """
    cookies = {'session_id': session_id}
    api_endpoint = 'http://localhost:5000/sessions'
    response = requests.delete(url=api_endpoint, cookies=cookies)
    output = response.json()
    assert output == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Test password reset
    """
    payload = {'email': email}
    api_endpoint = 'http://localhost:5000/reset_password'
    response = requests.post(url=api_endpoint, data=payload)
    output = response.json()
    token = output.get('reset_token')
    assert output == {"email": email, "reset_token": token}
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests updating of a password
    """
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    api_endpoint = 'http://localhost:5000/reset_password'
    response = requests.put(url=api_endpoint, data=payload)
    output = response.json()
    assert output == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
