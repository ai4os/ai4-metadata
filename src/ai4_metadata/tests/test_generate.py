"""Regression tests for sample metadata generation."""

import copy
import json
import unittest

from typer.testing import CliRunner

from ai4_metadata import cli, generate, metadata, validate


class TestGenerate(unittest.TestCase):
    """Check generated samples against the supported V2 schemas."""

    def test_samples_validate(self):
        """Full and required-only samples validate without changing the schema."""
        for version in metadata.MetadataVersions:
            if version == metadata.MetadataVersions.V1:
                continue
            for required_only in (False, True):
                with self.subTest(version=version, required_only=required_only):
                    schema = metadata.get_schema(version)
                    original = copy.deepcopy(schema)
                    result = generate.generate(schema, True, required_only)
                    validate.validate(result, schema)
                    self.assertEqual(result["metadata_version"], version.value)
                    self.assertEqual(schema, original)
                    self.assertEqual(
                        generate.generate(schema, True, required_only), result
                    )

    def test_cli_sample_resources(self):
        """The default CLI sample resolves nested resource references."""
        result = CliRunner().invoke(cli.app, ["generate", "--sample-values"])
        self.assertEqual(result.exit_code, 0, result.output)
        sample = json.loads(result.stdout)
        for task in ("inference", "training"):
            self.assertEqual(sample["resources"][task]["cpu"], 1)
            self.assertEqual(sample["resources"][task]["memory_MB"], 8000)
        validate.validate(sample, metadata.get_latest_schema())
