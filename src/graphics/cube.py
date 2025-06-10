# -*- coding: utf-8 -*-
"""
cube module

This module provides a means of storing information about cubes
such as the polygons that the cube itself consists of and their 
x, y, and z offsets

Classes:
- CubeTemplate (Enum class)
- Cube (dataclass)
"""

from dataclasses import dataclass
from dataclasses import field

from typing import List

from enum import Enum

from graphics.shape import Shape

ALL_CUBES = []


class CubeTemplate(Enum):
    """Stores the templates for generating a cube

    CUBE_VERTS represents the vertecies of the cube and CUBE_POLYS
    is a list of polygons where the number within the polygons represent
    the index of the vert
    """

    CUBE_VERTS = (
        (-0.5, -0.5, -0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, 0.5, 0.5),
        (-0.5, 0.5, 0.5),
    )

    CUBE_POLYS = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    )


@dataclass
class Cube:
    """Template for a single cube in 3D space

    This class provides a means of storing information about cubes
    such as the polygons that the cube itself consists of and their
    x, y, and z offsets
    """

    x: int = field()
    y: int = field()
    z: int = field()
    colours: List[str] = field()

    def __post_init__(self) -> None:
        cube = [
            [
                [
                    CubeTemplate.CUBE_VERTS.value[index][0] + self.x,
                    CubeTemplate.CUBE_VERTS.value[index][1] + self.y,
                    CubeTemplate.CUBE_VERTS.value[index][2] + self.z,
                ]
                for index in face_indexes
            ]
            for face_indexes in CubeTemplate.CUBE_POLYS.value
        ]

        self.cube = [Shape(colour, side) for colour, side in zip(self.colours, cube)]

        ALL_CUBES.append(self)


def filter_cubes(cube: Cube, index: int, target: int | float) -> bool:
    """Filteres the cubes at the specified target coordinate

    Args:
        cube (Cube): the cube thats being evaluated
        index (int): the axis thats being evaluated (0=x, 1=y, 2=z)
        target (int | float): the expected location of the cube on the given axis

    Returns:
        bool: if the cube is in that location on the specified axis
    """

    return (
        max(vert[index] for face in cube.cube for vert in face.poly)
        > target
        > min(vert[index] for face in cube.cube for vert in face.poly)
    )
