Command line interface
======================

The ``ai4-metadata`` command groups all the metadata tools. Metadata files can be
written in either JSON or YAML.

Installation
------------

.. code-block:: console

   $ pip install ai4-metadata

To use the optional SHACL validation, install the ``shacl`` extra:

.. code-block:: console

   $ pip install 'ai4-metadata[shacl]'

Use ``--help`` on any command to see all its options:

.. code-block:: console

   $ ai4-metadata --help
   $ ai4-metadata validate --help

Validate metadata
-----------------

Check a metadata file against the latest version of the metadata schema:

.. code-block:: console

   $ ai4-metadata validate my-module.json

Use ``--metadata-version`` to check against a specific version:

.. code-block:: console

   $ ai4-metadata validate --metadata-version 2.0.0 my-module.json

The command exits with a non-zero code if the file is not valid.

Generate metadata
-----------------

Create a new metadata file with the required fields filled with sample values, to
use as a starting point:

.. code-block:: console

   $ ai4-metadata generate --sample-values --required-only --output my-module.json

Migrate metadata
----------------

Migrate a version 1 metadata file to the latest version:

.. code-block:: console

   $ ai4-metadata migrate --output my-module-v2.json my-module-v1.json

Review the result, as some fields need to be completed by hand.

Profiles
--------

A profile is a way of describing a module with metadata. Two profiles are
supported:

AI4 metadata (``ai4os``)
   Our own metadata profile, in JSON or YAML. It is the input of all the commands.

MLDCAT-AP (``mldcat-ap``)
   An output profile to describe machine learning models as linked data, rendered
   as JSON-LD or Turtle.

See :doc:`profiles` for more details.

Map metadata to other profiles
------------------------------

Map a metadata file to the `MLDCAT-AP <https://semiceu.github.io/MLDCAT-AP/>`_
profile, rendered either as JSON-LD (``jsonld``) or as RDF Turtle (``ttl``):

.. code-block:: console

   $ ai4-metadata map mldcat-ap my-module.json --output-format jsonld --output my-module.jsonld
   $ ai4-metadata map mldcat-ap my-module.json --output-format ttl --output my-module.ttl

Add ``--shacl`` to also check the result against the MLDCAT-AP SHACL shapes (this
requires the ``shacl`` extra). If the result does not conform, the validation report
is printed and no output is written:

.. code-block:: console

   $ ai4-metadata map mldcat-ap my-module.json --output-format ttl --shacl
