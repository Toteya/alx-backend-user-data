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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates the password against the hashed_password
    """
    bytes_password = password.encode('utf-8')

    return bcrypt.checkpw(bytes_password, hashed_password)
