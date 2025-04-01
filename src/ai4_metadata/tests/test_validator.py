"""Unit tests for the validator module."""

import pytest

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata import utils
from ai4_metadata import validate


def test_validator(valid_schema_file, valid_instance_files):
    """Test the validator with a loaded JSON."""
    for aux in valid_instance_files:
        assert validate.validate(utils.load_json(aux), valid_schema_file) is None


def test_validator_all_schemas(all_valid_v2_schema_files, valid_instance_files):
    """Test the validator with all valid v2 schema files."""
    for schema_file in all_valid_v2_schema_files:
        for aux in valid_instance_files:
            assert validate.validate(utils.load_json(aux), schema_file) is None


def test_validator_default_schema(valid_instance_files):
    """Test the validator with the default schema."""
    schema_file = metadata.get_schema(metadata.get_latest_version())
    for aux in valid_instance_files:
        assert validate.validate(utils.load_json(aux), schema_file) is None


def test_validator_all_schema_files(valid_instance_files):
    """Test the validator with all schema files."""
    for metadata_version in metadata.MetadataVersions:
        if metadata_version == metadata.MetadataVersions.V1:
            continue
        schema_file = metadata.get_schema(metadata_version)
        for aux in valid_instance_files:
            assert validate.validate(utils.load_json(aux), schema_file) is None


def test_validator_file(valid_schema_file, valid_instances):
    """Test the validator with a JSON file."""
    for aux in valid_instances:
        assert validate.validate(aux, valid_schema_file) is None


def test_validator_yaml(valid_schema_file, valid_yaml_instances):
    """Test the validator with a loaded YAML."""
    for aux in valid_yaml_instances:
        assert validate.validate(aux, valid_schema_file) is None


def test_validator_yaml_file(valid_schema_file, valid_yaml_instance_files):
    """Test the validator with a YAML file."""
    for aux in valid_yaml_instance_files:
        assert validate.validate(aux, valid_schema_file) is None


def test_validator_invalid_instance(valid_schema_file, invalid_instances):
    """Test the validator with an invalid instance."""
    for aux in invalid_instances:
        with pytest.raises(exceptions.MetadataValidationError):
            validate.validate(aux, valid_schema_file)


def test_validator_invalid_instance_file(valid_schema_file, invalid_instance_files):
    """Test the validator with an invalid instance file."""
    for aux in invalid_instance_files:
        with pytest.raises(exceptions.MetadataValidationError):
            validate.validate(utils.load_json(aux), valid_schema_file)


def test_validator_not_found_instance_file(valid_schema_file, not_found_instance_files):
    """Test the validator with a not found instance file."""
    for aux in not_found_instance_files:
        with pytest.raises(exceptions.FileNotFoundError):
            validate.validate(utils.load_json(aux), valid_schema_file)


def test_validator_invalid_schema(invalid_schema_file, valid_instances):
    """Test the validator with an invalid schema."""
    for aux in valid_instances:
        with pytest.raises(exceptions.SchemaValidationError):
            validate.validate(aux, invalid_schema_file)


def test_validator_invallid_all(invalid_schema_file, invalid_instances):
    """Test the validator with an invalid schema and instance."""
    for aux in invalid_instances:
        with pytest.raises(exceptions.SchemaValidationError):
            validate.validate(aux, invalid_schema_file)
