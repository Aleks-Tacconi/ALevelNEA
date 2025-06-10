# -*- coding: utf-8 -*-
"""
rubix_solver module

This module Provides means of solving a Rubix2D object

Functions:
    breath_first_search: Uses a breath first search to solve the rubix cube
"""

import copy

from queue import deque
from typing import List

from rubix_cube.rubix_2d import Rubix2D
from rubix_cube.rubix_2d import rotate_side


def breath_first_search(
    top: List[List[str]],
    front: List[List[str]],
    left: List[List[str]],
    right: List[List[str]],
    back: List[List[str]],
    bottom: List[List[str]],
) -> List[int]:
    """Uses a breath first search to solve the rubix cube

    This function will run until it eventually finds the solution to
    the given rubix cube. it does through a breath-first-search which
    is a shortest path graph traversal algorithm

    Args:
        top (List[List[str]]): the top face of the rubix cube
        front (List[List[str]]): the front face of the rubix cube
        left (List[List[str]]): the left face of the rubix cube
        right (List[List[str]]): the right face of the rubix cube
        back (List[List[str]]): the back face of the rubix cube
        bottom (List[List[str]]): the bottom face of the rubix cube

    Returns:
        List[int]: A list of steps where every int represents a
            rotation that should be applied to solve the cube

    """

    rubix = Rubix2D()

    rubix.top = copy.deepcopy(top)
    rubix.front = copy.deepcopy(front)
    rubix.left = copy.deepcopy(left)
    rubix.right = copy.deepcopy(right)
    rubix.back = copy.deepcopy(back)
    rubix.bottom = copy.deepcopy(bottom)

    if rubix.is_solved():
        return []

    queue = deque([([], rubix)])

    while True:
        steps, rubix = queue.popleft()

        for move in range(1, 19):
            new_steps = steps + [move]
            new_rubix = copy.deepcopy(rubix)

            rotate_side(move, new_rubix)

            if new_rubix.is_solved():
                return new_steps

            queue.append((new_steps, new_rubix))
