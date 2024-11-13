#!/usr/bin/env python3
"""
auth: authentication module
"""
from typing import List
from typing import TypeVar
import os


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
        excl_paths = [ep.rstrip('/') for ep in excluded_paths]
        for excl_path in excl_paths:
            if '*' in excl_path and excl_path.rstrip('*') in path.rstrip('/'):
                return False
        if path.rstrip('/') not in excl_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        
        return request.cookies.get(os.getenv('SESSION_NAME'))
