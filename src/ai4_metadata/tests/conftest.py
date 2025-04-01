"""Fixtures for the tests."""

import pathlib

import pytest

from ai4_metadata import utils


@pytest.fixture(scope="module")
def valid_schema_file():
    """Fixture for a valid schema file."""
    return pathlib.Path(__file__).parent / "../schemata/ai4-apps-v2.0.0.json"


@pytest.fixture(scope="module")
def all_valid_v2_schema_files():
    """Fixture for all valid v2 schema files."""
    return list(pathlib.Path(__file__).parent.glob("../schemata/ai4-apps-v2.*.json"))


@pytest.fixture(scope="module")
def invalid_schema_file():
    """Fixture for an invalid schema file."""
    return pathlib.Path(__file__).parent / "../../../instances/invalid.json"


@pytest.fixture(scope="module")
def valid_instance_files():
    """Fixture for a valid list of instance files (JSON)."""
    names = ["sample-v2.mods.json", "sample-v2.pytho.json"]
    return [
        pathlib.Path(__file__).parent / "../../../instances" / name for name in names
    ]


@pytest.fixture(scope="module")
def valid_instances(valid_instance_files):
    """Fixture for a valid instance. This fixture returns a list of instances."""
    return [utils.load_json(i) for i in valid_instance_files]


@pytest.fixture(scope="module")
def valid_yaml_instance_files():
    """Fixture for a valid list of instance files (YAML)."""
    names = ["sample-v2.mods.yaml"]
    return [
        pathlib.Path(__file__).parent / "../../../instances" / name for name in names
    ]


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
    return [
        pathlib.Path(__file__).parent / "../../../instances" / name for name in names
    ]


@pytest.fixture(scope="module")
def not_found_instance_files():
    """Fixture for an invalid instance."""
    return [pathlib.Path(__file__).parent / "foo/bar/baz/instance.json"]
