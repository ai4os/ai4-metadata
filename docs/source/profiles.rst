Metadata profiles
=================

A profile is a way of describing a module with metadata. The AI4 metadata
profile is used as input, and it can be mapped into other output profiles with the
``ai4-metadata map`` command (see :doc:`cli`).

AI4 metadata
------------

:Identifier: ``ai4os``
:Role: Input
:Formats: JSON, YAML

Our own metadata profile, used to describe the AI4OS hub modules. It is defined by
a versioned JSON Schema, available in :doc:`assets`, and there are sample files in
:doc:`examples`.

Use ``ai4-metadata validate`` to check a file against the schema.

MLDCAT-AP
---------

:Identifier: ``mldcat-ap``
:Role: Output
:Version: `MLDCAT-AP 2.1.0 <https://semiceu.github.io/MLDCAT-AP/releases/2.1.0/>`_
:Formats: JSON-LD (``jsonld``), RDF Turtle (``ttl``)

MLDCAT-AP is a profile defined by `SEMIC
<https://interoperable-europe.ec.europa.eu/collection/semic-support-centre>`_ that
extends `DCAT-AP
<https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/dcat-application-profile-data-portals-europe>`_
to describe machine learning models. It is linked data (RDF).

AI4 metadata is converted into MLDCAT-AP with ``ai4-metadata map mldcat-ap``. The
conversion uses a JSON-LD context, available in :doc:`assets`, that maps the AI4
metadata fields to MLDCAT-AP terms.

The result can be checked against the official MLDCAT-AP SHACL shapes with the
``--shacl`` option, which requires the ``shacl`` extra.
