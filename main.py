from pi5neo import Pi5Neo
import time
import argparse 
import random 
from classes import Colors, RGB, LedStrip

def show_all_animations(strip: LedStrip):
    strip.random_rgb_animation(leds_per_frame=3, delay=0.2)
    strip.loading_animation()
    strip.flashing_animation()
    strip.firework_simulation()
    strip.breathing_animation(color=Colors.BLUE)
    strip.sparkle_animation()
    strip.gradient_shift()

def run():
    strip = LedStrip(num_leds = 10, frequency=800, spi_device='/dev/spidev0.0')
    print(f"Initialized LED strip with {strip.num_leds} LEDs.")
    #show_all_animations(strip)    
    #strip.pomodoro_animation(pomodoro_length=5)
    strip.gradient_shift(Colors.PURPLE, Colors.BLUE, delay=0.3)
    print(strip.state)

if __name__ == "__main__":
    run()
