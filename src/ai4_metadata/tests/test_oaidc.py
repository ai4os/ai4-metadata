"""Offline tests for OAI Dublin Core mapping and CLI output."""

import copy
import json
import pathlib
import xml.etree.ElementTree as ET

import pytest
import yaml
from typer.testing import CliRunner

from ai4_metadata import cli, exceptions
from ai4_metadata.mapping.profiles import oaidc

runner = CliRunner()


@pytest.fixture
def dc_metadata():
    """Provide all mapped fields, including repeated values and additional links."""
    return {
        "metadata_version": "3.0.0",
        "title": '  Módulo <modelo> & "日本語"  ',
        "author": ["Author1", "José & María", "Author1"],
        "summary": "Summary",
        "description": "**Description**\nwith a new line",
        "tags": ["tag", "duplicate"],
        "tasks": ["duplicate", "task"],
        "categories": ["category"],
        "identifier": "urn:example:model",
        "links": {
            "self": "https://example.org/metadata",
            "zenodo_doi": "https://doi.org/10.5281/zenodo.123",
            "source_code": "https://example.org/code",
            "docker_image": "https://example.org/image",
            "documentation": "https://example.org/docs",
            "dataset": "https://example.org/data",
            "weights": "https://example.org/weights",
            "custom": "https://example.org/data",
        },
        "dates": {"created": "2026-01-01", "updated": "2026-02-01"},
        "resources": {"unmapped": True},
    }


def elements(xml):
    """Return the ordered local element names and text from XML."""
    return [
        (child.tag.removeprefix(f"{{{oaidc.DC}}}"), child.text)
        for child in ET.fromstring(xml)
    ]


def test_complete_mapping(dc_metadata):
    """Preserve mapping order, namespaces, repeated values, and original input."""
    original = copy.deepcopy(dc_metadata)
    xml = oaidc.generate_mapping(dc_metadata)
    root = ET.fromstring(xml)
    assert xml.startswith("<?xml")
    assert root.tag == f"{{{oaidc.OAI_DC}}}dc"
    assert root.attrib == {f"{{{oaidc.XSI}}}schemaLocation": oaidc.SCHEMA_LOCATION}
    for prefix, uri in (("oai_dc", oaidc.OAI_DC), ("dc", oaidc.DC), ("xsi", oaidc.XSI)):
        assert f'xmlns:{prefix}="{uri}"' in xml
    expected = [
        ("title", dc_metadata["title"]),
        *[("creator", author) for author in dc_metadata["author"]],
        ("description", dc_metadata["summary"]),
        ("description", dc_metadata["description"]),
        *[
            ("subject", v)
            for v in ["tag", "duplicate", "duplicate", "task", "category"]
        ],
        ("identifier", dc_metadata["identifier"]),
        ("identifier", dc_metadata["links"]["zenodo_doi"]),
        *[
            ("relation", v)
            for k, v in dc_metadata["links"].items()
            if k != "zenodo_doi"
        ],
        ("date", "2026-01-01"),
        ("type", "Software"),
    ]
    assert elements(xml) == expected
    assert all(child.tag.startswith(f"{{{oaidc.DC}}}") for child in root)
    assert "&lt;modelo&gt; &amp;" in xml
    assert dc_metadata == original


@pytest.mark.parametrize("description, count", [("same", 1), ("same ", 2)])
def test_description_deduplication(description, count):
    """Only exactly identical descriptions are deduplicated."""
    result = elements(
        oaidc.generate_mapping(
            {"title": "Example", "summary": "same", "description": description}
        )
    )
    assert sum(name == "description" for name, _ in result) == count


@pytest.mark.parametrize("kind", ["module", "tool"])
def test_optional_fields_and_type(kind):
    """Empty optional values are skipped and type is always Software."""
    data = {
        "title": "Example",
        "type": kind,
        "identifier": None,
        "summary": "",
        "description": " \n",
        "tags": [None, "", " "],
        "tasks": None,
        "categories": [],
        "links": {"self": "", "zenodo_doi": None},
        "dates": {"created": None, "updated": {"ignored": True}},
    }
    assert elements(oaidc.generate_mapping(data)) == [
        ("title", "Example"),
        ("type", "Software"),
    ]
    assert elements(
        oaidc.generate_mapping({"title": "Example", "links": None, "dates": None})
    ) == [("title", "Example"), ("type", "Software")]


