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


import argparse
import json
import os
import uuid

from novaguestclient import constants


def format_json_for_object_property(obj, prop_name):
    """ Returns the property given by `prop_name` of the given
    API object as a nicely-formatted JSON string (if it exists) """
    prop = getattr(obj, prop_name, None)
    if prop is None:
        # NOTE: return an empty JSON object string to
        # clearly-indicate it's a JSON
        return "{}"

    if not isinstance(prop, dict) and hasattr(prop, 'to_dict'):
        prop = prop.to_dict()

    return json.dumps(prop, indent=2)


def validate_uuid_string(uuid_obj, uuid_version=4):
    """ Checks whether the provided string is a valid UUID string

        :param uuid_obj: A string or stringable object containing the UUID
        :param uuid_version: The UUID version to be used
    """
    uuid_string = str(uuid_obj).lower()
    try:
        uuid.UUID(uuid_string, version=uuid_version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return True


def add_args_for_json_option_to_parser(parser, option_name):
    """ Given an `argparse.ArgumentParser` instance, dynamically add a group of
    arguments for the option for both an '--option-name' and
    '--option-name-file'.
    """
    option_name = option_name.replace('_', '-')
    option_label_name = option_name.replace('-', ' ')
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('--%s' % option_name,
                           help='JSON encoded %s data' % option_label_name)
    arg_group.add_argument('--%s-file' % option_name,
                           type=argparse.FileType('r'),
                           help='Relative/full path to a file containing the '
                                '%s data in JSON format' % option_label_name)
    return parser


def get_option_value_from_args(args, option_name, error_on_no_value=True):
    """ Returns a dict with the value from of the option from the given
    arguments as set up by calling `add_args_for_json_option_to_parser`
    ('--option-name' and '--option-name-file')
    """
    value = None
    raw_value = None
    option_name = option_name.replace('-', '_')
    option_label_name = option_name.replace('_', ' ')
    option_file_name = "%s_file" % option_name
    option_arg_name = "--%s" % option_name.replace('_', '-')

    raw_arg = getattr(args, option_name)
    file_arg = getattr(args, option_file_name)
    if raw_arg:
        raw_value = raw_arg
    elif file_arg:
        with file_arg as fin:
            raw_value = fin.read()

    if not value and raw_value:
        try:
            value = json.loads(raw_value)
        except ValueError as ex:
            raise ValueError(
                "Error while parsing %s JSON: %s" % (
                    option_label_name, str(ex)))

    if not value and error_on_no_value:
        raise ValueError(
            "No '%s[-file]' parameter was provided." % option_arg_name)

    return value
