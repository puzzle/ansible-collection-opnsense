#  Copyright: (c) 2024, Puzzle ITC
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
# pylint: skip-file
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch, MagicMock
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import pytest

from ansible_collections.puzzle.opnsense.plugins.module_utils import xml_utils
from ansible_collections.puzzle.opnsense.plugins.module_utils.system_access_servers_utils import (
    AuthServerSet,
    AuthServer,
)
from ansible_collections.puzzle.opnsense.plugins.module_utils.module_index import (
    VERSION_MAP,
)

# Test version map for OPNsense versions and modules

TEST_VERSION_MAP = VERSION_MAP

TEST_XML = """
    <authserver>
      <refid>66751f1da54c1</refid>
      <type>ldap</type>
      <name>test_2</name>
      <host>example.com</host>
      <ldap_port>389</ldap_port>
      <ldap_urltype>TCP - Standard</ldap_urltype>
      <ldap_protver>3</ldap_protver>
      <ldap_scope>one</ldap_scope>
      <ldap_basedn/>
      <ldap_authcn>test</ldap_authcn>
      <ldap_extended_query/>
      <ldap_attr_user>cn</ldap_attr_user>
      <ldap_sync_memberof_groups/>
      <caseInSensitiveUsernames/>
    </authserver>
"""


@pytest.fixture(scope="function")
def sample_config_path(request):
    """
    Fixture that creates a temporary file with a test XML configuration.
    The file  is used in the tests.

    Returns:
    - str: The path to the temporary file.
    """
    with patch(
        "ansible_collections.puzzle.opnsense.plugins.module_utils.version_utils.get_opnsense_version",  # pylint: disable=line-too-long
        return_value="OPNsense Test",
    ), patch.dict(VERSION_MAP, TEST_VERSION_MAP, clear=True):
        # Create a temporary file with a name based on the test function
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(TEST_XML.encode())
            temp_file.flush()
            yield temp_file

    # Cleanup after the fixture is used
    os.unlink(temp_file.name)


def test_xml_to_authserver():
    test_etree_opnsense: Element = ElementTree.fromstring(TEST_XML)
    test_auth_server: AuthServer = AuthServer.from_xml(test_etree_opnsense)
    assert test_auth_server.case_insensitive_usernames is False
    assert test_auth_server.refid == "66751f1da54c1"
