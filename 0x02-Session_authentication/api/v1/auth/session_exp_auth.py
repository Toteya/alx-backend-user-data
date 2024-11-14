#!/usr/bin/env python3
"""
session_exp_auth module: Session Authentication expiration
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Session Authentication Expiration class
    """
    def __init__(self):
        """ Initialise authentication instance
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except ValueError:
            self.session_duration = 0
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session id for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user id based on the given session id
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        user_id = session_dictionary.get('user_id')
        if self.session_duration <= 0:
            return user_id
        if session_dictionary.get('created_at') is None:
            return None
        td_duration = timedelta(seconds=self.session_duration)
        if session_dictionary.get('created_at') + td_duration < datetime.now():
            return None
        return user_id
