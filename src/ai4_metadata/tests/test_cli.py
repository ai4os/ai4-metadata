"""Unit tests for the command line interface."""

import typer.testing

import ai4_metadata
from ai4_metadata import cli

runner = typer.testing.CliRunner()
app = cli.app


# Test validation

def test_cli_validate(valid_instance_files):
    """Test the CLI with a valid instance."""
    for aux in valid_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix()])
        assert result.exit_code == 0
        assert "Success" in result.stdout


def test_cli_validate_quiet(valid_instance_files):
    """Test the CLI with a valid instance and the quiet flag."""
    for aux in valid_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix(), "--quiet"])
        assert result.exit_code == 0
        assert not result.stdout


def test_cli_validate_list_deprecated(valid_instance_files):
    """Test the CLI with a list of valid instances."""
    result = runner.invoke(
        app, ["validate"] + [aux.as_posix() for aux in valid_instance_files]
    )
    assert result.exit_code == 0
    assert "Success" in result.stdout
    assert "Warning" in result.stdout


def test_cli_metadata_file_not_found(not_found_instance_files):
    """Test the CLI with a metadata file that does not exist."""
    for aux in not_found_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix()])
        assert result.exit_code == 2
        assert "Error" in result.stdout


def test_cli_metadata_file_not_found_quiet(not_found_instance_files):
    """Test the CLI with a metadata file that does not exist and the quiet flag."""
    for aux in not_found_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix(), "--quiet"])
        assert result.exit_code == 2
        assert "Error" in result.stdout


def test_cli_invalid_instance(invalid_instance_files):
    """Test the CLI with an invalid instance."""
    for aux in invalid_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix()])
        assert result.exit_code == 1
        assert "Error" in result.stdout


def test_cli_invalid_schema(invalid_schema_file, valid_instance_files):
    """Test the CLI with an invalid schema."""
    for aux in valid_instance_files:
        result = runner.invoke(
            app, ["validate", aux.as_posix(), "--schema", invalid_schema_file]
        )
        assert result.exit_code == 3
        assert "Error" in result.stdout


def test_cli_unexpected_error(valid_instance_files):
    """Test the CLI with an unexpected error."""
    for aux in valid_instance_files:
        result = runner.invoke(app, ["validate", aux.as_posix(), "--schema", "."])
        assert result.exit_code == 4
        assert "Error" in result.stdout


# Test version is eager

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert ai4_metadata.__version__ in result.stdout
