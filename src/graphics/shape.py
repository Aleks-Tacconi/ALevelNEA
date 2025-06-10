# -*- coding: utf-8 -*-
"""
shape module

This module provides means of storing data regarding each invidiual 3D
face of a geometric shape, such as its colour and coordinates

Classes:
- Shape (dataclass)

Functions:
- rotate_shape: rotates a shape and returns the new poly
- render_shape: renders a shape on the given tkinter canvas
"""

import tkinter as tk
import math

from dataclasses import dataclass
from dataclasses import field

from typing import List
from typing import Sequence
from typing import Callable
from typing import Any

from graphics.engine import transform_coord
from graphics.engine import rotate_x
from graphics.engine import rotate_y

ALL_SHAPES = []


@dataclass
class Shape:
    """Stores info about a 3D face

    This class stores information about a 3D face such as
    its colour and coordinates and its x and y orientation
    """

    colour: str = field()
    poly: List[List[float | int]] = field()
    orientation_x: int | float = field(default=45)
    orientation_y: int | float = field(default=45)

    def __post_init__(self) -> None:
        ALL_SHAPES.append(self)


def rotate_shapes(
    shapes: List[Shape], angle_x: int | float, angle_y: int | float
) -> None:
    """Rotates the shapes by the given x and y angle

    Args:
        shapes (List[Shape]): the shapes that will be rotated
        angle_x (int | float): the angle that the shape will be rotated by (x axis)
        angle_y (int | float): the angle that the shape will be rotated by (y axis)

    Returns:
        None
    """

    for shape in shapes:
        shape.orientation_x += angle_x
        shape.orientation_y += angle_y


def rotate_shape(
    shape: Shape, angle_x: int | float, angle_y: int | float
) -> List[List[float | int]]:
    """Rotates the shape

    Rotates a shape using its orientation_x and orientation_y attributes

    Args:
        shape (Shape): the shape thats being rotated
        angle_x (int | float): the angle that the shape will be rotated by (x axis)
        angle_y (int | float): the angle that the shape will be rotated by (y axis)

    Returns:
        List[List[float | int]]: the rotated shape
    """

    polygon = [rotate_x(coord, [0, 0, 0], angle_x) for coord in shape.poly]
    polygon = [rotate_y(coord, [0, 0, 0], angle_y) for coord in polygon]

    return polygon


def render_shape(
    canvas: tk.Canvas,
    shape: Shape,
    camera_pos: Sequence[float | int],
) -> None:
    """Renders the given shape

    This function renders the given shape on the given
    tkinter canvas that is passed as an argument

    Args:
        canvas (tk.Canvas): the tkinter canvas on
            which the shape will be rendered
        shape (Shape): the shape that will be rendered
        camera_pos (Sequence[int | float]): the position of the camera

    Returns:
        None
    """

    polygon = [
        [coord - cam_coord for coord, cam_coord in zip(coords, camera_pos)]
        for coords in rotate_shape(shape, shape.orientation_x, shape.orientation_y)
    ]
    polygon = [coord + canvas.winfo_width() // 2 if i % 2 == 0 else coord + canvas.winfo_height() // 2 for coords in polygon for i, coord in enumerate(transform_coord(coords))]

    canvas.create_polygon(*polygon, fill=shape.colour, outline="black")

def merge_sort(arr: List[Any], func: Callable) -> List[Any]:
    """Returns a sorted version of the array passed in

    This function recursively sorts the array using the merge sort algorithm

    Args:
        arr (List[Any]): the array that will be sorted
        func (Callable): a function that will be applied to each item in
            the array when making the comparision in the merge part of the algorithm

    Returns:
        List[Any]: the sorted array
    """
    length = len(arr)

    if length == 1:
        return arr

    array_one = arr[:length // 2]
    array_two = arr[length // 2:]

    array_one = merge_sort(array_one, func)
    array_two = merge_sort(array_two, func)

    return merge(array_one, array_two, func)

def merge(array_one, array_two, func):
    array_three = []

    while array_one and array_two:
        if func(array_one[0]) > func(array_two[0]):
            array_three.append(array_two.pop(0))
        else:
            array_three.append(array_one.pop(0))

    array_three += array_one
    array_three += array_two

    return array_three


def get_sorted_shapes(
    shapes: List[Shape],
    camera_pos: Sequence[float | int],
) -> List[Shape]:
    """Sorts the shapes by distance from the camera

    Uses 3D pythagerous to sort the shapes from furthest to
    closest (relative to the position of the camera)

    Args:
        shapes (List[Shape]): the list of shapes that will get sorted
        camera_pos (Sequence[float | int]): the position of the camera

    Returns:
        List[Shape]: the sorted shapes
    """

    rotated_shapes = [
        rotate_shape(shape, shape.orientation_x, shape.orientation_y)
        for shape in shapes
    ]

    sorted_shapes = merge_sort(
        list(zip(shapes, rotated_shapes)),
        lambda shapes: sum(
            math.sqrt(
                (camera_pos[2] - vert[2]) ** 2
                + (camera_pos[1] - vert[1]) ** 2
                + (camera_pos[0] - vert[0]) ** 2
            )
            for vert in shapes[1]
        )
    )[::-1]

    return [shape for shape, _ in sorted_shapes]
