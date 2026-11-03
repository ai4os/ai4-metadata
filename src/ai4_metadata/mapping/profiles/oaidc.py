"""Map AI4OS metadata to OAI Dublin Core XML."""

import enum
import pathlib
from typing import Optional
from typing_extensions import Annotated
import xml.etree.ElementTree as ET

import typer

from ai4_metadata import exceptions, utils

OAI_DC = "http://www.openarchives.org/OAI/2.0/oai_dc/"
DC = "http://purl.org/dc/elements/1.1/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_LOCATION = f"{OAI_DC} http://www.openarchives.org/OAI/2.0/oai_dc.xsd"

app = typer.Typer(help="Map AI4OS metadata to OAI Dublin Core XML.")


class SupportedOutputFormats(str, enum.Enum):
    """Supported serializations for OAI Dublin Core."""

    xml = "xml"


def _text(value: object, path: str) -> Optional[str]:
    """Read optional text without normalizing its content."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.InvalidMappingError(f"{path}: expected a string")
    if not value.strip():
        return None
    if any(
        not (
            char in "\t\n\r"
            or 0x20 <= ord(char) <= 0xD7FF
            or 0xE000 <= ord(char) <= 0xFFFD
            or 0x10000 <= ord(char) <= 0x10FFFF
        )
        for char in value
    ):
        raise exceptions.InvalidMappingError(f"{path}: invalid XML 1.0 character")
    return value


def _object(value: object, path: str) -> dict:
    """Read an optional object."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise exceptions.InvalidMappingError(f"{path}: expected an object")
    return value


def generate_mapping(from_metadata: dict) -> str:
    """Generate standalone OAI Dublin Core XML from the mapped fields only."""
    if not isinstance(from_metadata, dict):
        raise exceptions.InvalidMappingError("metadata: expected an object")

    title = _text(from_metadata.get("title"), "title")
    if title is None:
        raise exceptions.InvalidMappingError("title: a nonblank string is required")

    ET.register_namespace("oai_dc", OAI_DC)
    ET.register_namespace("dc", DC)
    ET.register_namespace("xsi", XSI)
    root = ET.Element(f"{{{OAI_DC}}}dc", {f"{{{XSI}}}schemaLocation": SCHEMA_LOCATION})

    def add(name: str, value: Optional[str]) -> None:
        if value is not None:
            ET.SubElement(root, f"{{{DC}}}{name}").text = value

    add("title", title)
    authors = from_metadata.get("author")
    if authors is not None:
        if not isinstance(authors, list):
            raise exceptions.InvalidMappingError("author: expected a list of strings")
        for index, author in enumerate(authors):
            add("creator", _text(author, f"author[{index}]"))

    descriptions = set()
    for field in ("summary", "description"):
        value = _text(from_metadata.get(field), field)
        if value is not None and value not in descriptions:
            add("description", value)
            descriptions.add(value)

    for field in ("tags", "tasks", "categories"):
        values = from_metadata.get(field)
        if values is None:
            continue
        if not isinstance(values, list):
            raise exceptions.InvalidMappingError(f"{field}: expected a list of strings")
        for index, value in enumerate(values):
            add("subject", _text(value, f"{field}[{index}]"))

    add("identifier", _text(from_metadata.get("identifier"), "identifier"))
    links = _object(from_metadata.get("links"), "links")
    add("identifier", _text(links.get("zenodo_doi"), "links.zenodo_doi"))
    for key, value in links.items():
        if key != "zenodo_doi":
            add("relation", _text(value, f"links.{key}"))

    dates = _object(from_metadata.get("dates"), "dates")
    add("date", _text(dates.get("created"), "dates.created"))
    add("type", "Software")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")


@app.command(name="oai_dc", help="Map AI4OS metadata to OAI Dublin Core XML.")
def _map(
    from_file: Annotated[
        pathlib.Path, typer.Argument(help="JSON or YAML file to map.")
    ],
    to_format: Annotated[
        SupportedOutputFormats,
        typer.Option("--output-format", help="Output serialization."),
    ] = SupportedOutputFormats.xml,
    output: Annotated[
        Optional[pathlib.Path], typer.Option("--output", "-o", help="Output XML file.")
    ] = None,
) -> None:
    """Load metadata and emit XML after validating the mapped fields."""
    try:
        mapping = generate_mapping(utils.load_file(from_file))
        if output is None:
            typer.echo(mapping)
        else:
            output.write_text(mapping, encoding="utf-8")
    except exceptions.FileNotFoundError as error:
        utils.format_rich_error(error)
        raise typer.Exit(2)
    except (
        exceptions.InvalidFileError,
        exceptions.InvalidMappingError,
        UnicodeError,
    ) as error:
        utils.format_rich_error(error)
        raise typer.Exit(1)
    except OSError as error:
        utils.format_rich_error(error)
        raise typer.Exit(4)
