"""
main.py
Perlin Noise 2D Generation
Written by AF & KP
"""

import math
import random
from generators import PerlinNoiseGenerator, OctavePerlinNoiseGenerator
from colouring import colourHeightMapImage, terrainColours, terrainColoursSmoothstep
from maths import scaleHeight, smoothstep

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
octavePerlin = OctavePerlinNoiseGenerator(generateGradients(w*2**2, h*2**2), smoothstep, octaves=2, persistence=0.5, lacunarity=2)

perlinHeight = perlin.generateHeightMap(w, h, res)
octavePerlinHeight = octavePerlin.generateHeightMap(w, h, res)

greyscaleImageRepresentation("img/perlin.png", perlinHeight)
greyscaleImageRepresentation("img/octaves.png", octavePerlinHeight)

colourHeightMapImage("img/terrainPerlin.png", perlinHeight, terrainColours)
colourHeightMapImage("img/terrainPerlinSmooth.png", perlinHeight, terrainColoursSmoothstep)
colourHeightMapImage("img/terrainPerlinOctave.png", octavePerlinHeight, terrainColours)
colourHeightMapImage("img/terrainPerlinOctaveSmooth.png", octavePerlinHeight, terrainColoursSmoothstep)
