"""
BDSM
==================================
Bachelor Data Science Modelling (BDSM) is a collection of methods
and datasets for Data Science as Python Package.
This package aims to provide useful tools for students and
lecturers alike to help to learn and understand Data Science in
python.
"""


# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '0.01.dev'


# Let users know if they're missing any of our hard dependencies
hard_dependencies = ('os', 'pandas', 'numpy')
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
    
del hard_dependencies, dependency, missing_dependencies


import os

from bdsm.datasets import (
    abalones,
    bodyfat,
    iris,
    mall,
    penguins,
    students,
    titanic,
    wine
)

from bdsm.tools import (
    quality,
    standardized_split,
    getpath,
    vif
)


l_datasets = ['abalones', 'bodyfat', 'iris', 'mall', 'penguins', 'students', 'titanic', 'wine']
l_processes = ['wn', 'ma', 'ar', 'arma']
l_tools = ['quality', 'standardized_split', 'getpath', 'vif']

__all__ = l_datasets + l_processes + l_tools
