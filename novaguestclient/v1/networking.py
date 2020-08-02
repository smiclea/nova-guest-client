# Copyright (c) 2017 Cloudbase Solutions Srl
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

from novaguestclient import base
from novaguestclient import exceptions


class Networking(base.Resource):
    pass


class NetworkingManager(base.BaseManager):
    resource_class = Networking

    def __init__(self, api):
        super(NetworkingManager, self).__init__(api)

    def apply_networking(self, instance_id):
        data = self.client.post(
            '/networking/%s/actions' % instance_id,
            json={'apply-networking': None}).json()
        validate_data = data["apply-networking"]
        return validate_data.get("success"), validate_data.get("message")
