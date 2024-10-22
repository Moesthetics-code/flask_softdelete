# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../flask_softdelete'))

# Project information
project = 'flask_softdelete'
copyright = '2024, Mohamed Ndiaye'
author = 'Mohamed Ndiaye'
release = '2.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Options for HTML output
html_theme = 'alabaster'
html_static_path = ['_static']
