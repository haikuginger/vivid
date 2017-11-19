import requests

from vivid.common import ParametersMixin

class BaseApiClient(ParametersMixin, object):
    """
    Base client class that just manages initialization
    arguments and the HTTP session
    """
    def __init__(self, **kwargs):
        """
        Create a session, save the initialization
        arguments, and init any superclasses
        """
        self.session = requests.session()
        self.base_kwargs = kwargs
        super(BaseApiClient, self).__init__()

    def request(self, request_params):
        """
        When called, create an HTTP request using the
        parameters provided. Expect a dictionary-like
        object that complies with Requests' API.
        """
        return self.session.request(**request_params)
