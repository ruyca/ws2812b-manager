from pi5neo import Pi5Neo
import time
import argparse 
import random 
from classes import Colors, RGB


neo = Pi5Neo('dev/spidev0.0', 10, 800)
parser = argparse.ArgumentParser(description="LED loading bar")
parser.add_argument("--color", "-c", default="blue")


def loading_bar(neo, color):
    """Display a loading bar"""
    r, g, b = get_rgb_value(color)
    for i in range(neo.num_leds):
        neo.set_led_color(i, r, g, b)
        neo.update_strip()
        time.sleep(0.1)
    

def random_rgb(neo):
    """Displays random rgb colors across the strip"""
    # Get 3 random colors
    # Change 3 random led within the range 
    
    while True: 
        r_int = random.randint(0, 9)
        r, g, b = get_random_color()
        neo.set_led_color(r_int, r, g, b)
        neo.update_strip()
        time.sleep(0.2)


def run():
    day_light = Colors.WARM_LIGHT
    print(day_light)
    neo.fill_strip(day_light.red, day_light.green, day_light.blue)
    #neo.clear_strip()
    neo.update_strip()

if __name__ == "__main__":
    run()
