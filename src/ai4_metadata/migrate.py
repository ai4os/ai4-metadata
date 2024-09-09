"""Migrate metadata from V1 to V2."""

import collections
import datetime
import pathlib
from typing_extensions import Annotated
from typing import Any, Optional
import warnings

import typer

import ai4_metadata
from ai4_metadata import validate
from ai4_metadata import utils

app = typer.Typer(help="Migrate an AI4 metadata file from V1 to V2.")


def migrate(instance_file: pathlib.Path) -> collections.OrderedDict:
    """Try to migrate metadata from V1 to latest V2."""
    v1_metadata = utils.load_json(instance_file)

    v2: collections.OrderedDict[str, Any] = collections.OrderedDict()

    v2["metadata_version"] = ai4_metadata.get_latest_version().value
    v2["title"] = v1_metadata.get("title")
    v2["summary"] = v1_metadata.get("summary")
    v2["description"] = " ".join(v1_metadata.get("description", []))
    v2["dates"] = {
        "created": v1_metadata.get("date_creation"),
        "updated": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    v2["links"] = {
        "source_code": v1_metadata.get("sources", {}).get("code"),
        "docker_image": v1_metadata.get("sources", {}).get("docker_registry_repo"),
    }
    v2["tags"] = v1_metadata.get("keywords", [])
    v2["tasks"] = []
    v2["categories"] = []
    v2["libraries"] = []

    # Now move things, if present, into links
    if v1_metadata.get("doi"):
        v2["links"]["doi"] = v1_metadata.get("doi")
    if v1_metadata.get("sources", {}).get("zenodo_doi"):
        v2["links"]["zenodo_doi"] = v1_metadata.get("sources", {}).get("zenodo_doi")
    if v1_metadata.get("sources", {}).get("pre_trained_weights"):
        v2["links"]["weights"] = v1_metadata.get("sources", {}).get(
            "pre_trained_weights"
        )
    if v1_metadata.get("sources", {}).get("ai4_template"):
        v2["links"]["ai4_template"] = v1_metadata.get("sources", {}).get("ai4_template")

    if v1_metadata.get("dataset_url"):
        v2["links"]["dataset_url"] = v1_metadata.get("dataset_url")
    if v1_metadata.get("training_files_url"):
        v2["links"]["training_files_url"] = v1_metadata.get("training_files_url")
    if v1_metadata.get("cite_url"):
        v2["links"]["cite_url"] = v1_metadata.get("cite_url")

    # Try to infer some some more information on libraries and categories
    kw = [k.lower() for k in v1_metadata.get("keywords", [])]
    if "tensorflow" in kw:
        v2["libraries"].append("TensorFlow")
    if "pytorch" in kw:
        v2["libraries"].append("PyTorch")
    if "keras" in kw:
        v2["libraries"].append("Keras")
    if "scikit-learn" in kw:
        v2["libraries"].append("Scikit-Learn")

    if "trainable" in kw:
        v2["categories"].append("AI4 trainable")
    if "inference" in kw:
        v2["categories"].append("AI4 inference")
        v2["categories"].append("AI4 pre trained")

    return v2


@app.command(name="migrate")
def main(
    v1_metadata: Annotated[
        pathlib.Path, typer.Argument(help="AI4 application metadata file to migrate.")
    ],
    output: Annotated[
        Optional[pathlib.Path],
        typer.Option("--output", "-o", help="Output file for migrated metadata."),
    ] = None,
):
    """Migrate an AI4 metadata file from V1 to the latest V2 version."""
    v1_schema = ai4_metadata.get_schema(ai4_metadata.MetadataVersions.V1)
    validate.validate(v1_metadata, v1_schema)

    # Migrate metadata
    v2_metadata = migrate(v1_metadata)
    v2_version = ai4_metadata.get_latest_version()
    v2_schema = ai4_metadata.get_schema(v2_version)
    validate.validate(v2_metadata, v2_schema)

    # Write out the migrated metadata
    utils.dump_json(v2_metadata, output)
    if output:
        utils.format_rich_ok(
            f"V1 metadata '{v1_metadata}' migrated to version {v2_version} and "
            f"stored in '{output}'",
        )


def migrate_main():
    """Run the migration command as an independent script."""
    # NOTE(aloga): This is a workaround to be able to provide the command as a separate
    # script, in order to be compatible with previous versions of the package. However,
    # this will be not be supported in the next major version of the package, therfore
    # we mark it as deprecated and raise a warining
    msg = (
        "The 'ai4-metadata-migrate' command is deprecated and will be removed "
        "in the next major version of the package, please use 'ai4-metadata migrate' "
        "instead."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    utils.format_rich_warning(DeprecationWarning(msg))
    typer.run(main)
