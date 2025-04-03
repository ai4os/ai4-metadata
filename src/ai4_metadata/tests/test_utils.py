"""Test the utils module."""

import json

import pytest

from ai4_metadata import exceptions
from ai4_metadata import utils


def test_load_json(valid_instance_files):
    """Test the load_json method."""
    for aux in valid_instance_files:
        assert utils.load_json(aux) is not None


def test_load_json_not_found(not_found_instance_files):
    """Test the load_json method with a file that does not exist."""
    for aux in not_found_instance_files:
        with pytest.raises(exceptions.FileNotFoundError):
            utils.load_json(aux)


def test_load_yaml(valid_yaml_instance_files):
    """Test the load_yaml method."""
    for aux in valid_yaml_instance_files:
        assert utils.load_yaml(aux) is not None


def test_load_yaml_not_found(not_found_instance_files):
    """Test the load_yaml method with a file that does not exist."""
    for aux in not_found_instance_files:
        with pytest.raises(exceptions.FileNotFoundError):
            utils.load_yaml(aux)


def test_load_invalid_yaml(invalid_instance_files):
    """Test the load_yaml method with an invalid file."""
    for aux in invalid_instance_files:
        with pytest.raises(exceptions.InvalidYAMLError):
            utils.load_yaml(aux)


def test_load_file(valid_instance_files):
    """Test the load_file method."""
    for aux in valid_instance_files:
        assert utils.load_file(aux) is not None


def test_dump_json():
    """Test the dump_json method."""
    data = {"key": "value"}
    assert utils.dump_json(data) is None


def test_dump_json_to_file(tmp_path):
    """Test the dump_json method with a file."""
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    utils.dump_json(data, file_path)
    assert file_path.exists()
    with open(file_path, "r") as f:
        assert json.loads(f.read()) == {"key": "value"}
