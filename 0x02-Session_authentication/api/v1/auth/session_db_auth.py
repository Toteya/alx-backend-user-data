#!/usr/bin/env python3
"""
session_db_auth module: Implements user session storage and retrieval
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    User session storage
    """
    def create_session(self, user_id: str = None) -> str:
        """ Creates and stores a new user session instance.
        Returns the session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user id based on the given session id
        """

        if session_id is None:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except (KeyError, IndexError) as error:
            return None
        user_id = user_session.user_id
        if self.session_duration <= 0:
            return user_id

        td_duration = timedelta(seconds=self.session_duration)
        if user_session.created_at + td_duration < datetime.utcnow():
            user_session.remove()
            return None
        return user_id

    def destroy_session(self, request=None) -> bool:
        """ Deletes the user session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_session = UserSession.search({'user_id': session_id})[0]
        user_session.remove()
        return True
