#!/usr/bin/env python3
"""
auth module: implements user authentication
"""
import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from db import NoResultFound
from typing import Type
from user import User
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates the login credentials (email and password) provided
        by the user
        """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def _generate_uuid(self) -> str:
        """ Generates and returns a UUID
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """ Creates a new session_id for the given user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Type[User]:
        """ Returns the user matching the given session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """ Destroys a session
        """
        self._db.update_user(user_id=user_id, session_id=None)


def _hash_password(password: str) -> bytes:
    """ Converts and returns the given passsword in bytes
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
