from pi5neo import Pi5Neo
import time
import argparse 
import random 

class RGB:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue
    
    def __repr__(self):
        return f"RGB({self.red}, {self.green}, {self.blue})"
    
    @classmethod
    def from_hex(cls, hex_string: str) -> "RGB": 
        hex_string = hex_string.lstrip("#")
        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)

        return cls(r, g, b)

    def dim_color(self, factor: float):
        if factor < 0 or factor > 1: 
            raise ValueError("Factor must be between 0 and 1")
        return RGB(
            r=int(self.red * factor), 
            g=int(self.green * factor),
            b=int(self.blue * factor)
        )


class Colors: 
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    WHITE = RGB(255, 255, 255)
    OFF = RGB(0, 0, 0)
    WARM_LIGHT = RGB(255, 220, 82)
    PINK = RGB(255, 96, 208)
    PURPLE = RGB(128, 0, 128)
    ORANGE = RGB(255, 165, 0)



print(type(Colors.RED))