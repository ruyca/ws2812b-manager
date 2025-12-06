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
            red=int(self.red * factor), 
            green=int(self.green * factor),
            blue=int(self.blue * factor)
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
    YELLOW = RGB(255, 255, 0)
    CYAN = RGB(0, 255, 255)
    RANDOM = RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255))


class LedStrip:
    def __init__(self, num_leds: int = 10, frequency: int = 800, spi_device: str = '/dev/spidev0.0'):
        self.num_leds = num_leds
        self.frequency = frequency
        self.spi_device = spi_device
        self._neo = Pi5Neo(spi_device, num_leds, frequency)
        self._state = [RGB() for _ in range(num_leds)]

    @property
    def state(self):
        state_copy = self._state.copy()
        return state_copy
    
    def set_led(self, index: int, rgb_color: RGB):
        if index < 0 or index >= self.num_leds: 
            raise IndexError("LED index out of range")
        
        self._state[index] = rgb_color
        self._neo.set_led_color(index, rgb_color.red, rgb_color.green, rgb_color.blue)

    def fill(self, color: RGB):
        for i in range(self.num_leds):
            self.set_led(i, color)

    def update(self):
        self._neo.update_strip()

    def clear(self):
        self.fill(Colors.OFF)
        self.update()

    def random_rgb_animation(self, leds_per_frame: int = 3, delay: float = 0.1):
        """Displays random red, green or blue color accross the strip"""
        n = self.num_leds
        rgb = [Colors.RED, Colors.GREEN, Colors.BLUE]
        try:
            while True: 
                colors = random.choices(rgb,k=leds_per_frame)
                indices = random.sample(range(n), leds_per_frame)
                for i in range(leds_per_frame):
                    self.set_led(indices[i], colors[i])
                self.update()
                time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def flashing_animation(self, delay: float = 0.3, duration: int = 15):
        end_time = time.time() + duration
        try:
            while time.time() < end_time:
                color = RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                self.fill(color)
                self.update()
                time.sleep(delay)
                self.clear()
                time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()
        

    def loading_animation(self, color:RGB = Colors.WARM_LIGHT, delay: float = 0.1):
        
        try:
            while True: 
                for i in range(self.num_leds):
                    self.set_led(i, color)
                    self.update()
                    time.sleep(delay)
                self.clear()
        except KeyboardInterrupt: 
            self.clear()

    def pomodoro_animation(self, pomodoro_length: int = 25, color: RGB = Colors.BLUE):
        try:
            pace = pomodoro_length / self.num_leds # Time per LED in minutes
            # Start pomodoro with all the lights on
            self.fill(color = color)
            self.update()
            # Power off lights as time passes
            dimmed_color = color.dim_color(0.2)
            for i in range(self.num_leds - 1, -1, -1):
                time.sleep(pace * 60) # Convert minutes to seconds
                print(f"Turning off LED {i}, time passed: {pomodoro_length - pace * (self.num_leds - i)} minutes")
                self.set_led(i, dimmed_color)
                self.update()
            # Pomodoro finished
            self.flashing_animation()
        except KeyboardInterrupt:
            self.clear()

    def firework_simulation(self, delay=0.05):
        try: 
            while True: 
                center = random.randint(0, self.num_leds - 1)
                color = RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                print(color)
                # Expand from center
                for radius in range(self.num_leds):
                    self.clear()
                    if center - radius >= 0:
                        self.set_led(center - radius, color)
                    if center + radius < self.num_leds:
                        self.set_led(center + radius, color)
                    self.update()
                    #time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def breathing_animation(self, color: RGB = Colors.WARM_LIGHT, steps: int = 20, delay: float = 0.05):
        try:
            high = [i / steps for i in range(1, steps + 1)] 
            low = [j / steps for j in range(steps, 0, -1)]
            bright_levels = high + low
            while True:
                for b_level in bright_levels:
                    new_color = color.dim_color(b_level)
                    self.fill(new_color)
                    self.update()
                    time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def sparkle_animation(self, base_color: RGB = None,
                          sparkle_color: RGB = Colors.WHITE, sparkle_count: int = 50,
                           delay: float = 0.1, steps: int = 5):
        if base_color is None: 
            base_color = Colors.BLUE.dim_color(0.3)

        high = [i / steps for i in range(1, steps + 1)]
        low = [j / steps for j in range(steps - 1, 0, -1)]
        bright_level = high + low
        try:
            while True:  
                self.fill(base_color)
                indices = random.sample(range(self.num_leds), k=sparkle_count)
                for b in bright_level:
                    color = sparkle_color.dim_color(b)
                    for idx in indices:
                        self.set_led(idx, color)
                    self.update()
                    time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def interpolate(self, color_start: RGB, color_end: RGB, factor: float) -> RGB:
        r_m =  int(color_start.red + (color_end.red - color_start.red)*factor)
        g_m =  int(color_start.green + (color_end.green - color_start.green)*factor)
        b_m =  int(color_start.blue + (color_end.blue - color_start.blue)*factor)
        
        return RGB(r_m, g_m, b_m)

    def gradient_shift_animation(self, color_start: RGB = Colors.RED, 
                        color_end: RGB = Colors.BLUE, delay: float = 0.05 ): 
        try: 
            step = 1 / (self.num_leds - 1) 
            steps = [i*step for i in range(0, self.num_leds)]
            gradient = [self.interpolate(color_start=color_start,color_end=color_end, factor=j) for j in steps]
            while True:
                for idx, color in enumerate(gradient): 
                    self.set_led(idx, color)
                self.update()
                # Shift list to the right
                gradient = [gradient[-1]] + gradient[:-1]
                time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def moving_colors_animation(self, colors: list[RGB] = [Colors.RED, Colors.GREEN, Colors.BLUE], 
                      delay: float = 0.2):
        try:
            color_count = len(colors)
            while True:
                for i in range(self.num_leds):
                    self.set_led(i, colors[i % color_count])
                self.update()
                # Shift colors to the right
                colors = [colors[-1]] + colors[:-1]
                time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()

    def build_state(self, colors: list[RGB]) -> list[RGB]:
        state = []
        color_count = len(colors)
        base  = self.num_leds // color_count 
        remain = self.num_leds % color_count
        for color in colors:
            state.extend([color] * base)
        for i in range(remain):
            state.append(colors[i])
        return state

    def moving_colors2_animation(self, colors: list[RGB] = [Colors.RED, Colors.GREEN, Colors.BLUE], 
                      delay: float = 0.2):
        try:
            state = self.build_state(colors)
            while True:
                for i, colro in enumerate(state):
                    self.set_led(i, state[i])
                self.update()
                # Shift colors to the left
                state = state[1:] + [state[0]]
                time.sleep(delay)
        except KeyboardInterrupt:
            self.clear()
 
print(type(Colors.RED))
led_strip = LedStrip()
print(led_strip.num_leds)