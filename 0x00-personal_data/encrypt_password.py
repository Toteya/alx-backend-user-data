#!/usr/bin/env python3
"""
encrypt password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password
    """
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(bytes_password, salt)
    return hash
