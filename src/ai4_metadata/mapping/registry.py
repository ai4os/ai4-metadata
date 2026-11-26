"""Registry of the available output profiles."""

from typing import Dict, List

from ai4_metadata import exceptions
from ai4_metadata.mapping.profiles import base
from ai4_metadata.mapping.profiles import mldcatap

# NOTE(aloga): new profiles must be added here explicitly.
_PROFILES: Dict[str, base.Profile] = {
    mldcatap.PROFILE.name: mldcatap.PROFILE,
}


def get_profile(name: str) -> base.Profile:
    """Get a registered profile by its name.

    :raises InvalidMappingError: If there is no profile registered with that name.
    """
    try:
        return _PROFILES[name]
    except KeyError:
        raise exceptions.InvalidMappingError(msg=f"profile `{name}` not supported.")


def list_profiles() -> List[str]:
    """Get the names of all the registered profiles."""
    return list(_PROFILES.keys())
