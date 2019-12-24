import re
import logging
from travel.auth.token import decode_token, UnauthorizedToken

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(object):

    re_auth_header = re.compile(r'^Bearer\s+(.+)$')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.token = self._authenticate(request)
        logger.info(f"Token: {request.token}")
        return self.get_response(request)

    def _authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        if auth is None:
            return UnauthorizedToken()
        raw_token = self._parse_authorization_header(auth)
        return decode_token(raw_token)

    def _parse_authorization_header(self, auth_string):
        matched = self.re_auth_header.match(auth_string)
        if not matched:
            return None
        return matched.group(1)
