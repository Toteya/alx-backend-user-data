#!/usr/bin/env python3
"""
auth module: implements user authentication
"""
import bcrypt


def _hash_password(password):
    """ Converts and returns the given passsword in bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
