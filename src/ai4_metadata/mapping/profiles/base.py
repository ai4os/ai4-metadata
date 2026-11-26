"""Common interface for metadata output profiles."""

import abc
import enum
import json
from typing import Tuple

import rdflib

from ai4_metadata import metadata


class SupportedInputProfiles(str, enum.Enum):
    """Supported input profiles for crosswalks."""

    ai4os = "ai4os"


class SupportedOutputFormats(str, enum.Enum):
    """Supported output formats for crosswalks."""

    jsonld = "jsonld"
    ttl = "ttl"


class Profile(abc.ABC):
    """Interface that every output profile must implement.

    A profile maps AI4 metadata into a JSON-LD document. The JSON-LD document is the
    single source of truth: every other output format is rendered from it.
    """

    #: Name of the profile, used as the CLI sub-command and registry key.
    name: str
    #: One line description of the profile.
    description: str
    #: Output formats that this profile can be rendered into.
    output_formats: Tuple[SupportedOutputFormats, ...]

    @abc.abstractmethod
    def to_jsonld(
        self, from_metadata: dict, metadata_version: metadata.MetadataVersions
    ) -> dict:
        """Map AI4 metadata into a JSON-LD document for this profile.

        :param from_metadata: AI4 metadata, already validated against its schema.
        :param metadata_version: AI4 metadata version of ``from_metadata``.
        :return: JSON-LD document, including its ``@context``.
        """

    def to_graph(self, document: dict) -> rdflib.Graph:
        """Parse a JSON-LD document produced by this profile into an RDF graph."""
        graph = rdflib.Graph()
        graph.parse(data=json.dumps(document), format="json-ld")
        return graph

    def serialize(self, document: dict, to_format: SupportedOutputFormats) -> str:
        """Render a JSON-LD document produced by this profile into ``to_format``."""
        if to_format == SupportedOutputFormats.jsonld:
            return json.dumps(document)
        elif to_format == SupportedOutputFormats.ttl:
            return str(self.to_graph(document).serialize(format="turtle"))
        else:
            raise ValueError(f"Unknown output format '{to_format}'.")
