"""Unit tests for the SHACL validation."""

import sys

import pytest
import rdflib
import typer.testing

from ai4_metadata import exceptions
from ai4_metadata import metadata
from ai4_metadata import shacl
from ai4_metadata.cli import app
from ai4_metadata.mapping.profiles import base
from ai4_metadata.mapping.profiles import mldcatap

pytest.importorskip("pyshacl")

runner = typer.testing.CliRunner()

_SHAPES = """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix it6: <http://data.europa.eu/it6/> .

<urn:test:ModelShape> a sh:NodeShape ;
    sh:targetClass it6:MachineLearningModel ;
    sh:property [ sh:path {path} ; sh:minCount 1 ] .
"""


@pytest.fixture
def conforming_shapes_file(tmp_path):
    """Fixture for shapes that the AI4 samples conform to (they have a title)."""
    path = tmp_path / "conforming.ttl"
    path.write_text(_SHAPES.replace("{path}", "dct:title"))
    return path


@pytest.fixture
def failing_shapes_file(tmp_path):
    """Fixture for shapes that the AI4 samples do not conform to."""
    path = tmp_path / "failing.ttl"
    path.write_text(_SHAPES.replace("{path}", "dct:accessRights"))
    return path


def _mldcatap_graph(instance):
    document = mldcatap.PROFILE.to_jsonld(instance, metadata.MetadataVersions.V2)
    return mldcatap.PROFILE.to_graph(document)


def test_validate_graph_conforms(valid_instances, conforming_shapes_file):
    """Test a graph that conforms to the shapes."""
    for instance in valid_instances:
        report = shacl.validate_graph(_mldcatap_graph(instance), conforming_shapes_file)
        assert report.conforms is True
        assert isinstance(report.graph, rdflib.Graph)


def test_validate_graph_does_not_conform(valid_instances, failing_shapes_file):
    """Test a graph that does not conform to the shapes."""
    for instance in valid_instances:
        report = shacl.validate_graph(_mldcatap_graph(instance), failing_shapes_file)
        assert report.conforms is False
        assert "accessRights" in report.text


def test_validate_graph_without_pyshacl(monkeypatch, conforming_shapes_file):
    """Test that an exception is raised when pySHACL is not installed."""
    monkeypatch.setitem(sys.modules, "pyshacl", None)
    with pytest.raises(exceptions.ShaclNotAvailableError):
        shacl.validate_graph(rdflib.Graph(), conforming_shapes_file)


def test_mldcatap_shapes_file_exists():
    """Test that the bundled MLDCAT-AP shapes exist and can be parsed."""
    assert mldcatap.PROFILE.shapes_file is not None
    shapes = rdflib.Graph().parse(mldcatap.PROFILE.shapes_file, format="turtle")
    assert len(shapes) > 0


def test_mldcatap_validate_shacl(valid_instances):
    """Test the validation of the mapping against the bundled MLDCAT-AP shapes."""
    for instance in valid_instances:
        document = mldcatap.PROFILE.to_jsonld(instance, metadata.MetadataVersions.V2)
        report = mldcatap.PROFILE.validate_shacl(document)
        assert isinstance(report, shacl.ValidationReport)
        assert isinstance(report.conforms, bool)


def test_validate_shacl_without_shapes():
    """Test that an exception is raised when the profile has no SHACL shapes."""

    class NoShapesProfile(base.Profile):
        name = "no-shapes"
        description = "Profile without SHACL shapes."
        output_formats = (base.SupportedOutputFormats.jsonld,)
        local_contexts: dict = {}
        shapes_file = None

        def to_jsonld(self, from_metadata, metadata_version):
            return {}

    with pytest.raises(exceptions.InvalidMappingError):
        NoShapesProfile().validate_shacl({})


def _invoke_map_shacl(instance_file):
    return runner.invoke(
        app,
        [
            "map",
            "mldcat-ap",
            instance_file.as_posix(),
            "--output-format",
            "ttl",
            "--shacl",
        ],
    )


def test_cli_shacl_conforms(monkeypatch, valid_instance_files, conforming_shapes_file):
    """Test the CLI when the mapping conforms to the shapes."""
    monkeypatch.setattr(mldcatap.PROFILE, "shapes_file", conforming_shapes_file)
    for instance_file in valid_instance_files:
        result = _invoke_map_shacl(instance_file)
        assert result.exit_code == 0
        assert "MachineLearningModel" in result.stdout


def test_cli_shacl_does_not_conform(
    monkeypatch, valid_instance_files, failing_shapes_file
):
    """Test the CLI when the mapping does not conform to the shapes."""
    monkeypatch.setattr(mldcatap.PROFILE, "shapes_file", failing_shapes_file)
    for instance_file in valid_instance_files:
        result = _invoke_map_shacl(instance_file)
        assert result.exit_code == 1
        assert "MachineLearningModel" not in result.stdout


def test_cli_shacl_without_pyshacl(monkeypatch, valid_instance_files):
    """Test the CLI when pySHACL is not installed."""
    monkeypatch.setitem(sys.modules, "pyshacl", None)
    result = _invoke_map_shacl(valid_instance_files[0])
    assert result.exit_code == 5
