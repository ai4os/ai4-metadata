"""Common interface for metadata output profiles."""

import abc
import enum
import json
import pathlib
from typing import Any, Dict, List, Tuple

import rdflib

from ai4_metadata import exceptions
from ai4_metadata import metadata
from ai4_metadata import utils


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
    #: Bundled copies of the remote JSON-LD contexts used by this profile, as a
    #: mapping of context URL to local file. Used to build RDF graphs offline.
    local_contexts: Dict[str, pathlib.Path]

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
        """Parse a JSON-LD document produced by this profile into an RDF graph.

        Remote contexts are replaced by their bundled copies (see
        :attr:`local_contexts`), so no network access is needed.
        """
        document = dict(document)
        document["@context"] = resolve_context(
            document["@context"], self.local_contexts
        )
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


def resolve_context(context: Any, local_contexts: Dict[str, pathlib.Path]) -> List:
    """Replace remote JSON-LD contexts by their bundled copies.

    Context URLs (either used directly or through ``@import``) are replaced by the
    ``@context`` of the matching local file. An ``@import`` is replaced by placing the
    imported context before the importing one, so that the importing context terms
    take precedence, as defined by JSON-LD 1.1. Scoped contexts inside term
    definitions are left untouched.

    :param context: Value of a JSON-LD ``@context``.
    :param local_contexts: Mapping of context URL to local file.
    :return: Equivalent context, as a list of context definitions.

    :raises InvalidMappingError: If a context URL has no bundled copy.
    """
    if isinstance(context, list):
        resolved = []
        for item in context:
            resolved.extend(resolve_context(item, local_contexts))
        return resolved

    if isinstance(context, str):
        if context not in local_contexts:
            raise exceptions.InvalidMappingError(
                msg=f"no bundled copy of JSON-LD context `{context}`."
            )
        local_document = utils.load_json(local_contexts[context])
        return resolve_context(local_document["@context"], local_contexts)

    context = dict(context)
    imported = context.pop("@import", None)
    if imported is None:
        return [context]
    return resolve_context(imported, local_contexts) + [context]
