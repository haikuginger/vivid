class ParametersMixin(object):
    """
    Mixin looks at the variables present on the object,
    and provides a method for applying each of those
    variables to a given request.
    """
    def apply_parameters(self, request, request_kwargs):
        """
        For each variable defined on the object, give
        the variable the opportunity to apply itself
        to the given pending HTTP request, in the
        context of the current object and the parameters
        that the user passed when calling the requestor.
        """
        for variable in getattr(self, 'parameters', []):
            variable.apply(request, request_kwargs)