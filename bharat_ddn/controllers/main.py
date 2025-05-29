import jwt
import datetime
import random
import logging
import requests  # Import requests to send API call
from odoo import http
from odoo.http import request, Response
from odoo import models, fields
import json
import random

_logger = logging.getLogger(__name__)

import jwt

from odoo.exceptions import AccessError, UserError
from functools import wraps


def check_permission(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.httprequest.headers.get('Authorization')

        if not token:
            raise AccessError('Authorization header is missing or invalid')

        try:
            # Check if the token starts with "Bearer " and extract it
            if token.startswith("Bearer "):
                token = token[7:]

            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded_token['user_id']

            # Check if the user exists
            user = request.env['res.users'].sudo().search([('id', '=', user_id)])
            if not user:
                raise AccessError('Invalid user or token')

            # You can assign the user to the request object if needed
            request.env.user = user

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')

        # Proceed to the actual function after permission check
        return func(self, *args, **kwargs)

    return wrapper

