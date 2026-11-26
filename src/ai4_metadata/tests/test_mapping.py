"""Unit tests for the mapping profile registry and interface."""

import pytest

from ai4_metadata import exceptions
from ai4_metadata.mapping import registry
from ai4_metadata.mapping.profiles import base
from ai4_metadata.mapping.profiles import mldcatap


def test_list_profiles():
    """Test that the MLDCAT-AP profile is registered."""
    assert registry.list_profiles() == ["mldcat-ap"]


def test_get_profile():
    """Test that a registered profile can be retrieved by name."""
    profile = registry.get_profile("mldcat-ap")
    assert profile is mldcatap.PROFILE
    assert isinstance(profile, base.Profile)


def test_get_invalid_profile():
    """Test that an exception is raised when the profile is not registered."""
    with pytest.raises(exceptions.InvalidMappingError):
        registry.get_profile("invalid-profile")


def test_profile_is_abstract():
    """Test that the profile interface cannot be instantiated."""
    with pytest.raises(TypeError):
        base.Profile()  # type: ignore[abstract]


def test_serialize_invalid_format():
    """Test that serializing into an unknown format raises an exception."""
    with pytest.raises(ValueError):
        mldcatap.PROFILE.serialize({}, "invalid_format")  # type: ignore[arg-type]


def test_resolve_context_import(tmp_path):
    """Test that an @import is replaced by the imported context, placed first."""
    imported = tmp_path / "imported.jsonld"
    imported.write_text('{"@context": {"a": "http://example.org/a"}}')
    local_contexts = {"http://example.org/imported.jsonld": imported}
    context = {"@import": "http://example.org/imported.jsonld", "b": "@id"}

    resolved = base.resolve_context(context, local_contexts)

    assert resolved == [{"a": "http://example.org/a"}, {"b": "@id"}]


def test_resolve_context_url(tmp_path):
    """Test that a context URL is replaced by the bundled context."""
    local = tmp_path / "local.jsonld"
    local.write_text('{"@context": {"a": "http://example.org/a"}}')
    local_contexts = {"http://example.org/local.jsonld": local}

    resolved = base.resolve_context(
        ["http://example.org/local.jsonld", {"b": "@id"}], local_contexts
    )

    assert resolved == [{"a": "http://example.org/a"}, {"b": "@id"}]


def test_resolve_context_not_bundled():
    """Test that an exception is raised for a context without bundled copy."""
    with pytest.raises(exceptions.InvalidMappingError):
        base.resolve_context("http://example.org/missing.jsonld", {})


def test_mldcatap_local_contexts_exist():
    """Test that all the MLDCAT-AP bundled contexts exist."""
    for url, path in mldcatap.PROFILE.local_contexts.items():
        assert path.is_file(), f"Missing bundled context for {url}"
