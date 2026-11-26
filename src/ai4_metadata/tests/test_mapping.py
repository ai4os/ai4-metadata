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
