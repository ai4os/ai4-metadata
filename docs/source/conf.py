# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AI4OS/AI4EOSC'
copyright = '2025, AI4EOSC Consortium'
author = 'AI4EOSC Consortium'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "ai4_metadata.sphinxext",
]

# In code blocks, the copy button will exclude:
#   .lineos: line numbers
#   .gp: prompts
#   .go: console outputs
copybutton_exclude = '.linenos, .gp, .go'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'piccolo_theme'
html_static_path = ['_static', 'assets']

html_theme_options = {
    "globaltoc_collapse": False,
    "show_theme_credit": False,
}


html_logo = "_static/ai4eosc-logo.png"
html_show_sourcelink = False
