"""Tests for the metadata module."""

from jsonschema import validators
import pytest

from ai4_metadata import exceptions
from ai4_metadata import metadata
from ai4_metadata import utils


def test_schemata_files_are_present():
    """Test that all schema files are present and not empty."""
    for k, v in metadata._metadata_version_files.items():
        assert v.exists(), f"Metadata file {k} does not exist"
        assert v.is_file(), f"Metadata file {k} is not a file"
        assert v.stat().st_size > 0, f"Metadata file {k} is empty"


def test_schemata_files_are_valid():
    """Test that all schema files are valid JSON."""
    for version, file_ in metadata._metadata_version_files.items():
        if version == metadata.MetadataVersions.V2_0_0:
            continue
        try:
            schema = utils.load_json(file_)
        except exceptions.InvalidJSONError:
            assert False, f"Metadata file {file_} is not valid JSON"  # noqa: B011
        validator = validators.validator_for(schema)
        assert (
            validator.check_schema(schema) is None
        ), f"Metadata file {file_} is not valid JSON schema"


def test_get_latest_version():
    """Test that the latest version is correct."""
    assert metadata.get_latest_version() != metadata.MetadataVersions.V2_0_0
    assert metadata.get_latest_version() != metadata.MetadataVersions.V1


def test_get_latest_schema_file():
    """Test that the latest schema file is correct."""
    assert (
        metadata.get_latest_schema_file()
        == metadata._metadata_version_files[metadata.get_latest_version()]
    )


def test_get_schema_file_from_metadata():
    """Test that the schema file can be obtained from metadata."""
    for version in metadata.MetadataVersions:
        if version == metadata.MetadataVersions.V1:
            continue
        metadata_dict = {
            "metadata_version": version,
            "schema": "https://example.com/schema.json",
        }
        assert (
            metadata.get_schema_file_from_metadata(metadata_dict)
            == metadata._metadata_version_files[version]
        )

    with pytest.raises(exceptions.InvalidMetadataError):
        metadata.get_schema_file_from_metadata({})


def test_get_latest_schema():
    """Test that the latest schema can be obtained."""
    assert metadata.get_latest_schema() == utils.load_json(
        metadata.get_latest_schema_file()
    )


def test_get_schema_from_metadata():
    """Test that the schema can be obtained from metadata."""
    for version in metadata.MetadataVersions:
        if version == metadata.MetadataVersions.V1:
            continue
        metadata_dict = {
            "metadata_version": version,
            "schema": "https://example.com/schema.json",
        }
        assert metadata.get_schema_from_metadata(metadata_dict) == utils.load_json(
            metadata.get_schema_file(version)
        )

    with pytest.raises(exceptions.InvalidMetadataError):
        metadata.get_schema_from_metadata({})


def test_get_validator_for_schema_file():
    """Test that the validator can be obtained for a schema file."""
    for version in metadata.MetadataVersions:
        schema_file = metadata.get_schema_file(version)
        assert metadata.get_validator_for_schema_file(schema_file) is not None
