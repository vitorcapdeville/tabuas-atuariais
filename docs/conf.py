# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from pathlib import Path
import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "tabatu"
copyright = "2023, Vitor Capdeville"
author = "Vitor Capdeville"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx_design",
]
ROOT_SRC_TREE_DIR = Path(__file__).parents[1]

templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

language = "pt_BR"

master_doc = "index"
source_suffix = ".rst"


def setup(app):
    # https://docs.readthedocs.io/en/latest/guides/adding-custom-css.html
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_js_file
    app.add_js_file(
        "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js"
    )


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = [
    "css/pandas.css",
]
html_theme_options = {
    "external_links": [],
    "github_url": "https://github.com/vitorcapdeville/tabuas-atuariais",
    "logo": {
        "text": "tabatu",
    },
}


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

autosummary_generate = True

default_role = "autolink"

add_function_parentheses = False

autodoc_typehints_format = "short"
autodoc_preserve_defaults = True
autodoc_type_aliases = {"ArrayLike": "ArrayLike"}
autodoc_member_order = "bysource"
