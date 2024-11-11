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
        return False
    
    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None