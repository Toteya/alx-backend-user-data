#!/usr/bin/env python3
"""
auth module: implements user authentication
"""
import bcrypt
from db import DB
from db import NoResultFound
from typing import Type
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Type[User]:
        """ Registers and returns a user based on the given email and password
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        return self._db.add_user(email=email, hashed_password=hashed_password)


def _hash_password(password: str) -> bytes:
    """ Converts and returns the given passsword in bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password