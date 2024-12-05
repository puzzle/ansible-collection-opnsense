#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024,
# Yoan Müller <ymueller@puzzle.ch>,
# Puzzle ITC
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""system_access_servers"""

__metaclass__ = type

# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html

# fmt: off

DOCUMENTATION = r'''
---
author:
  - Yoan Müller (@LuminatiHD)
module: system_access_servers
short_description: Configure access methods used for authentication on the Webgui
description:
  - "This Module allows you to configure different access methods (ex: LDAP) to secure the Web frontend of the OPNsense firewall."
options:
  description:
    description: "Descriptive name of your access server"
    required: true
    type: str
  type:
    description: "The access type you want to configure"
    default: LDAP
    choices:
      - LDAP
      - LDAP + Timebased One Time Password
      - Local + Timebased One Time Password
      - Radius
      - Voucher
    type: list
    elements: str
  hostname:
    description: "Hostname or IP address of your access server instance"
    required: true
    type: str
  port:
    description: "Port of your access server instance."
    default: 389
    type: int
  transport:
    description: "Transport protocol to use to connect to your server. When choosing StartTLS or SSL, please configure the required private CAs in System -> Trust" # nopep8
    default: TCP - Standard
    choices:
      - TCP - Standard
      - StarTLS
      - SSL - Encrypted
    type: list
    elements: str
  protocol_version:
    description: "Select protocol version"
    default: 3
    choices:
      - 3
      - 2
    type: int
  bind_credentials:
    description: "Bind user and credentials specified with two keys user_dn and password"
    choices:
      - user_dn: <CN=Binduser,OU=Staff,O=Company,DC=example,DC=com>
      - password: <password for bind user>
    type: dict
  search_scope:
    description: "The scope of how many levels the Base DN get searched for users."
    default: "One Level"
    choices:
      - One Level
      - Entire Subtree
    type: list
    elements: str
  authentication_containers:
    description: "Semicolon-separated list of distinguished names DC= components."
    required: true
    type: str
  extended_query:
    description: "Extended LDAP Query to map additional attributes."
    type: str
  initial_template:
    description: "Select if using OpenLDAP, Microsoft AD or Novell eDirectory"
    default: "OpenLDAP"
    choices:
      - OpenLDAP
      - Microsoft AD
      - Novell eDirectory
    type: list
    elements: str
  user_naming_attribute:
    description: "LDAP attribute to map usernames."
    default: "cn"
    type: str
  read_properties:
    description: " Normally the authentication only tries to bind to the remote server, when this option is enabled also the objects properties are fetched, can be practical for debugging purposes. "
    default: false
    type: bool
  synchronize_groups:
    description: "Synchronize groups specified by memberOf or class attribute after login, this option requires to enable read properties. Groups will be extracted from the first CN= section and will only be considered when already existing in OPNsense. Group memberships will be persisted in OPNsense."
    default: false
    type: bool
  constraint_groups:
    description: " Constraint allowed groups to those selected in the container section. This may offer additional security in cases where users are able to inject memberOf attributes in different trees. "
    default: false
    type: bool
  limit_groups:
    description: " Limit the groups which may be used by this authenticator, keep empty to consider all local groups in OPNsense. When groups are selected, you can assign unassigned groups to the user manually "
    default: "Nothing selected"
    type: list
    elements: str
  automatic_user_creation:
    description: " To be used in combination with synchronize groups, allow the authenticator to create new local users after successful login with group memberships returned for the user. "
    default: false
    type: bool
  match_case_insensitive:
    description: " Allow mixed case input when gathering local user settings. "
    default: false
    type: bool
  state:
    description: "Whether to add or update (`present`) or remove (`absent`) an server access configuration."
    type: str
    choices:
       - present
       - absent
'''

EXAMPLES = r'''
---
- name: Configure ldap authentication server without a bind-user
  puzzle.opnsense.system_access_servers:
    description: "My ldap server"
    hostname: "ldap.example.com"
    base_dn: "dc=example,dc=com"
    authentication_container: "ou=sysadmins,dc=example,dc=com"

- name: Configure ldaps authentication server with a bind-user
  puzzle.opnsense.system_access_servers:
    description: "My ldap secured server"
    hostname: "ldap.example.com"
    port: 636
    transport: "SSL - Encrypted"
    bind_credentials:
      user_dn: "uid=mybinduser,ou=bindusers,dc=example,dc=com"
      password: "secret123"
    base_dn: "dc=example,dc=com"
    authentication_container: "ou=sysadmins,dc=example,dc=com"
'''
# pylint: disable=duplicate-code
RETURN = '''
opnsense_configure_output:
    description: A List of the executed OPNsense configure function along with their respective stdout, stderr and rc
    returned: always
    type: list
    sample:
      - function: "opnsense_configure_output"
        params: []
        rc: 0
        stderr: ""
        stderr_lines: []
        stdout: ""
        stdout_lines: []
'''

# pylint: enable=duplicate-code
# fmt: on


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.puzzle.opnsense.plugins.module_utils.config_utils import (
    OPNsenseModuleConfig,
)


def main():
    """
    Main function of the system_access_servers module
    """

    module_args = {
        "description": {
            "required": True,
            "type": "str",
        },
        "type": {
            "default": "LDAP",
            "choices": [
                "LDAP",
                "LDAP + Timebased One Time Password",
                "Local + Timebased One Time Password",
                "Radius",
                "Voucher",
            ],
            "type": "list",
            "elements": "str",
        },
        "hostname": {
            "required": True,
            "type": "str",
        },
        "port": {
            "default": 389,
            "type": "int",
        },
        "transport": {
            "default": "TCP - Standard",
            "choices": ["TCP - Standard", "StarTLS", "SSL - Encrypted"],
            "type": "list",
            "elements": "str",
        },
        "protocol_version": {
            "default": 3,
            "choices": [3, 2],
            "type": "int",
        },
        "bind_credentials": {
            "choices": [
                {"user_dn": "<CN=Binduser,OU=Staff,O=Company,DC=example,DC=com>"},
                {"password": "<password for bind user>"},
            ],
            "type": "dict",
        },
        "search_scope": {
            "default": "One Level",
            "choices": ["One Level", "Entire Subtree"],
            "type": "list",
            "elements": "str",
        },
        "authentication_containers": {
            "required": True,
            "type": "str",
        },
        "extended_query": {
            "type": "str",
        },
        "initial_template": {
            "default": "OpenLDAP",
            "choices": ["OpenLDAP", "Microsoft AD", "Novell eDirectory"],
            "type": "list",
            "elements": "str",
        },
        "user_naming_attribute": {
            "default": "cn",
            "type": "str",
        },
        "read_properties": {
            "default": False,
            "type": "bool",
        },
        "synchronize_groups": {
            "default": False,
            "type": "bool",
        },
        "constraint_groups": {
            "default": False,
            "type": "bool",
        },
        "limit_groups": {
            "default": "Nothing selected",
            "type": "list",
            "elements": "str",
        },
        "automatic_user_creation": {
            "default": False,
            "type": "bool",
        },
        "match_case_insensitive": {
            "default": False,
            "type": "bool",
        },
        "state": {
            "type": "str",
            "choices": ["present", "absent"],
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    result = {
        "changed": False,
        "invocation": module.params,
        "diff": None,
    }
    with OPNsenseModuleConfig(
        module_name="system_access_servers",
        config_context_names=["system_access_servers"],
        check_mode=module.check_mode,
    ) as config:  # pylint: disable=W0612
        pass
    module.exit_json(**result)


if __name__ == "__main__":
    main()
