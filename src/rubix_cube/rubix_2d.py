# -*- coding: utf-8 -*-
"""
rubix_2d module

This module provides a way to represent a rubix cube
in the form of 2D arrays and rotate thoose arrays

Classes:
- Rubix2D

Functions:
- rotate_side: Rotates the side of the rubix cube specified by index
- rotate_arr: Rotates an array 90 clockwise [iters] times
"""

from typing import List
from typing import Any

import copy

INVERSE = {0: 2, 1: 1, 2: 0}


class Rubix2D:
    """2D representation of a rubix cube

    This class allows for the representation of a cube in
    the form of 2D arrays and allows for rotation of the sides
    """

    def __init__(self) -> None:
        """Constructor for the Rubix2D class

        Returns:
            None
        """

        self.top = [["yellow"] * 3 for _ in range(3)]
        self.bottom = [["white"] * 3 for _ in range(3)]
        self.left = [["green"] * 3 for _ in range(3)]
        self.right = [["blue"] * 3 for _ in range(3)]
        self.front = [["red"] * 3 for _ in range(3)]
        self.back = [["orange"] * 3 for _ in range(3)]

    def rotate_x(self, y: int, iters: int) -> None:
        """Performs a yaw rotation on the rubix cube

        Rotates the row specified by the y coord.
        if top row is being rotated, rotate top face 90 degree anticlockwise.
        if bottom row is being rotated, rotate bottom face 90 degree clockwise.

        Args:
            y (int): the row that will be rotated
            iters (int): the amount of times the row will be rotated

        Returns:
            None
        """

        for _ in range(iters):
            self.front[y], self.right[y], self.back[y], self.left[y] = (
                self.left[y],
                self.front[y],
                self.right[y],
                self.back[y],
            )

        self.top = rotate_arr(self.top, 3 * iters) if y == 0 else self.top
        self.bottom = rotate_arr(self.bottom, 1 * iters) if y == 2 else self.bottom

    def rotate_y(self, x: int, iters: int) -> None:
        """Performs a pitch rotation on the rubix cube

        Rotates the column specified by the x coord.
        if left column is being rotated, rotate left face 90 degree clockwise.
        if right column is being rotated, rotate right face 90 degree anticlockwise.


        Args:
            y (int): the column that will be rotated
            iters (int): the amount of times the column will be rotated

        Returns:
            None
        """

        for _ in range(iters):
            front = copy.deepcopy(self.front)
            top = copy.deepcopy(self.top)
            back = copy.deepcopy(self.back)
            bottom = copy.deepcopy(self.bottom)

            inv_x = INVERSE[x]

            for index in range(3):
                self.front[index][x] = top[index][x]
                self.bottom[index][x] = front[index][x]

            for index_1, index_2 in zip((0, 1, 2), (2, 1, 0)):
                self.top[index_1][x] = back[index_2][inv_x]
                self.back[index_1][inv_x] = bottom[index_2][x]

        self.left = rotate_arr(self.left, 1 * iters) if x == 0 else self.left
        self.right = rotate_arr(self.right, 3 * iters) if x == 2 else self.right

    def rotate_z(self, z: int, iters: int) -> None:
        """Performs a roll rotation on the rubix cube

        rotates the column specified by the z coord
        if back column is being rotated, rotate back face 90 degree anticlockwise.
        if front column is being rotated, rotate front face 90 degree clockwise.

        Args:
            y (int): the column that will be rotated
            iters (int): the amount of times the column will be rotated

        Returns:
            None
        """

        for _ in range(iters):
            left = copy.deepcopy(self.left)
            top = copy.deepcopy(self.top)
            right = copy.deepcopy(self.right)
            bottom = copy.deepcopy(self.bottom)

            inv_z = INVERSE[z]

            for index_1, index_2 in zip((0, 1, 2), (2, 1, 0)):
                self.top[z][index_1] = left[index_2][z]
                self.bottom[inv_z][index_1] = right[index_2][inv_z]

            for index in range(3):
                self.right[index][inv_z] = top[z][index]
                self.left[index][z] = bottom[inv_z][index]

        self.back = rotate_arr(self.back, 3 * iters) if z == 0 else self.back
        self.front = rotate_arr(self.front, 1 * iters) if z == 2 else self.front

    def is_solved(self) -> bool:
        """Returns if the cube is solved

        Returns:
            bool: if the cube is solved
        """

        return all(
            len(set(colour for row in side for colour in row)) == 1
            for side in [
                self.top,
                self.bottom,
                self.left,
                self.right,
                self.front,
                self.back,
            ]
        )


def rotate_side(index: int, rubix: Rubix2D) -> None:
    """Rotates the side of the rubix cube specified by index

    Args:
        index (int): the rotation that will be performed 1-18
        rubix (Rubix2D): the cube on which the rotation will be
            performed on

    Returns:
        None
    """

    match index:
        case 1:
            rubix.rotate_x(2, 1)
        case 2:
            rubix.rotate_x(1, 1)
        case 3:
            rubix.rotate_x(0, 1)
        case 4:
            rubix.rotate_y(0, 1)
        case 5:
            rubix.rotate_y(1, 1)
        case 6:
            rubix.rotate_y(2, 1)
        case 7:
            rubix.rotate_z(0, 1)
        case 8:
            rubix.rotate_z(1, 1)
        case 9:
            rubix.rotate_z(2, 1)
        case 10:
            rubix.rotate_x(2, 3)
        case 11:
            rubix.rotate_x(1, 3)
        case 12:
            rubix.rotate_x(0, 3)
        case 13:
            rubix.rotate_y(0, 3)
        case 14:
            rubix.rotate_y(1, 3)
        case 15:
            rubix.rotate_y(2, 3)
        case 16:
            rubix.rotate_z(0, 3)
        case 17:
            rubix.rotate_z(1, 3)
        case 18:
            rubix.rotate_z(2, 3)


def rotate_arr(arr: List[List[Any]], iters: int) -> List[List[Any]]:
    """Rotates an array 90 clockwise [iters] times

    Rotates an array clockwise 90 degrees [iters] times.

    Args:
        arr (List[List[Any]]): the arry that will be rotated
        iters (int): the number of times the array will be rotated

    Returns:
        List[List[Any]]: the rotated array
    """
    for _ in range(iters):
        arr = list(zip(*arr[::-1]))

    arr = [list(row) for row in arr]

    return arr
