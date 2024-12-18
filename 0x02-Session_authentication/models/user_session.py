#!/usr/bin/env python3
"""
user_session module: implements user session persistence
"""
from models.base import Base


class UserSession(Base):
    """
    A user session
    """
    def __init__(self, *args, **kwargs: dict):
        """ Initialise the user session instance
        """
        super().__init__(*args, *kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
