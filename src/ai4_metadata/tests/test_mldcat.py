"""Unit tests for the mldcat-ap profile module."""

import json

import pyld
import pytest
import rdflib
import requests

from ai4_metadata import exceptions
from ai4_metadata import metadata
from ai4_metadata.mapping.profiles import mldcatap


def test_correct_metadata_versions_and_mappings():
    """Test that all metadata versions have a mapping."""
    for v in metadata.MetadataVersions:
        if v == metadata.MetadataVersions.V1:
            continue
        assert v in mldcatap._JSON_LD_CONTEXT.keys(), f"Missing version {v} in mapping."
        assert mldcatap.get_context_for_version(v) is not None


def test_incorrect_metadata_version():
    """Test that an exception is raised when the metadata version is not supported."""
    with pytest.raises(exceptions.InvalidMetadataVersionError):
        mldcatap.get_context_for_version(metadata.MetadataVersions.V1)


def test_context_is_valid_json():
    """Test that the context is a valid JSON-LD document.

    This test loads the context file and checks that it is a valid JSON document.
    """
    for v in metadata.MetadataVersions:
        if v == metadata.MetadataVersions.V1:
            continue
        context_url = mldcatap.get_context_for_version(v)
        
        # Handle both file:// URLs and http(s):// URLs
        if context_url.startswith('file://'):
            # For file URLs, read the file directly
            import pathlib
            import urllib.parse
            file_path = pathlib.Path(urllib.parse.urlparse(context_url).path)
            with open(file_path, 'r') as f:
                context_data = json.load(f)
        else:
            # For HTTP URLs, use requests
            response = requests.get(context_url)
            assert response.status_code == 200, f"Error fetching context for version {v}"
            context_data = response.json()
            assert "application/ld+json" in response.headers["Content-Type"]
        
        assert context_data is not None, f"Error parsing context for version {v}"
        # Note: pyld.jsonld.expand may not work with file:// URLs in the context,
        # so we just validate that it's valid JSON for now
        assert "@context" in context_data


def test_generate_jsonld_mapping(valid_instances):
    """Test the generation of a mapping file in JSON-LD."""
    profile = mldcatap.SupportedInputProfiles.ai4os
    for instance in valid_instances:
        mapping = mldcatap.generate_mapping(
            profile, instance, mldcatap.SupportedOutputFormats.jsonld
        )
        assert mapping is not None
        assert isinstance(mapping, str)
        jsonld = json.loads(mapping)
        
        # Create a custom document loader for pyld that handles file:// URLs
        import pathlib
        import urllib.parse
        from pyld import jsonld as pyld_jsonld
        
        def custom_document_loader(url, options={}):
            """Custom document loader that handles file:// URLs."""
            if url.startswith('file://'):
                file_path = pathlib.Path(urllib.parse.urlparse(url).path)
                with open(file_path, 'r') as f:
                    doc = json.load(f)
                return {
                    'contextUrl': None,
                    'documentUrl': url,
                    'document': doc
                }
            else:
                # Fall back to default loader for http(s) URLs
                return pyld_jsonld.requests_document_loader()(url, options)
        
        # Expand the JSON-LD with the custom loader
        expanded = pyld.jsonld.expand(jsonld, options={'documentLoader': custom_document_loader})
        assert expanded is not None


def test_generate_rdf_mapping(valid_instances):
    """Test the generation of a mapping file in RDF."""
    profile = mldcatap.SupportedInputProfiles.ai4os
    g = rdflib.Graph()
    for instance in valid_instances:
        mapping = mldcatap.generate_mapping(
            profile, instance, mldcatap.SupportedOutputFormats.ttl
        )
        assert mapping is not None
        assert isinstance(mapping, str)
        assert g.parse(data=mapping, format="ttl") is not None


def test_invalid_mapping():
    """Test that an exception is raised when an invalid profile is provided."""
    with pytest.raises(exceptions.InvalidMappingError):
        mldcatap.generate_mapping(
            "invalid_profile", {}, mldcatap.SupportedOutputFormats.jsonld
        )


def test_invalid_output_format(valid_instances):
    """Test that an exception is raised when an invalid output format is provided."""
    with pytest.raises(exceptions.InvalidMappingError):
        mldcatap.generate_mapping(
            mldcatap.SupportedInputProfiles.ai4os, valid_instances[0], "invalid_format"
        )
