"""
generators.py
Perlin Noise 2D Generation
Written by AF & KP
"""

import math
from typing import Callable, Any
from abc import ABC, abstractmethod

def dotGradient(candidate: tuple[int, int], pt: tuple[float, float], gradients: list[list[tuple[float, float]]]) -> float:
    # offset vector
    diff = (pt[0]-candidate[0], pt[1]-candidate[1])
    # use candidate to grab gradient
    gradient = gradients[candidate[1]][candidate[0]]
    return diff[0]*gradient[0] + diff[1]*gradient[1]

class NoiseGenerator(ABC):
    def __init__(self, gradients: list[list[tuple[float, float]]], interpolator: Callable[[float, float, float], float],  **settings: Any):
        self.gradients = gradients
        self.interpolate = interpolator
        self.settings = settings
    
    @abstractmethod
    def __call__(self, pt: tuple[float, float]) -> float:
        """
        Finds the height at a point, pt.

            Parameters:
                pt (tuple[float, float]): the target co-ordinates.
            Returns:
                float: the height at the point, pt. 
        """
        pass
    
    def generateHeightMap(self, width:int, height:int, resolution: int) -> list[list[float]]:
        """
        Generates a grid of heights using the NoiseGenerator.

            Paramaters:
                resolution (int): the (square-root of the) number of samples within each cell, each cell is split into resolution x resolution subcells. 
            Returns:
                list[list[float]]: the generated grid of heights.                    
        """
        return [[self((x/resolution, y/resolution)) for x in range((width-1)*resolution)] for y in range((height-1)*resolution)]

class PerlinNoiseGenerator(NoiseGenerator):
    def __init__(self, gradients: list[list[tuple[float, float]]], interpolator: Callable[[float, float, float], float], **settings: Any):
        super(PerlinNoiseGenerator, self).__init__(gradients, interpolator, **settings)
    
    def __call__(self, pt: tuple[float, float]) -> float:
        x0, y0 = math.floor(pt[0]), math.floor(pt[1])
        x1, y1 = x0 + 1, y0 + 1

        iv0, iv1 = self.interpolate(
            dotGradient((x0, y0), pt, self.gradients),
            dotGradient((x1, y0), pt, self.gradients),
            pt[0] - x0
        ), self.interpolate(
            dotGradient((x0, y1), pt, self.gradients),
            dotGradient((x1, y1), pt, self.gradients),
            pt[0] - x0
        )
        return self.interpolate(iv0, iv1, pt[1] - y0)

class OctavePerlinNoiseGenerator(PerlinNoiseGenerator):
    def __init__(self, gradients: list[list[tuple[float, float]]], interpolator: Callable[[float, float, float], float], **settings: Any):
        super(OctavePerlinNoiseGenerator, self).__init__(gradients, interpolator, **settings)

    def __call__(self, pt: tuple[float, float]) -> float:
        total: float = 0
        freq: float = 1
        amp: float = 1
        maxVal: float = 0

        for _ in range(self.settings["octaves"]):
            total += super(OctavePerlinNoiseGenerator, self).__call__((pt[0] * freq, pt[1] * freq)) * amp
            maxVal += amp

            amp *= self.settings["persistence"]
            freq *= self.settings["lacunarity"]

        return total/maxVal