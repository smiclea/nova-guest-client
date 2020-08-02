# Copyright (c) 2016 Cloudbase Solutions Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class NovaGuestAgentException(Exception):
    pass


class HTTPError(Exception):

    """Base exception for HTTP errors."""

    def __init__(self, message, status_code=0):
        super(HTTPError, self).__init__(message)
        self.status_code = status_code


class HTTPServerError(HTTPError):

    """Raised for 5xx responses from the server."""
    pass


class HTTPClientError(HTTPError):

    """Raised for 4xx responses from the server."""
    pass


class HTTPAuthError(HTTPError):

    """Raised for 401 Unauthorized responses from the server."""

    def __init__(self, message, status_code=401):
        super(HTTPAuthError, self).__init__(message, status_code)


class EndpointConnectionValidationFailed(NovaGuestAgentException):
    def __init__(self, validation_message):
        super(EndpointConnectionValidationFailed, self).__init__(
            "Connection validation failed. Details: %s" % validation_message)


class NoUniqueEndpointNameMatch(NovaGuestAgentException):
    """Raised for multiple existing endpoint names found"""

    def __init__(self, cli_arg):
        super(NoUniqueEndpointNameMatch, self).__init__(
            "More than one endpoint exists with the name '%s'. "
            "Please use an ID to be more specific." % (
                cli_arg))


class EndpointIDNotFound(NovaGuestAgentException):
    """Raised when couldn't find endpoint ID that matches endpoint name"""

    def __init__(self, cli_arg):
        super(EndpointIDNotFound, self).__init__(
            "No endpoint found for '%s'" % cli_arg)


class LoggingEndpointNotFound(NovaGuestAgentException):
    """Raised when logging endpoint could not be found in service catalogue"""

    def __init__(self, *args, **kw):
        super(EndpointIDNotFound, self).__init__(
            "no logging endpoint found in service catalogue")
