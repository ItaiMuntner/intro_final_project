###########
# IMPORTS #
###########

from typing import Union, Tuple
from walker import Walker
from shapely.geometry import LineString, Point


class Obstacle:
    """
    A class to represent an obstacle on the plane.

    Attributes
    ----------
    __start : tuple[float, float]
        The start point of the obstacle.
    __end : tuple[float, float]
        The end point of the obstacle.
    """

    def __init__(self, start: tuple[float, float], end: tuple[float, float]) -> None:
        self.__start = start
        self.__end = end

    def get_start(self) -> tuple[float, float]:
        """
        :return: The start point of the obstacle.
        """
        return self.__start

    def get_end(self) -> tuple[float, float]:
        """
        :return: The end point of the obstacle.
        """
        return self.__end

    def set_start(self, start: tuple[float, float]) -> None:
        """
        Sets the start point of the obstacle.
        :param start: The start point to set.
        """
        self.__start = start

    def set_end(self, end: tuple[float, float]) -> None:
        """
        Sets the end point of the obstacle.
        :param end: The end point to set.
        """
        self.__end = end


class Portal:
    """
    A class to represent a portal on the plane.

    Attributes
    ----------
    __start : tuple[float, float]
        The start point of the portal.
    __end : tuple[float, float]
        The end point of the portal.
    __destination : tuple[float, float]
        The destination of the portal.
    """

    def __init__(self, start: tuple[float, float], end: tuple[float, float], destination: tuple[float, float]) -> None:
        self.__start = start
        self.__end = end
        self.__destination = destination

    def get_destination(self) -> tuple[float, float]:
        """
        :return: The destination of the portal.
        """
        return self.__destination

    def set_destination(self, destination: tuple[float, float]) -> None:
        """
        Sets the destination of the portal.
        :param destination: The destination to set.
        """
        self.__destination = destination

    def get_start(self) -> tuple[float, float]:
        """
        :return: The start point of the portal.
        """
        return self.__start

    def get_end(self) -> tuple[float, float]:
        """
        :return: The end point of the portal.
        """
        return self.__end

    def set_start(self, start: tuple[float, float]) -> None:
        """
        Sets the start point of the portal.
        :param start: The start point to set.
        """
        self.__start = start

    def set_end(self, end: tuple[float, float]) -> None:
        """
        Sets the end point of the portal.
        :param end: The end point to set.
        """
        self.__end = end


class Plane:
    """
    A class to represent an infinite 2D plane.

    Attributes
    ----------
    __walkers : list[Walker]
        The walkers on the plane.
    __obstacles : list[Obstacle]
        The obstacles on the plane.
    __portals : list[Portal]
        The portals on the plane.
    """

    def __init__(self) -> None:
        self.__walkers = []
        self.__obstacles = []
        self.__portals = []

    def add_walker(self, walker: Walker) -> None:
        """
        Adds a walker to the plane.
        :param walker: The walker to add.
        """
        self.__walkers.append(walker)

    def add_obstacle(self, obstacle: Obstacle) -> None:
        """
        Adds an obstacle to the plane.
        :param obstacle: The obstacle to add.
        """
        self.__obstacles.append(obstacle)

    def add_portal(self, portal: Portal) -> None:
        """
        Adds a portal to the plane.
        :param portal: The portal to add.
        """
        self.__portals.append(portal)

    def check_intersection(self, current_position: Tuple[float, float], next_position: Tuple[float, float]) ->\
            Union[Tuple[float, float], Tuple[str, Union[Obstacle, Portal]]]:
        """
        Checks if the path from the current position to the next position intersects with any obstacle or portal.

        Parameters
        ----------
        current_position : Tuple[float, float]
            The current position of the walker.
        next_position : Tuple[float, float]
            The next position of the walker.

        Returns
        -------
        Union[Tuple[float, float], Tuple[str, Union[Obstacle, Portal]]]
            If there is no intersection, it returns the next position.
            If there is an intersection, it returns a tuple where the first element is a string indicating the type of
             the intersected object ('obstacle' or 'portal'),
            and the second element is the intersected object itself (an instance of Obstacle or Portal).
        """
        # Create LineString for the path
        path = LineString([Point(*current_position), Point(*next_position)])

        # Initialize minimum distance to a large number and intersected object to None
        min_distance = float('inf')
        intersected_object = None
        intersected_type = None

        # Check intersection with obstacles
        for obstacle in self.__obstacles:
            obstacle_line = LineString([Point(*obstacle.get_start()), Point(*obstacle.get_end())])
            intersection = path.intersection(obstacle_line)
            if not intersection.is_empty:
                # Convert intersection to a Point object
                intersection = Point(intersection.x, intersection.y)
                distance = Point(*current_position).distance(intersection)
                if distance < min_distance:
                    min_distance = distance
                    intersected_object = obstacle
                    intersected_type = 'obstacle'

        # Check intersection with portals
        for portal in self.__portals:
            portal_line = LineString([Point(*portal.get_start()), Point(*portal.get_end())])
            intersection = path.intersection(portal_line)
            if not intersection.is_empty:
                # Convert intersection to a Point object
                intersection = Point(intersection.x, intersection.y)
                distance = Point(*current_position).distance(intersection)
                if distance < min_distance:
                    min_distance = distance
                    intersected_object = portal
                    intersected_type = 'portal'

        # If no intersection with any obstacle or portal
        if intersected_object is None:
            return next_position
        else:
            return intersected_type, intersected_object

    def get_walkers(self) -> list[Walker]:
        """
        :return: The walkers on the plane.
        """
        return self.__walkers

    def get_obstacles(self) -> list[Obstacle]:
        """
        :return: The obstacles on the plane.
        """
        return self.__obstacles

    def get_portals(self) -> list[Portal]:
        """
        :return: The portals on the plane.
        """
        return self.__portals

    def remove_walker(self, walker: Walker) -> None:
        """
        Removes a walker from the plane.
        :param walker: The walker to remove.
        """
        try:
            self.__walkers.remove(walker)
        except ValueError:
            pass
