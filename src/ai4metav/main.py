"""Main module for AI4 metadata validator."""

import argparse
import os
import simplejson as json

from jsonschema import validators


VERSIONS = {
    "1.0.0": os.path.join(os.path.dirname(__file__), "schemata/ai4-apps-v1.0.0.json"),
    "2.0.0": os.path.join(os.path.dirname(__file__), "schemata/ai4-apps-v2.0.0.json"),
}

LATEST_VERSION = "2.0.0"


def load_json(f):
    """Load a JSON from the file f."""
    data = f.read()
    return json.loads(data)


def validate():
    """Validate the schema."""
    parser = argparse.ArgumentParser(
        description=("AI4 application metadata " "(JSON-schema based) " "validator.")
    )

    version_group = parser.add_mutually_exclusive_group()
    # Add argument to specify the schema version to use
    version_group.add_argument(
        "--schema",
        metavar="SCHEMA_JSON",
        type=argparse.FileType("r"),
        help="AI4 application metadata schema file to use. "
             "If set, overrides --metadata-version."
    )

    # Add argument to specify version of the metadata to use
    version_group.add_argument(
        "--metadata-version",
        metavar="VERSION",
        choices=VERSIONS.keys(),
        default=LATEST_VERSION,
        help=f"AI4 application metadata version (default: {LATEST_VERSION})",
    )

    parser.add_argument(
        "instance",
        metavar="METADATA_JSON",
        type=argparse.FileType("r"),
        nargs="+",
        help="DEEP application metadata",
    )
    args = parser.parse_args()

    schema = args.schema or open(VERSIONS[args.metadata_version])

    try:
        schema = load_json(schema)
    except json.JSONDecodeError as e:
        print(f"Error loading schema as JSON: {e}")
        raise

    try:
        validator = validators.validator_for(schema)
        validator.check_schema(schema)
    except Exception as e:
        print(f"Error validating schema: {e}")
        raise

    for f in args.instance:
        instance = load_json(f)
        validators.validate(instance, schema)
