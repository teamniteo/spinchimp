# -*- coding: utf-8 -*-


class SpinChimpError(Exception):
    """Base class for exceptions in Spin Chimp module."""
    def __init__(self, api_error_msg):
        #api_error_msg respresents raw error string as returned by API server
        super(SpinChimpError, self).__init__()
        self.api_errors = tuple(api_error_msg.split('|'))

    def __str__(self):
        if not self.api_errors:
            return "Exception occurred."
        elif len(self.api_errors) == 1:
            return self.api_errors[0]
        else:
            return "Multiple errors, see api_erros attribute for details."


class WrongParameterName(SpinChimpError):
    """Raised on unsuppported parameter name."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return u"Parameter '{}' does not exist.".format(self.name)


class WrongParameterVal(SpinChimpError):
    """Raised on invalid parameter value."""
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __str__(self):
        return u"Parameter '{}' has a wrong value: '{}'".format(self.name, self.val)


class NetworkError(SpinChimpError):
    """Raised if there are network problems, like timeout."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class AuthenticationError(SpinChimpError):
    """Raised when authentication error occurs."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class QuotaLimitError(SpinChimpError):
    """Raised when API quota limit is reached."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InternalError(SpinChimpError):
    """Raised when unexpected error occurs on the API server when processing a request."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ArticleError(SpinChimpError):
    """Raised when spinning article."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class UnknownError(SpinChimpError):
    """Raised when API call results in an unrecognized error."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
