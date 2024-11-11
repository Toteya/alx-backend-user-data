#!/usr/bin/env python3
"""
basic_auth: Basic Authorization
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header for a Basic
        Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """ Returns the decodes value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_utf_str = decoded_bytes.decode('utf-8')
        except base64.binascii.Error:
            return None

        return decoded_utf_str

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header.split(':')[1]
        return email, password
