"""
generators.py
Perlin Noise 2D Generation
Written by AF & KP
"""

import math
from typing import Callable, Any, Optional
from abc import ABC, abstractmethod
from maths import dotGradient

class NoiseGenerator(ABC):
    def __init__(self, gradients: list[list[tuple[float, float]]],  **settings: Any):
        self.gradients = gradients
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
        super(PerlinNoiseGenerator, self).__init__(gradients, **settings)
        self.interpolate = interpolator
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
    
class SimplexNoiseGenerator(NoiseGenerator):
    def __init__(self, gradients: list[list[tuple[float, float]]], **settings: Any):
        super(SimplexNoiseGenerator, self).__init__(gradients, **settings)
        if "rsq" not in self.settings or "scale" not in self.settings:
            self.settings["rsq"] = 0.5
            self.settings["scale"] = 70

    def __call__(self, pt: tuple[float, float]) -> float:
        F = 0.3660254037844386 # (math.sqrt(3)-1)/2
        G = 0.21132486540518708 # (1-1/math.sqrt(3))/2
        skew = (pt[0]+pt[1])*F
        skewpt = (math.floor(pt[0]+skew), math.floor(pt[1]+skew))
        
        deskew = (skewpt[0]+skewpt[1])*G
        unskewpt = (skewpt[0]-deskew, skewpt[1]-deskew)
        
        dist = (pt[0]-unskewpt[0], pt[1]-unskewpt[1])

        order = [(0, 0), (1, 0) if dist[0] > dist[1] else (0, 1), (1,1)]

        middlept = (dist[0]-order[1][0]+G, dist[1]-order[1][1]+G)
        lastpt = (dist[0]-1+2*G, dist[1]-1+2*G)

        vertices = (dist, middlept, lastpt)
        ns = []
        for i in range(3):
            t = self.settings["rsq"] - vertices[i][0]**2 - vertices[i][1]**2
            gradient = self.gradients[skewpt[1]+order[i][1]][skewpt[0]+order[i][0]]
            ns.append(0 if t < 0 else t**4*(gradient[0]*vertices[i][0]+gradient[1]*vertices[i][1]))
        return self.settings["scale"]*sum(ns)
    
class OctaveSimplexNoiseGenerator(SimplexNoiseGenerator):
    def __init__(self, gradients: list[list[tuple[float, float]]], **settings: Any):
        super(OctaveSimplexNoiseGenerator, self).__init__(gradients, **settings)
    
    def __call__(self, pt: tuple[float, float]) -> float:
        total: float = 0
        freq: float = 1
        amp: float = 1
        maxVal: float = 0

        for _ in range(self.settings["octaves"]):
            total += super(OctaveSimplexNoiseGenerator, self).__call__((pt[0] * freq, pt[1] * freq)) * amp
            maxVal += amp

            amp *= self.settings["persistence"]
            freq *= self.settings["lacunarity"]

        return total/maxVal