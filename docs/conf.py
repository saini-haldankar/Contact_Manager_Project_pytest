import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Contact Manager"
author = "Your Name"
copyright = "2026"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
