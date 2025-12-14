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
    
    def __eq__(self, other):
        if not isinstance(other, RGB):
            return NotImplemented
        return(
            self.red == other.red and
            self.green == other.green and
            self.blue == other.blue
        )
    
    def to_hex(self):
        r = hex(self.red)[2:].zfill(2)
        g = hex(self.green)[2:].zfill(2)
        b = hex(self.blue)[2:].zfill(2)

        return f"#{r}{g}{b}"
    
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

    def to_dict(self):
        return {"red": self.red, "green": self.green, "blue": self.blue}


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
    
    def power_status(self):
        state = self.state # [RGB(128,128,128), ...]
        led_is_on = [True if (led.red != 0 or led.green != 0 or led.blue != 0) else False for led in state]

        return any(led_is_on) 
    
    def uniform_color(self): 
        state = self.state
        first = state[0] # RGB(0,0,0)
        same_color = [first == led for led in state]
        first_rgb = first.to_dict() # RGB instnace -> dict
        first_hex = first.to_hex() # RGB instance -> str
        if all(same_color):
            return first_rgb, first_hex
        else:
            return None 

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

    def shifting_rgb_animation(self, groups: int = 12, delay: float = 0.1):
        """
        Displays shifting RGB colors accross the strip, in a grouped manner.
        Each group consists of red, green, and blue LEDs.
        Each subgroup is equal to num_leds / groups (300 / 12 = 25 LEDs per color).
        """
        n = self.num_leds
        rgb = [Colors.RED, Colors.GREEN, Colors.BLUE]
        try:
            # Build the state
            state = [Colors.OFF] * n
            for i in range(n):
                position_in_group = i % 12 # Where am I within my 12-LED super-group? (0-11)
                color_index = position_in_group // 4 # Which color block? (0, 1, or 2)
                state[i] = rgb[color_index] 
            while True: 
                for idx, color in enumerate(state): 
                    self.set_led(idx, color)
                self.update()
                # Shift list to the right
                state = [state[-1]] + state[:-1]
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
                    #time.sleep(delay)
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
                # Keep track of which indices are currently lit so we don't clear the whole strip
                prev_indices = set()
                # radius should go until edges from center
                max_radius = max(center, self.num_leds - 1 - center)
                for radius in range(max_radius + 1):
                    new_indices = set()
                    left = center - radius
                    right = center + radius
                    if 0 <= left < self.num_leds:
                        new_indices.add(left)
                    if 0 <= right < self.num_leds:
                        new_indices.add(right)

                    # Turn off LEDs that were lit previously but are not part of this step
                    to_clear = prev_indices - new_indices
                    for idx in to_clear:
                        self.set_led(idx, Colors.OFF)

                    # Light the new LEDs for this radius (skip ones already lit)
                    to_light = new_indices - prev_indices
                    for idx in to_light:
                        self.set_led(idx, color)

                    prev_indices = new_indices
                    self.update()
                    time.sleep(delay)

                # After the explosion, clear remaining lit LEDs
                for idx in prev_indices:
                    self.set_led(idx, Colors.OFF)
                self.update()
                time.sleep(delay)
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