"""
main.py
Perlin Noise 2D Generation
Written by AF & KP
"""

import math
import random
from generators import PerlinNoiseGenerator, OctavePerlinNoiseGenerator
from colouring import colourHeightMapImage, terrainColours
def generateGradients(width: int, height: int) -> list[list[tuple[float, float]]]:
    """
    Generates a random grid of gradients for use in noise generation.

        Parameters:
            width (int): the width of the gradient grid (should be one larger than the width of the cell grid).
            height (int): the height of the gradient grid (should be one larger than the width of the desired cell grid).

        Returns:
            list[list[tuple[float, float]]]: the generated grid of gradients
    """
    gradients: list[list[tuple[float, float]]] = []
    for y in range(height):
        gradients.append([])
        for _ in range(width): 
            # generate theta in [0, 2pi)
            theta = random.random() * 2 * math.pi
            # this is normalised by nature, x = rcos(theta), y = rsin(theta) with r = 1 
            # w/ x^2 + y^2 = r^2 -> r^2cos^2(theta) + r^2sin^2(theta) = r^2
            # -> r^2(cos^2(theta) + sin^2(theta)) = r^2 -> r^2(1) = r^2   [] -> QED -pep x)
            gradients[y].append((math.cos(theta), math.sin(theta)))
    return gradients

# main code 

def smoothstep(start: float, end: float, weight: float) -> float:
    """
    Uses smoothstep to interpolate between two floats ∈ [start, end].

        Parameters:
            start (float): start of the interpolation range.
            end (float): end of the interpolation range.
            weight (float): the weight of the interpolation in the range [0, 1].

        Returns:
            float: the interpolated value in the range [start, end].
    """
    return (end-start)*(3-weight*2)*(weight**2)+start

def scaleHeight(height: float, lower: float, upper: float) -> float:
    """
    Scales a value, height ∈ [-1, 1], to a range [lower, upper].

        Parameters:
            height (float): a value in the range [-1, 1].
            lower (float): the lower bound of the target range.
            upper (float): the upper bound of the target range.

        Returns:
            float: the scaled value in the range [lower, upper].
    """
    return (height+1)/2*(upper-lower) + lower

# terminal classical greyscale display
def greyscaleRepresentation(heights: list[list[float]]) -> None:
    for r in heights:
        for h in r:
            height = round(scaleHeight(h, 0, 255))
            print(f"\x1b[48;2;{height};{height};{height}m  \x1b[0m", end="")
        print()

# classical greyscale display in image
def greyscaleImageRepresentation(filename: str, heights: list[list[float]]) -> None:
    data = [round(scaleHeight(h, 0, 255)) for y in heights for h in y]
    
    from PIL import Image
    import os

    img = Image.new("L", (len(heights[0]), len(heights)), 0)
    img.putdata(data)
    img.save(filename)
    
    print(f'Saved: FILENAME = {filename}, SIZE = {os.path.getsize(filename)}B, WxH = {img.width}x{img.height}')

w, h, res = 5, 5, 100
perlin = PerlinNoiseGenerator(generateGradients(w, h), smoothstep)
octavePerlin = OctavePerlinNoiseGenerator(generateGradients(w*2**4, h*2**4), smoothstep, octaves=4, persistence=0.5, lacunarity=2)

perlinHeight = perlin.generateHeightMap(w, h, res)
octavePerlinHeight = octavePerlin.generateHeightMap(w, h, res)

greyscaleImageRepresentation("perlin.png", perlinHeight)
greyscaleImageRepresentation("octaves.png", octavePerlinHeight)

colourHeightMapImage("terrainPerlin.png", perlinHeight, terrainColours)
colourHeightMapImage("terrainPerlinOctave.png", octavePerlinHeight, terrainColours)