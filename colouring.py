"""
colouring.py
Perlin Noise 2D Generation
Written by AF & KP
"""
from typing import Callable
from maths import lerp, smoothstep
class Colour:
    def __init__(self, r: float, g: float, b: float):
        for v in [r, g, b]:
            if not 0 <= v <= 255:
                raise ValueError("r, g, b values must lie within [0, 255]")
        self.r, self.g, self.b = r, g, b
    
    # this is sad but used to avoid typing errors that don't exist (python and mypy are delusional)
    def __call__(self, v: float):
        return self
    def prepare(self):
        return (round(self.r), round(self.g), round(self.b))
    
class ColourRange:
    def __init__(self, start: Colour, end: Colour, interpolater: Callable[[float, float, float], float]):
        self.start = start
        self.end = end
        self.interpolate = interpolater
    def __call__(self, v: float) -> Colour:
        if not 0 <= v <= 1:
            raise ValueError("value must lie within [0, 1]")
        return Colour(
            self.interpolate(self.start.r, self.end.r, v),
            self.interpolate(self.start.g, self.end.g, v),
            self.interpolate(self.start.b, self.end.b, v)
        )
    
class ColourBounds:
    def __init__(self, colours: dict[float, Colour | ColourRange]):
        self.lower = min(colours.keys())
        self.upper = max(colours.keys())
        self.colours = colours

    def at(self, v: float) -> Colour:
        if not self.lower <= v <= self.upper:
            raise ValueError(f"value(={v}) must lie within [{self.lower}, {self.upper}]") 
        for (lb, _), (ub, colour) in zip(self.colours.items(), list(self.colours.items())[1:]):
            if lb <= v <= ub:
                return colour((v-lb)/(ub-lb)) if type(colour) == ColourRange else colour(v)
        return Colour(0, 0, 0)
    
terrainColours = ColourBounds({
     -1.0: Colour(0, 0, 0),
     -0.3: ColourRange(Colour(20, 20, 20), Colour(20, 20, 130), lerp),
    -0.15: ColourRange(Colour(253, 255, 77), Colour(212, 214, 29), lerp),
     -0.1: Colour(212, 214, 29),
        0: ColourRange(Colour(212, 214, 29), Colour(184, 255, 116), lerp),
      0.3: ColourRange(Colour(184, 255, 116), Colour(16, 140, 9), lerp),
     0.45: Colour(170, 170, 170),
        1: Colour(255, 255, 255)
})
terrainColoursSmoothstep = ColourBounds({
     -1.0: Colour(0, 0, 0),
     -0.3: ColourRange(Colour(20, 20, 20), Colour(20, 20, 130), smoothstep),
    -0.15: ColourRange(Colour(253, 255, 77), Colour(212, 214, 29), smoothstep),
     -0.1: Colour(212, 214, 29),
        0: ColourRange(Colour(212, 214, 29), Colour(184, 255, 116), smoothstep),
      0.3: ColourRange(Colour(184, 255, 116), Colour(16, 140, 9), smoothstep),
     0.45: Colour(170, 170, 170),
        1: Colour(255, 255, 255)
})
def colourHeightMapImage(filename: str, heights: list[list[float]], colourBounds: ColourBounds):
    from PIL import Image
    import os
    
    image = Image.new("RGB", (len(heights[0]), len(heights)))
    image.putdata([colourBounds.at(h).prepare() for y in heights for h in y]) # type: ignore    
    image.save(filename)
    print(f'Saved: FILENAME = {filename}, SIZE = {os.path.getsize(filename)}B, WxH = {image.width}x{image.height}')
