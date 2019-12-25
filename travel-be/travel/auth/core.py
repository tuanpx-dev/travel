from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from .token import decode_token


class JwtAuthentication(BaseAuthentication):
    """
    Authentication class to retrieve a token from headers and
     to validate the token.
    """
    NULL_TOKEN = 'null'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            raise exceptions.AuthenticationFailed("Authorization header must be supplied.")
        elif len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header')
        elif auth[0].lower() != b'bearer':
            raise exceptions.AuthenticationFailed('Invalid token header')
        try:
            token = auth[1]
            if token == self.NULL_TOKEN:
                raise exceptions.AuthenticationFailed('Null token not allowed')
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid '
                                                  'characters.')
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        token = decode_token(token)
        user = token.user
        if user is None:
            raise exceptions.AuthenticationFailed("User does not exist")
        return user, token

    def authenticate_header(self, request):
        return 'Bearer'
