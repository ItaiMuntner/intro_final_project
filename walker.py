###########
# IMPORTS #
###########

import random
import math

#############
# CONSTANTS #
#############

NORMAL_WALKER: int = 1
UNEVEN_STEP_WALKER: int = 2
DISCRETE_WALKER: int = 3
UNEVEN_DISTRIBUTION_WALKER: int = 4
ACCEPTABLE_WALKER_TYPES: set[int] = {NORMAL_WALKER, UNEVEN_STEP_WALKER, DISCRETE_WALKER, UNEVEN_DISTRIBUTION_WALKER}


class Walker:
    """
        A class to represent a random walker in a 2D plane.

        Attributes
        ----------
        __x : float
            x-coordinate of the walker's current position.
        __y : float
            y-coordinate of the walker's current position.
        __steps : int
            Number of steps taken by the walker.
        __path : list[tuple[float, float]]
            List of positions visited by the walker.
        __weights : tuple[int, int, int, int, int]
            Weights for the directions of the walker (for UNEVEN_DISTRIBUTION_WALKER type).
        __walker_type : int
            Type of the walker.
    """

    def __init__(self, walker_type: int = NORMAL_WALKER,
                 weights: tuple[int, int, int, int, int] = (1, 1, 1, 1, 1)) -> None:
        self.__x = 0
        self.__y = 0
        self.__steps = 0
        self.__path = [(0, 0)]
        self.__weights = weights
        if walker_type not in ACCEPTABLE_WALKER_TYPES:
            raise ValueError("Invalid walker type.")
        else:
            self.__walker_type = walker_type

    def __str__(self) -> str:
        """
        :return: A string representation of the walker.
        """
        return f"Walker at position ({self.__x}, {self.__y}) after {self.__steps} steps."

    def get_next_move(self) -> tuple[float, float]:
        """
        :return: The next move of the walker.
        """
        if self.__walker_type == NORMAL_WALKER:
            angle = random.uniform(0, 2*math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)
        elif self.__walker_type == UNEVEN_STEP_WALKER:
            angle = random.uniform(0, 2*math.pi)
            step = random.uniform(0.5, 1.5)
            dx = step * math.cos(angle)
            dy = step * math.sin(angle)
        elif self.__walker_type == DISCRETE_WALKER:
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            dx, dy = direction
        elif self.__walker_type == UNEVEN_DISTRIBUTION_WALKER:
            direction = random.choices([(0, 1), (0, -1), (1, 0), (-1, 0), (-self.__x, -self.__y)],
                                       weights=self.__weights, k=1)[0]
            dx, dy = direction
        else:
            raise ValueError("Invalid walker type.")
        return dx, dy

    def move(self, dx: float, dy: float) -> None:
        """
        Moves the walker one step.
        :return: None.
        """
        self.__x += dx
        self.__y += dy
        self.__steps += 1
        self.__path.append((self.__x, self.__y))

    def get_position(self) -> tuple[float, float]:
        """
        :return: The current position of the walker.
        """
        return self.__x, self.__y

    def set_position(self, x: float, y: float) -> None:
        """
        Sets the position of the walker.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        :return: None.
        """
        self.__x = x
        self.__y = y

    def get_distance(self) -> float:
        """
        :return: The Euclidean distance from the walker to the origin.
        """
        return math.sqrt(abs(self.__x)**2 + abs(self.__y)**2)

    def get_walker_type(self) -> int:
        """
        :return: The type of the walker.
        """
        return self.__walker_type

    def reset_position(self) -> None:
        """
        Resets the walker's position to the origin.
        :return: None.
        """
        self.__x = 0
        self.__y = 0
        self.__steps = 0
        self.__path = [(0, 0)]

    def get_steps(self) -> int:
        """
        :return: The number of steps taken by the walker.
        """
        return self.__steps

    def get_path(self) -> list[tuple[float, float]]:
        """
        :return: The path taken by the walker.
        """
        return self.__path

    def set_walker_type(self, walker_type: int) -> None:
        """
        Sets the type of the walker.
        :param walker_type: The type of the walker.
        :return: None.
        """
        if walker_type not in ACCEPTABLE_WALKER_TYPES:
            raise ValueError("Invalid walker type.")
        else:
            self.__walker_type = walker_type
