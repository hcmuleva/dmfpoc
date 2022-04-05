import os
import sys
from pathlib import Path

import jwt
SECRET_SALT="PIONEER_KI_DEN"
def encode_auth_token(user_id, role_list):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'user_id': user_id,
            'user_role':role_list
        }
        return jwt.encode(
            payload,SECRET_SALT,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        return jwt.decode(auth_token,SECRET_SALT,options={"verify_signature": True}, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
