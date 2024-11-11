#!/usr/bin/env python3
"""
auth: authentication module
"""
from flask import request
from typing import List
from typing import TypeVar


class Auth:
    """
    Authentication classs
    """
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """ Require auth
        """
        if not excluded_path:
            return True
        if path is None:
            return True
        if path.strip('/') not in [ep.strip('/') for ep in excluded_path]:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None
