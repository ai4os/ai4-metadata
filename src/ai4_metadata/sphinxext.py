"""Sphinx extension for generating static HTML metadata pages for metadata classes."""

import collections
import pathlib

from typing import Any, Dict, List

from docutils import nodes
from docutils.parsers.rst import directives
import sphinx.util.docutils
import rdflib
import rdflib.namespace
import sphinx.application
from sphinx.util import logging

import ai4_metadata


LOG = logging.getLogger(__name__)

classes = ["category", "library", "tasktype"]

# Namespace definitions
SKOS = rdflib.namespace.SKOS
RDF = rdflib.namespace.RDF
IT6 = rdflib.Namespace("http://data.europa.eu/it6/")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")

_NAMESPACES = {
    "SKOS": SKOS,
    "IT6": IT6,
}


class SKOSVocabularyDirective(sphinx.util.docutils.SphinxDirective):
    """

    Usage:
    .. skos-vocabulary:: vocabulary_name
       :source: path/to/rdf/file.ttl
       :format: turtle
       :namespace: SKOS
    """

    has_content = False
    required_arguments = 1  # vocabulary name
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        "source": directives.unchanged_required,
        "format": directives.unchanged,
        "namespace": directives.unchanged,
        "base-uri": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        """Run the directive to generate the SKOS vocabulary page."""

        vocabulary_name = self.arguments[0]
        vocabulary_name_normalized = vocabulary_name.strip().lower().replace(" ", "-")
        source_path = pathlib.Path(self.options.get("source", "not provided"))
        rdf_format = self.options.get("format", "turtle")
        namespace = self.options.get("namespace", "SKOS")

        if namespace not in _NAMESPACES:
            LOG.error(
                f"Invalid namespace '{namespace}'. Available namespaces: {list(_NAMESPACES.keys())}"
            )
            return self._create_error_section(f"Invalid namespace '{namespace}'.")

        base_uri = self.options.get(
            "base-uri",
            f"http://w3id.org/ai4os/vocabulary/{vocabulary_name_normalized}/",
        )

        LOG.info(f"SKOS Directive called with: {vocabulary_name}")
        LOG.info(f"Source: {source_path}")
        LOG.info(f"Format: {rdf_format}")
        LOG.info(f"Base URI: {base_uri}")

        if not source_path.is_absolute():
            source_path = self.env.srcdir / source_path

        try:
            # Load and parse the RDF graph
            graph = rdflib.Graph()
            graph.parse(str(source_path), format=rdf_format)

            # Create a proper section with unique ID
            section_id = f"skos-vocabulary-{vocabulary_name_normalized}"
            section = nodes.section(ids=[section_id])

            # Set the section name for TOC purposes
            section["names"] = [section_id]

            # Add title
            title_text = f"{vocabulary_name}"
            title = nodes.title(title_text, title_text)
            section += title

            # Add a subsection with H2 title
            subsection = nodes.section(ids=[f"{section_id}-details"])
            subsection["names"] = [f"{section_id}-details"]

            # This will render as H2
            title_text = f"{base_uri} : A-Z"
            h2_title = nodes.title(title_text, title_text)
            subsection += h2_title

            # Add some content to the subsection
            details_para = nodes.paragraph()
            details_para += nodes.Text(
                "This section contains detailed information about the vocabulary."
            )
            subsection += details_para

            section += subsection

            # # Add vocabulary information
            # self._add_vocabulary_info(section, vocabulary_name, source_path, rdf_format, graph)

            self._format_section(section, namespace, graph)

            LOG.info(
                f"SKOS Directive: Successfully processed vocabulary '{vocabulary_name}'"
            )
            return [section]

        except FileNotFoundError:
            LOG.error(f"SKOS source file not found: {source_path}")
            return self._create_error_section(f"Source file not found: {source_path}")
        except Exception as e:
            LOG.error(f"SKOS Directive error: {e}")
            return self._create_error_section(e)

    def _get_it6_concepts(self, section: nodes.section, graph: rdflib.Graph) -> None:
        """Add a section for IT6 concepts."""

        # NOTE(aloga): Only IT6.Library is supported for now, but we can extend this to
        # other IT6 concepts in the future.
        subjects = list(graph.subjects(predicate=RDF.type, object=IT6.Library))
        aux = collections.OrderedDict()
        for subject in sorted(subjects):
            title = graph.value(subject=subject, predicate=DCT.title)
            version = graph.value(subject=subject, predicate=IT6.version)
            if title is None:
                title = subject
            aux[str(title)] = {"uri": str(subject), "attr": {}}
            for pred in graph.predicates(subject=subject):
                if pred == RDF.type:
                    continue
                # Get the values for the predicate
                values = graph.objects(subject=subject, predicate=pred)
                # Store the values in the attributes dict
                aux[str(title)]["attr"][str(pred)] = [str(value) for value in values]
        return aux

    def _get_skos_concepts(self, section: nodes.section, graph: rdflib.Graph) -> None:
        """Add a section for vocabulary concepts."""

        subjects = list(graph.subjects(predicate=RDF.type, object=SKOS.Concept))
        # Create a sorted dict, that will be as follows
        # aux = {"label": {"uri": "uri", attributes: {"attribute": "value"}}}
        aux = collections.OrderedDict()
        for subject in sorted(subjects):
            LOG.debug(f"Found SKOS concept: {subject}")
            label = graph.value(subject=subject, predicate=SKOS.prefLabel)
            if label is None:
                label = subject
            label_str = str(label)
            aux[label_str] = {"uri": str(subject), "attr": {}}
            for pred in graph.predicates(subject=subject):
                if pred == RDF.type:
                    continue
                # Get the values for the predicate
                values = graph.objects(subject=subject, predicate=pred)
                # Store the values in the attributes dict
                aux[label_str]["attr"][str(pred)] = [str(value) for value in values]
        return aux

    def _format_section(
        self, section: nodes.section, namespace: str, graph: rdflib.Graph
    ) -> None:
        if namespace == "SKOS":
            aux = self._get_skos_concepts(section, graph)
        elif namespace == "IT6":
            aux = self._get_it6_concepts(section, graph)

        concepts_section = nodes.section(ids=["concepts"])
        concepts_section["names"] = ["concepts"]

        if not aux:
            LOG.warning("Nothing found in the vocabulary.")
            concepts_section += nodes.paragraph(
                text="Nothing found in this vocabulary."
            )
            section += concepts_section
            return

        # Create a list for concepts
        concepts_list = nodes.bullet_list()

        for entry_label, entry_vals in aux.items():
            LOG.info(
                f"Processing vocabulary entry: {entry_label} with values: {entry_vals}"
            )

            uri = entry_vals["uri"]
            attributes = entry_vals["attr"]
            notation = attributes.get(str(SKOS.notation), None)
            if notation is None:
                LOG.info(
                    f"'{entry_label}' does not have SKOS concept notation, using label."
                )
                notation = entry_label.strip().replace(" ", "_")

            # Create a list item for each concept
            concept_node = nodes.list_item(ids=[f"{notation}"])

            # Add raw HTML for the link
            raw_html = f'<a href="{uri}" target="_blank">{entry_label}</a>'
            concept_node += nodes.raw(raw_html, raw_html, format="html")

            concept_attributes_list = nodes.bullet_list()
            for attr, values in attributes.items():
                # Create a list item for each attribute
                attribute_item = nodes.list_item()
                attribute_text = f"{attr.split('/')[-1]}: {', '.join(values)}"
                attribute_node = nodes.paragraph(text=attribute_text)
                attribute_item += attribute_node
                concept_attributes_list += attribute_item

            concept_node += concept_attributes_list
            concepts_list += concept_node

        concepts_section += concepts_list

        LOG.info(f"Adding concepts section with {len(aux)} concepts.")
        section += concepts_section

    def _create_error_section(self, error_message: str) -> List[nodes.Node]:
        """Create an error section when something goes wrong."""

        error_section = nodes.section(ids=["skos-error"])
        error_section["names"] = ["skos-error"]

        error_title = nodes.title("SKOS Vocabulary Error", "SKOS Vocabulary Error")
        error_section += error_title

        error_para = nodes.paragraph()
        error_para += nodes.strong(text="Error: ")
        error_para += nodes.Text(error_message)
        error_section += error_para

        return [error_section]


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Setup function for the Sphinx extension"""

    app.add_directive("skos-vocabulary", SKOSVocabularyDirective)

    meta = {
        "version": ai4_metadata.__version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
    LOG.info(f"Loaded ai4_metadata Sphinx extension version {ai4_metadata.__version__}")

    return meta
