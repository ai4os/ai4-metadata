"""Unit tests for the AI4 vocabularies."""

import pathlib

import pytest
import rdflib
from rdflib.namespace import DCTERMS, SKOS

from ai4_metadata import metadata

RDF_DIR = pathlib.Path(__file__).parent / "../assets/rdf/"


@pytest.mark.parametrize(
    "field, vocabulary",
    [
        ("categories", "ai4eosc-category.ttl"),
        ("tasks", "ai4eosc-tasktype.ttl"),
        ("libraries", "ai4eosc-library.ttl"),
    ],
)
def test_vocabulary_labels_match_schema(field, vocabulary):
    """Test that every vocabulary entry is spelled as in the latest schema."""
    schema = metadata.get_latest_schema()
    allowed = set(schema["properties"][field]["items"]["enum"])

    graph = rdflib.Graph().parse(RDF_DIR / vocabulary, format="turtle")
    labels = {
        str(label)
        for predicate in (SKOS.prefLabel, DCTERMS.title)
        for label in graph.objects(None, predicate)
    }

    assert labels, f"No entries found in {vocabulary}"
    assert labels <= allowed, f"Not in the '{field}' schema: {labels - allowed}"
