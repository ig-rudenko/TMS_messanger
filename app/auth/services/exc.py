class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass
