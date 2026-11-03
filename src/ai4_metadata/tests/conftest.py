"""Fixtures for the tests."""

import pathlib
import json

import pytest

from ai4_metadata import utils
from ai4_metadata.mapping.profiles import mldcatap


SCHEMATA_DIR = pathlib.Path(__file__).parent / "../assets/schemata/"
INSTANCES_DIR = pathlib.Path(__file__).parent / "../assets/examples/"


@pytest.fixture
def local_mldcat_context(monkeypatch):
    """Use the bundled context with local imported classes for serialization tests."""
    context_file = SCHEMATA_DIR.parent / "json-ld/mldcat-ap-context-2.0.0.jsonld"
    context = json.loads(context_file.read_text(encoding="utf-8"))["@context"]
    # Only these imported classes are emitted by the mapper. Keep their definitions
    # from the MLDCAT-AP 2.1.0 context local, so tests never fetch its @import URL.
    context.pop("@import")
    imported_classes = {
        "MachineLearningModel": "http://data.europa.eu/it6/MachineLearningModel",
        "Repository": "https://linkedpaperswithcode.com/class/repository",
        "Dataset": "http://www.w3.org/ns/dcat#Dataset",
        "Concept": "http://www.w3.org/2004/02/skos/core#Concept",
        "TaskType": "http://data.europa.eu/it6/TaskType",
        "Library": "http://data.europa.eu/it6/Library",
    }
    monkeypatch.setattr(
        mldcatap,
        "get_context_for_version",
        lambda version: {**imported_classes, **context},
    )


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
