"""Fixtures for the tests."""

import pathlib

import pytest

from ai4_metadata import utils


SCHEMATA_DIR = pathlib.Path(__file__).parent / "../assets/schemata/"
INSTANCES_DIR = pathlib.Path(__file__).parent / "../assets/examples/"


@pytest.fixture(scope="module")
def valid_schema_file():
    """Fixture for a valid schema file."""
    return SCHEMATA_DIR / "ai4-apps-v2.0.0.json"


@pytest.fixture(scope="module")
def all_valid_v2_schema_files():
    """Fixture for all valid v2 schema files."""
    return list(SCHEMATA_DIR.glob("ai4-apps-v2.*.json"))


@pytest.fixture(scope="module")
def invalid_schema_file():
    """Fixture for an invalid schema file."""
    return INSTANCES_DIR / "invalid.json"


@pytest.fixture(scope="module")
def valid_instance_files():
    """Fixture for a valid list of instance files (JSON)."""
    names = ["sample-v2.mods.json", "sample-v2.pytho.json"]
    return [INSTANCES_DIR / name for name in names]


@pytest.fixture(scope="module")
def valid_instances(valid_instance_files):
    """Fixture for a valid instance. This fixture returns a list of instances."""
    return [utils.load_json(i) for i in valid_instance_files]


@pytest.fixture(scope="module")
def valid_yaml_instance_files():
    """Fixture for a valid list of instance files (YAML)."""
    names = ["sample-v2.mods.yaml"]
    return [INSTANCES_DIR / name for name in names]


@pytest.fixture(scope="module")
def valid_yaml_instances(valid_yaml_instance_files):
    """Fixture for a valid instance."""
    return [utils.load_yaml(i) for i in valid_yaml_instance_files]


@pytest.fixture(scope="module")
def invalid_instances():
    """Fixture for an invalid instance."""
    return [{"foo": "bar"}]


@pytest.fixture(scope="module")
def invalid_instance_files():
    """Fixture for an invalid instance."""
    names = ["invalid.json"]
    return [INSTANCES_DIR / name for name in names]


@pytest.fixture(scope="module")
def not_found_instance_files():
    """Fixture for an invalid instance."""
    return [INSTANCES_DIR / "not_found.json"]
