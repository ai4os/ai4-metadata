# AI4 Metadata utilities

[![GitHub license](https://img.shields.io/github/license/ai4os/ai4-metadata.svg)](https://github.com/ai4os/ai4-metadata/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/ai4os/ai4-metadata.svg)](https://github.com/ai4os/ai4-metadata/releases)
[![PyPI](https://img.shields.io/pypi/v/ai4-metadata.svg)](https://pypi.python.org/pypi/ai4-metadata)
[![Python versions](https://img.shields.io/pypi/pyversions/ai4-metadata.svg)](https://pypi.python.org/pypi/ai4-metadata)

[![DOI](https://zenodo.org/badge/721337407.svg)](https://zenodo.org/doi/10.5281/zenodo.13343453)

Metadata utilities for the AI4OS hub data science applications.

The AI4OS hub data science applications use metadata to describe the data
sources, models, and other resources. The metadata is used to validate the
resources and to provide information to the users.

## Installation

The metadata utilities can be installed using pip:

    $ pip install ai4-metadata

## Usage

The AI4 metadata utilities can be invoked from the command line. The utilities
provide commands to validate and migrate the metadata files.

    $ ai4-metadata --help

### Metadata validation

The metadata utilities provide a command-line interface (CLI) tool
`ai4-metadata-validate` that can be used to validate the metadata files. The
CLI tool accepts the metadata files as input parameters.

    $ ai4-metadata validate instances/sample-v2.mods.json
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ 'instances/sample-v2.mods.json' is valid for version 2.0.0                 │
    ╰────────────────────────────────────────────────────────────────────────────╯

Different metadata versions can be specified, either by using the
`--metadata-version` or by providing the metadata schema file. The following
two executions are equivalent:

    $ ai4-metadata validate --metadata-version 2.0.0 instances/sample-v2.mods.json
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ 'instances/sample-v2.mods.json' is valid for version 2.0.0                 │
    ╰────────────────────────────────────────────────────────────────────────────╯
    $ ai4-metadata validate --schema schemata/ai4-apps-v2.0.0.json instances/sample-v2.mods.json
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ 'instances/sample-v2.mods.json' is valid for version 2.0.0                 │
    ╰────────────────────────────────────────────────────────────────────────────╯
    $ ai4-metadata validate --metadata-version 1.0.0 instances/sample-v2.mods.json
    ╭─ Error ────────────────────────────────────────────────────────────────────╮
    │ Error validating instance 'instances/sample-v2.mods.json': 'date_creation' │
    │ is a required property                                                     │
    ╰────────────────────────────────────────────────────────────────────────────╯

Metadata files can be present in either JSON or YAML format. The metadata
utilities will automatically detect the format.

    $ ai4-metadata validate instances/sample-v2.mods.yaml
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ 'instances/sample-v2.mods.yaml' is valid for version 2.0.0                 │
    ╰────────────────────────────────────────────────────────────────────────────╯
    $ ai4-metadata validate instances/sample-v2.mods.json
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ 'instances/sample-v2.mods.json' is valid for version 2.0.0                 │
    ╰────────────────────────────────────────────────────────────────────────────╯

### Metadata migration

The metadata utilities provide a command-line interface (CLI) tool
`ai4-metadata-migrate` that can be used to migrate the metadata files from V1
to latest V2. To save the output, use the `--output` option.

    $ ai4-metadata migrate --output sample-v2.mods.json instances/sample-v1.mods.json
    ╭─ Success ──────────────────────────────────────────────────────────────────╮
    │ V1 metadata 'instances/sample-v1.mods.json' migrated to version            │
    │ MetadataVersions.V2 and stored in 'sample-v2.mods.json'                    │
    ╰────────────────────────────────────────────────────────────────────────────╯

Please review the changes, as the metadata migration is not complete, and
manual steps are needed.

## Acknowledgements

<img width=300 align="left" src="https://raw.githubusercontent.com/AI4EOSC/.github/ai4eosc/profile/EN-Funded.jpg" alt="Funded by the European Union" />

This project has received funding from the European Union’s Horizon Research and Innovation programme under Grant agreement No. [101058593](https://cordis.europa.eu/project/id/101058593)
