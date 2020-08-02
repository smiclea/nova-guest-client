# Copyright (c) 2018 Cloudbase Solutions Srl
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
import logging

from keystoneauth1 import adapter
from keystoneauth1.exceptions.catalog import EndpointNotFound

from novaguestclient.v1 import networking

LOG = logging.getLogger(__name__)

_DEFAULT_SERVICE_TYPE = 'guest-agent'
_DEFAULT_SERVICE_INTERFACE = 'internal'
_DEFAULT_API_VERSION = 'v1'


class _HTTPClient(adapter.Adapter):
    def __init__(self, session, project_id=None, **kwargs):
        kwargs.setdefault('interface', _DEFAULT_SERVICE_INTERFACE)
        kwargs.setdefault('service_type', _DEFAULT_SERVICE_TYPE)
        kwargs.setdefault('version', _DEFAULT_API_VERSION)
        endpoint = kwargs.pop('endpoint', None)

        super(_HTTPClient, self).__init__(session, **kwargs)

        if endpoint:
            self.endpoint_override = '{0}/{1}'.format(endpoint, self.version)


class Client(object):
    def __init__(self, session=None, *args, **kwargs):
        httpclient = _HTTPClient(session=session, *args, **kwargs)

        self.networking = networking.NetworkingManager(httpclient)
