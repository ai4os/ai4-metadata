"""SHACL validation of RDF graphs (requires the optional ``shacl`` extra)."""

import dataclasses
import pathlib

import rdflib

from ai4_metadata import exceptions


@dataclasses.dataclass
class ValidationReport:
    """Result of validating an RDF graph against a set of SHACL shapes."""

    #: Whether the graph conforms to the shapes.
    conforms: bool
    #: Human readable validation report.
    text: str
    #: Validation report as an RDF graph.
    graph: rdflib.Graph


def validate_graph(
    data_graph: rdflib.Graph, shapes_file: pathlib.Path
) -> ValidationReport:
    """Validate an RDF graph against the SHACL shapes in a Turtle file.

    :param data_graph: RDF graph to validate.
    :param shapes_file: Turtle file with the SHACL shapes to validate against.
    :return: The validation report.

    :raises ShaclNotAvailableError: If pySHACL is not installed.
    """
    try:
        import pyshacl
    except ImportError:
        raise exceptions.ShaclNotAvailableError()

    shapes_graph = rdflib.Graph()
    shapes_graph.parse(shapes_file, format="turtle")

    conforms, report_graph, report_text = pyshacl.validate(
        data_graph, shacl_graph=shapes_graph
    )
    return ValidationReport(
        conforms=bool(conforms), text=str(report_text), graph=report_graph
    )
