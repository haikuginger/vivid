from vivid.common import ParametersMixin

class Endpoint(ParametersMixin, object):
    """
    Descriptor that describes an attribute which acts
    as a function making an HTTP request. Return a
    bound endpoint attached to this and the base API.
    """    
    def __init__(self, method, path, *parameters):
        """
        Save relevant data at init; this includes the
        path component of the URL we want, as well as
        the HTTP method, and any endpoint-specific vars.
        """
        self.method = method
        self.path = path
        self.parameters = parameters
        super(Endpoint, self).__init__()

    def __get__(self, instance, _owner):
        """
        Return a bound endpoint object tied to both this
        object and to the parent BaseApiClient instance.
        """
        return BoundEndpoint(self, instance)


class BoundEndpoint(object):

    def __init__(self, endpoint, api_instance):
        """
        Store links to both the unbound endpoint and the
        API client instance we're bound to
        """
        self.endpoint = endpoint
        self.api_instance = api_instance

    def __call__(self, **kwargs):
        """
        Handle being called like a function
        """
        request = {
            'method': self.endpoint.method,
            'url': self.full_url
        }
        request_kwargs = self.get_base_kwargs()
        request_kwargs.update(kwargs)
        self.apply_parameters(request, request_kwargs)
        return self.api_instance.request(request)

    def apply_parameters(self, request, request_kwargs):
        """
        Apply endpoint- and client-defined parameters to the request
        """
        self.api_instance.apply_parameters(request, request_kwargs)
        self.endpoint.apply_parameters(request, request_kwargs)
        self.finalize(request)

    def get_base_kwargs(self):
        """
        Get the base kwargs from the instance
        """
        return self.api_instance.base_kwargs.copy()

    @property
    def full_url(self):
        """
        Build a complete URL for the bound endpoint
        """
        return self.api_instance.root + self.endpoint.path

    def finalize(self, request):
        """
        Do any followup/cleanup work that any variables requested.
        """
        followup_work = request.pop('followup', {})
        for item in followup_work.values():
            item(request)