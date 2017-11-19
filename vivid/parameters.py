"""
Defines several common variable types to be used in API clients.
"""
from requests.auth import (
    HTTPBasicAuth,
    HTTPDigestAuth,
    HTTPProxyAuth,
)
from vivid.exceptions import VariableNotReceived

# Default sentinel to indicate a value wasn't passed to a parameter
NOT_PASSED = object()


class BaseParameter(object):
    """
    Perform basic functions required by most variable types
    """
    def __init__(self, name, key=None, default=NOT_PASSED, required=False):
        """
        Save base information about variable
        """
        self.name = name
        self.key = key or name
        self.default = default
        self.required = required

    def apply(self, request, request_kw):
        """
        Given a request and received arguments, update
        the request to contain the needed parameters.
        """
        val = request_kw.get(self.key, self.default)
        if self.required and val is NOT_PASSED:
            raise VariableNotReceived(
                '{} is a required variable, but was not passed a value, '
                'and did not have a default value set.'.format(self.key)
            )
        elif val is not NOT_PASSED:
            request.setdefault(self.request_kw_key, {})
            request[self.request_kw_key][self.name] = val


class PostBodyParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args
    into the `data` dictionary of the request object to
    be sent in the request body by Requests
    """
    request_kw_key = 'data'

class UrlQueryParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args
    into the `params` dictionary of the request object
    to be appended to the URL by Requests
    """
    request_kw_key = 'params'

class JsonBodyParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args into the
    `json` dictionary of the request object to be serialized
    to JSON and sent in the request body by Requests
    """
    request_kw_key = 'json'

class HeaderParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args into
    the `headers` dictionary of the request object to be sent
    as HTTP header fields by Requests
    """
    request_kw_key = 'headers'

class CookieParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args into
    the `cookies` dictionary of the request object to be sent
    as individual items in the Cookie header field by Requests
    """
    request_kw_key = 'cookies'

class FileParameter(BaseParameter):
    """
    Subclass of BaseParameter that stores received args into
    the `files` dictionary of the request object to be sent
    as individual files using multipart upload by Requests
    """
    request_kw_key = 'cookies'

class UrlTemplateParameter(BaseParameter):

    request_kw_key = 'pending_url_templates'

    def apply(self, request, request_kw):
        super(UrlVariable, self).apply(request, request_kw)
        request.setdefault('followup', {})
        request['followup'][self.request_kw_key] = self.get_applicator()

    @classmethod
    def get_applicator(cls):
        def applicator(request):
            template_params = request.pop(cls.request_kw_key)
            request['url'] = request['url'].format(**template_params)
        return applicator


class BaseAuthParameter(BaseParameter):

    def __init__(self, username_key, password_key, **kwargs):
        self.username_key = username_key
        self.password_key = password_key
        super(BasicAuthVariable, self).__init__('auth', **kwargs)

    def apply(self, request, request_kw):
        username = request_kw.get(self.username_key, NOT_PASSED)
        password = request_kw.get(self.password_key, NOT_PASSED)
        if self.required and (username is NOT_PASSED or password is NOT_PASSED):
            raise VariableNotReceived
        request['auth'] = self.auth_class(username, password)

class BasicAuthParameter(BaseAuthParameter):

    auth_class = HTTPBasicAuth

class ProxyAuthParameter(BaseAuthParameter):

    auth_class = HTTPProxyAuth

class DigestAuthParameter(BaseAuthParameter):

    auth_class = HTTPDigestAuth