@pytest.mark.parametrize(
    "data, path",
    [
        ([], "metadata"),
        ({}, "title"),
        ({"title": " "}, "title"),
        ({"title": 1}, "title"),
        ({"title": "bad\x00text"}, "title"),
        ({"summary": []}, "summary"),
        ({"description": False}, "description"),
        ({"identifier": {}}, "identifier"),
        ({"author": "Author1"}, "author"),
        ({"author": [123]}, "author[0]"),
        ({"tags": "tag"}, "tags"),
        ({"tasks": [1]}, "tasks[0]"),
        ({"categories": {}}, "categories"),
        ({"links": []}, "links"),
        ({"links": {"self": []}}, "links.self"),
        ({"links": {"zenodo_doi": 1}}, "links.zenodo_doi"),
        ({"dates": []}, "dates"),
        ({"dates": {"created": 2026}}, "dates.created"),
    ],
)
def test_invalid_fields(data, path):
    """Invalid mapped field types report a useful field path."""
    if isinstance(data, dict) and data and "title" not in data:
        data = {"title": "Example", **data}
    with pytest.raises(exceptions.InvalidMappingError) as error:
        oaidc.generate_mapping(data)
    assert path in str(error.value)


def test_identifiers_are_not_inferred_or_deduplicated():
    """Identifiers come only from explicit identifier fields."""
    data = {"title": "Example", "links": {"self": "urn:example:model"}}
    assert not any(
        name == "identifier" for name, _ in elements(oaidc.generate_mapping(data))
    )
    data["identifier"] = "urn:example:model"
    data["links"]["zenodo_doi"] = "urn:example:model"
    assert [
        value
        for name, value in elements(oaidc.generate_mapping(data))
        if name == "identifier"
    ] == ["urn:example:model"] * 2


def test_proposed_v3_example():
    """Map the proposed example without requiring V3 schema registration."""
    path = pathlib.Path(__file__).parent.parent / "assets/examples/sample-v3.mods.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    result = elements(oaidc.generate_mapping(data))
    assert result[0] == ("title", data["title"])
    assert result[-1] == ("type", "Software")
    assert ("identifier", data["identifier"]) in result
    assert [value for name, value in result if name == "creator"] == data["author"]
    cli_result = runner.invoke(cli.app, ["map", "oai_dc", str(path)])
    assert cli_result.exit_code == 0, cli_result.output
    assert elements(cli_result.stdout) == result


@pytest.mark.parametrize("authors", [None, [], [None, "", "  "]])
def test_empty_authors(authors):
    """Omit empty optional author values."""
    result = elements(oaidc.generate_mapping({"title": "Example", "author": authors}))
    assert result == [("title", "Example"), ("type", "Software")]


@pytest.mark.parametrize("file_format", ["json", "yaml"])
@pytest.mark.parametrize("output_file", [False, True])
def test_cli_mapping(dc_metadata, tmp_path, file_format, output_file):
    """Load JSON/YAML, accept default/explicit XML, and write UTF-8 or stdout."""
    source = tmp_path / f"metadata.{file_format}"
    source.write_text(
        (
            json.dumps(dc_metadata)
            if file_format == "json"
            else yaml.safe_dump(dc_metadata)
        ),
        encoding="utf-8",
    )
    args = ["map", "oai_dc", str(source)]
    target = tmp_path / "metadata.xml"
    if output_file:
        args += ["--output-format", "xml", "-o", str(target)]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 0, result.output
    xml = target.read_text(encoding="utf-8") if output_file else result.stdout
    if output_file:
        assert not result.stdout
    assert elements(xml)[0] == ("title", dc_metadata["title"])
    assert elements(xml)[-1] == ("type", "Software")


@pytest.mark.parametrize("content", ['{"title":', "[]", "{}", '{"title": 123}'])
def test_cli_invalid_input_preserves_output(tmp_path, content):
    """Invalid content reports an error before opening the destination."""
    source = tmp_path / "invalid.json"
    source.write_text(content)
    target = tmp_path / "existing.xml"
    target.write_text("keep me")
    result = runner.invoke(
        cli.app, ["map", "oai_dc", str(source), "--output", str(target)]
    )
    assert result.exit_code == 1
    assert "Error" in result.stderr
    assert not result.stdout
    assert target.read_text() == "keep me"


def test_cli_missing_file(tmp_path):
    """Missing input files return exit code 2."""
    result = runner.invoke(cli.app, ["map", "oai_dc", str(tmp_path / "missing.json")])
    assert result.exit_code == 2
    assert "Error" in result.stderr


def test_cli_invalid_format(tmp_path):
    """Only XML is accepted as an output format."""
    result = runner.invoke(
        cli.app,
        ["map", "oai_dc", str(tmp_path / "input.json"), "--output-format", "jsonld"],
    )
    assert result.exit_code == 2
    assert result.stderr


def test_cli_io_errors(tmp_path):
    """Input and output I/O failures return exit code 4."""
    source = tmp_path / "metadata.json"
    source.write_text('{"title": "Example"}')
    for args in (
        [str(tmp_path)],
        [str(source), "-o", str(tmp_path)],
        [str(source), "-o", str(tmp_path / "missing" / "out.xml")],
    ):
        result = runner.invoke(cli.app, ["map", "oai_dc", *args])
        assert result.exit_code == 4
        assert "Error" in result.stderr
