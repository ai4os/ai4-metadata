"""Module to generate mappings from AI4OS metadata to MLDCAT-API."""

import copy
import enum
import json

import rdflib

import ai4_metadata
from ai4_metadata import exceptions


# FIXME(aloga): this is a placeholder for now, change to final value when we merge
# the code in the main branch
_url_prefix = (
    "https://github.com/ai4os/ai4-metadata/raw/refs/heads/mldcat-ap/src/"
    "ai4_metadata/mapping/json-ld/"
)
MetadataVersions = ai4_metadata.MetadataVersions

_JSON_LD_CONTEXT = {
    MetadataVersions.V2: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_2_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_1_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_0_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
}


class SupportedInputProfiles(str, enum.Enum):
    """Supported input profiles for crosswalks."""

    ai4os = "ai4os"


class SupportedOutputFormats(str, enum.Enum):
    """Supported input formats for crosswalks."""

    jsonld = "jsonld"
    ttl = "ttl"


class SupportedOutputProfiles(str, enum.Enum):
    """Supported output profiles for crosswalks."""

    mldcat = "mldcat"


def generate_mapping(
    from_profile: SupportedInputProfiles,
    from_metadata: dict,
    to_format: SupportedOutputFormats,
    metadata_version: MetadataVersions = MetadataVersions.V2,
) -> str:
    """Generate a mapping file for a given input and output format."""
    if from_profile not in SupportedInputProfiles.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"input format `{from_profile}` not supported for MLDCAT-API profile."
        )

    if to_format not in SupportedOutputFormats.__members__:
        raise exceptions.InvalidMappingError(
            msg=f"output format `{to_format}` not supported for MLDCAT-API profile."
        )

    uri = from_metadata.get("links", {}).get("self", "")
    if not uri:
        uri = from_metadata.get("links", {}).get("source_code", "")

    new_meta = copy.deepcopy(from_metadata)
    new_meta["@context"] = _JSON_LD_CONTEXT[metadata_version]
    new_meta["uri"] = uri
    new_meta["type"] = "MachineLearningModel"

    if to_format == SupportedOutputFormats.ttl:
        graph = rdflib.Graph()
        graph.parse(data=json.dumps(new_meta), format="json-ld")
        turtle_data = graph.serialize(format="turtle")
        return str(turtle_data)
    else:
        return str(new_meta)
