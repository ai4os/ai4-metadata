"""Module to generate mappings from AI4OS metadata to MLDCAT-API."""

import copy
from typing import Union

from ai4_metadata import metadata
from ai4_metadata import exceptions
from ai4_metadata.mapping.profiles import base


# NOTE(aloga): move to GH pages or documentation as soon as possible.
_url_prefix = "https://docs.ai4os.eu/projects/ai4-metadata/latest/_static/json-ld"
MetadataVersions = metadata.MetadataVersions

_JSON_LD_CONTEXT = {
    MetadataVersions.V2: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_3_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_2_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_1_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
    MetadataVersions.V2_0_0: f"{_url_prefix}/mldcat-ap-context-2.0.0.jsonld",
}


def get_context_for_version(version: MetadataVersions) -> str:
    """Get the context for a given version."""
    try:
        return _JSON_LD_CONTEXT[version]
    except KeyError:
        raise exceptions.InvalidMetadataVersionError(version)


# NOTE(aloga): kept as module level names for backwards compatibility.
SupportedInputProfiles = base.SupportedInputProfiles
SupportedOutputFormats = base.SupportedOutputFormats


class MLDCATAPProfile(base.Profile):
    """MLDCAT-AP output profile."""

    name = "mldcat-ap"
    description = "Map to MLDCAT-AP profile, with different renderings."
    output_formats = (SupportedOutputFormats.jsonld, SupportedOutputFormats.ttl)

    def to_jsonld(
        self, from_metadata: dict, metadata_version: MetadataVersions
    ) -> dict:
        """Map AI4 metadata into an MLDCAT-AP JSON-LD document."""
        uri = from_metadata.get("links", {}).get("self", "")
        if not uri:
            uri = from_metadata.get("links", {}).get("source_code", "")

        new_meta = copy.deepcopy(from_metadata)
        new_meta["@context"] = get_context_for_version(metadata_version)
        new_meta["uri"] = uri
        new_meta["type"] = "MachineLearningModel"

        links = new_meta.pop("links", {})
        new_meta["links"] = {}
        for key, value in links.items():
            new_meta["links"][key] = format_link(key, value)

        for key in ["categories", "tasks", "libraries"]:
            old_meta = new_meta.pop(key, [])
            new_meta[key] = [as_object(cat, key) for cat in old_meta]

        license_ = new_meta.pop("license", None)
        if license_:
            new_meta["license"] = {
                "uri": license_.replace(" ", "_"),
                "title": license_,
                "type": "LicenseDocument",
            }

        return new_meta


PROFILE = MLDCATAPProfile()


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

    document = PROFILE.to_jsonld(from_metadata, metadata_version)
    return PROFILE.serialize(document, to_format)


def format_link(key: str, value: str) -> Union[str, dict]:
    """Format a link to a URI object."""
    if key == "source_code":
        return {
            "uri": value,
            "type": "Repository",
            "title": "Source code",
        }
    elif key == "docker_image":
        return {
            "uri": value,
            "type": "Repository",
            "title": "Docker image",
        }
    elif key == "dataset":
        return {
            "uri": value,
            "type": "Dataset",
            "title": "Dataset",
        }
    else:
        return value


def as_object(object_name: str, object_category: str) -> dict:
    """Convert a dictionary to an object with a given type."""
    object_type_map = {
        "categories": "Concept",
        "tasks": "TaskType",
        "libraries": "Library",
    }

    return {
        "uri": object_name.replace(" ", "_"),
        "title": object_name,
        "type": object_type_map.get(object_category, "Concept"),
    }
