# -*- coding: utf-8 -*-
"""
rubix_cube package

This package provides a means of interacting with the 3D cubes that
make up the rubix cube whilst keeping track of the rotations using 2D
arrays and allowing for the cube to be solved
"""

from .rubix_2d import Rubix2D
from .rubix_cube import RubixCube

__all__ = ["Rubix2D", "RubixCube"]
