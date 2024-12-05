#  Copyright: (c) 2024, Puzzle ITC, Fabio Bertagna <bertagna@puzzle.ch>
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
Utilities for firewall_rules module related operations.
"""
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from xml.etree.ElementTree import Element
import time

from ansible_collections.puzzle.opnsense.plugins.module_utils import xml_utils
from ansible_collections.puzzle.opnsense.plugins.module_utils.config_utils import (
    OPNsenseModuleConfig,
)


def uniqid() -> str:
    """
    returns a hex code dependant on the unix timestamp.
    """
    timestamp = time.time()
    sec = int(timestamp)
    msec = int((timestamp - sec) * 1000000)
    return f"{sec:08x}%{msec:05x}"


@dataclass
class AuthServer:
    """
    lal
    """

    refid: str
    auth_type: str = "LDAP"
    name: str = ""
    host: str = ""
    ldap_port: int = 389
    ldap_urltype: str = "TCP - Standart"
    ldap_protver: int = 3
    ldap_scope: int = 1
    ldap_basedn: str = ""
    ldap_authcn: str = ""
    ldap_extended_query: str = ""
    ldap_attr_user: str = ""
    ldap_sync_memberof_groups: List[str] = field(default_factory=list)
    case_insensitive_usernames: bool = False

    def __init__(
        self,
        refid: Optional[str] = None,
        auth_type: str = "LDAP",
        name: str = "",
        host: str = "",
        ldap_port: int = 389,
        ldap_urltype: str = "TCP - Standart",
        ldap_protver: int = 3,
        ldap_scope: int = 1,
        ldap_basedn: str = "",
        ldap_authcn: str = "",
        ldap_extended_query: str = "",
        ldap_attr_user: str = "",
        ldap_sync_memberof_groups: List[str] = [],
        case_insensitive_usernames: bool = False,
        **kwargs,
    ):
        if ldap_scope not in [1, 2]:
            raise ValueError(
                f"Param ldap_scope has to be either 1 or 2, not {ldap_scope}"
            )

        self.auth_type = auth_type
        self.name = name
        self.host = host
        self.ldap_port = ldap_port
        self.ldap_urltype = ldap_urltype
        self.ldap_protver = ldap_protver
        self.ldap_scope = ldap_scope
        self.ldap_basedn = ldap_basedn
        self.ldap_authcn = ldap_authcn
        self.ldap_extended_query = ldap_extended_query
        self.ldap_attr_user = ldap_attr_user
        self.ldap_sync_memberof_groups = ldap_sync_memberof_groups
        self.case_insensitive_usernames = case_insensitive_usernames

        if refid is None:
            self.refid = uniqid()
        else:
            self.refid = refid
        self.extra_attrs = kwargs

    def __eq__(self, _o: "AuthServer"):
        """
        Compare two AuthServers. Comparison is done attribute wise.
        """
        return self.__dict__ == _o.__dict__

    def to_etree(self) -> Element:
        """
        Convert AuthServer instance to XML element
        """
        authserver_dict: dict = asdict(self)
        authserver_dict["type"] = authserver_dict.pop("auth_type")
        authserver_dict["caseInSensitiveUsernames"] = authserver_dict.pop(
            "case_insensitive_usernames"
        )

        ldap_scope_lookup = {1: "one", 2: "subtree"}
        case_insensitive_lookup = {True: 1, False: None}

        authserver_dict["caseInSensitiveUsernames"] = case_insensitive_lookup[
            self.case_insensitive_usernames
        ]
        authserver_dict["ldap_scope"] = ldap_scope_lookup[self.ldap_scope]

        for key, val in authserver_dict.items():
            if isinstance(val, int):
                authserver_dict[key] = str(val)
        element: Element = xml_utils.dict_to_etree("authserver", authserver_dict)[0]

        return element

    # pylint: disable=too-many-locals
    @classmethod
    def from_ansible_module_params(cls, params: dict) -> "AuthServer":
        """
        Creates an instance from Ansible module parameters.

        Args:
            params (dict): Parameters from an Ansible module.

        Returns:
            AuthServer: An instance of AuthServer.

        """
        ldap_scope_lookup = {"One Level": 1, "Entire Subtree": 2}
        ldap_scope = params.get("ldap_scope")
        if ldap_scope is not None:
            ldap_scope = ldap_scope_lookup[ldap_scope]

        interface_assignment_dict = {
            "auth_type": params.get("auth_type"),
            "name": params.get("description"),
            "host": params.get("hostname"),
            "ldap_port": params.get("port"),
            "ldap_urltype": params.get("transport"),
            "ldap_protver": params.get("protocol_version"),
            "ldap_binddn": params.get("bind_user_dn"),
            "ldap_bindpw": params.get("bind_password"),
            "search_scope": ldap_scope,
            "ldap_basedn": params.get("ldap_basedn"),
            "ldap_authcn": params.get("authentication_containers"),
            "ldap_extended_query": params.get("ldap_extended_query"),
            "ldap_attr_user": params.get("ldap_attr_user"),
            "ldap_sync_memberof_groups": params.get("limit_groups"),
            "case_insensitive_usernames": params.get("match_case_insensitive"),
        }

        return cls(**interface_assignment_dict)

    @staticmethod
    def from_xml(element: Element) -> "AuthServer":
        """
        Creates an AuthServer object out of an xml Element
        """
        attrs = dict((subelem.tag, subelem.text) for subelem in element)
        attrs["auth_type"] = attrs.pop("type")

        attr = attrs.pop("caseInSensitiveUsernames")
        if attr is None:
            attrs["case_insensitive_usernames"] = False
        elif attr == 1:
            attrs["case_insensitive_usernames"] = True
        else:
            raise ValueError(
                "Field `case_insensitive_usernames` has to be either empty or 0"
            )

        ldap_scope_lookup = {"one": 1, "subtree": 2}

        attrs["ldap_scope"] = ldap_scope_lookup[attrs["ldap_scope"]]

        return AuthServer(**attrs)


class AuthServerSet(OPNsenseModuleConfig):
    """
    Represents something idk
    """

    _auth_servers: Dict[str, AuthServer]

    def __init__(self, path: str = "/conf/config.xml", **kwargs):
        super().__init__(
            module_name="system_access_servers",
            config_context_names=["system_access_servers"],
            path=path,
            **kwargs,
        )

        self._config_xml_tree = self._load_config()
        self._auth_servers = self._load_servers()

    def _load_servers(self) -> Dict[str, AuthServer]:
        element_tree_rules: Element = self.get("auth_servers")

        auth_servers = [
            AuthServer.from_xml(element)
            for element in element_tree_rules
            if element.tag == "authserver"
        ]

        return dict((server.refid, server) for server in auth_servers)

    @property
    def changed(self) -> bool:
        """
        Checks if the current set of auth servers has changed compared to the
        loaded configuration.

        This property compares the current set of `AuthServer` objects in `_auth_servers`
        with the set loaded from the configuration file. It returns True if there are
        differences, indicating that changes have been made to the set which are
        not yet saved to the configuration file.

        Returns:
            bool: True if the set has changed, False otherwise.
        """
        return self._load_servers() != self._auth_servers

    def get_server_by_id(self, refid: str) -> Optional[AuthServer]:
        """
        Returns the server with the given refid if it is contained in the set. Else None:
        Parameters:
            refid (str): The refid of the server in question
        """
        return self._auth_servers.get(refid)

    def add_or_update(self, server: AuthServer) -> None:
        """
        Adds the server to the set if it's not present, or updates it if it is.
        """
        self._auth_servers[server.refid] = server

    def delete(self, server: AuthServer) -> bool:
        """
        Removes a specified auth server from the set.

        This method iterates through the current set of auth servers and removes the auth server
        that matches the provided `server` parameter. The comparison for removal is based on
        the inequality of the `AuthServer` objects (comparison of attributes as dicts).
        If the rule is not found, no action is taken.

        Parameters:
            server (AuthServer): The auth server to be removed from the set.

        Returns:
            bool: True if server was deleted, False if server was already not present
        """

        if server in self._auth_servers:
            self._auth_servers.pop(server.refid)
            return True
        return False

    def save(self) -> bool:
        """
        Saves the current set of auth servers to the configuration file.

        This method first checks if there have been any changes to the set using the `changed`
        property. If there are no changes, it returns False. Otherwise, it updates the configuration
        XML tree with the current set of auth servers and writes the updated configuration to the file.
        It then reloads the configuration from the file to ensure synchronization.

        The saving process involves removing the existing servers from the configuration XML tree,
        clearing the filter element, and then extending it with the updated set of rules
        converted to XML elements.

        Returns:
            bool: True if changes were saved, False if there were no changes to save.
        """

        if not self.changed:
            return False

        filter_element: Element = self._config_xml_tree.find(
            self._config_maps[self._module_name]["auth_servers"]
        )

        self._config_xml_tree.remove(filter_element)
        filter_element.clear()
        filter_element.extend([rule.to_etree() for rule in self._auth_servers.values()])
        self._config_xml_tree.append(filter_element)
        return super().save(override_changed=True)
