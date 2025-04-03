"""Test migration from V1 to V2 of the metadata."""

import json

from ai4_metadata import migrate


def test_migrate(tmp_path):
    """Test the migrate function."""
    v1_metadata = {
        "metadata_version": "1.0.0",
        "title": "test_app",
        "description": ["Test application"],
        "keywords": ["tensorflow", "keras", "scikit-learn", "trainable", "inference"],
        "doi": "10.1234/doi",
        "sources": {
            "zenodo_doi": "10.1234/zenodo.1234567",
            "pre_trained_weights": "https://example.com/weights",
            "ai4_template": "https://example.com/template",
        },
        "dataset_url": "https://example.com/dataset",
        "training_files_url": "https://example.com/training_files",
        "cite_url": "https://example.com/cite",
    }

    # v1_metadata has to be sent as a file
    v1_metadata_file = tmp_path / "v1_metadata.json"
    with open(v1_metadata_file, "w") as f:
        f.write(json.dumps(v1_metadata))

    v2_metadata = migrate.migrate(v1_metadata_file)

    assert v2_metadata["metadata_version"] == migrate.metadata.get_latest_version()
    assert v2_metadata["title"] == v1_metadata["title"]
    assert v2_metadata["description"] == " ".join(v1_metadata["description"])
    assert v2_metadata["links"]["doi"] == v1_metadata["doi"]
    assert v2_metadata["links"]["zenodo_doi"] == v1_metadata["sources"]["zenodo_doi"]
    assert (
        v2_metadata["links"]["weights"] == v1_metadata["sources"]["pre_trained_weights"]
    )
    assert (
        v2_metadata["links"]["ai4_template"] == v1_metadata["sources"]["ai4_template"]
    )
    assert v2_metadata["links"]["dataset_url"] == v1_metadata["dataset_url"]
    assert (
        v2_metadata["links"]["training_files_url"] == v1_metadata["training_files_url"]
    )
    assert v2_metadata["links"]["cite_url"] == v1_metadata["cite_url"]
    assert "TensorFlow" in v2_metadata["libraries"]
    assert "Keras" in v2_metadata["libraries"]
    assert "Scikit-Learn" in v2_metadata["libraries"]
    assert "AI4 inference" in v2_metadata["categories"]
    assert "AI4 pre trained" in v2_metadata["categories"]
