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
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """
        if not excluded_paths:
            return True
        if path is None:
            return True
        if path.rstrip('/') not in [ep.rstrip('/') for ep in excluded_paths]:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request:
            return None
        return request.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None
