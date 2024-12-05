# Copyright: (c) 2023, Puzzle ITC
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Tests for the ansible_collections.puzzle.opnsense.plugins.modules.system_access_servers"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from tempfile import NamedTemporaryFile
from unittest.mock import patch
import os


from ansible_collections.puzzle.opnsense.plugins.module_utils.module_index import (
    VERSION_MAP,
)

from ansible_collections.puzzle.opnsense.plugins.module_utils.config_utils import (
    OPNsenseModuleConfig,
)


import pytest


TEST_VERSION_MAP = {"OPNsense Test": {"system_access_servers": {}}}

XML_CONFIG: str = """<?xml version="1.0"?>
    <opnsense>
    </opnsense>
    """


@pytest.fixture(scope="function")
def sample_config(request):
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
            temp_file.write(request.param.encode())
            temp_file.flush()
        with OPNsenseModuleConfig(
            module_name="system_access_servers",
            config_context_names=["system_access_servers"],
            path=temp_file.name,
            check_mode=True,
        ) as config:
            yield config

    # Cleanup after the fixture is used
    os.unlink(temp_file.name)


@pytest.mark.parametrize("sample_config", [XML_CONFIG], indirect=True)
def test_empty(sample_config):
    pass
