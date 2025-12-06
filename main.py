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
    strip.gradient_shift_animation()
    strip.moving_colors_animation()
    strip.moving_colors2_animation()
    strip.pomodoro_animation()

def get_color(hex: str) -> RGB:
    """
    Initializes an instance of RGB Object and returns it
         
            - Blue, Red, Warm_light etc.
            - HEX: str
            - RGB: str
    """
    c = RGB.from_hex(hex)
    return c

def run_animation():
    pass

def display_color(strip: LedStrip, color: RGB) -> None:
    print(f"Displaying static color: {color}")
    try:
        while True: 
            strip.fill(color)
            strip.update()
    except KeyboardInterrupt:
        print('Stopping RGB Strip')

def run():
    parser = argparse.ArgumentParser(
        description="Controls the RGB LED Strip. Display a static color or run animations.",
        epilog="Examples:\n"
               "  python main.py --color '#ff0000'           # Red static color\n"
               "  python main.py --animation firework        # Run firework animation\n"
               "  python main.py --animation all             # Run all animations in sequence",
        formatter_class=argparse.RawDescriptionHelpFormatter  # Preserves formatting in epilog
    )

    # General LED strip configuration
    parser.add_argument('-n', '--num-leds', 
                        default=300, 
                        type=int,
                        help="Number of LEDs in the strip (default: 300)")

    # Create a mutually exclusive group for the mode of operation
    mode_group = parser.add_mutually_exclusive_group(required=True) 

    # Option 1: Static color mode
    mode_group.add_argument('-c', '--color', 
                           type=str,
                           metavar='HEX',
                           help="Display a static color (hex format, e.g., '#ff0000' or 'ff0000')")
    
    # Option 2: Animation mode
    mode_group.add_argument('-a', '--animation',
                           type=str,
                           choices=['firework', 'breathing', 'sparkle', 'gradient', 
                                    'loading', 'flashing', 'moving', 'pomodoro', 'random', 'all'],
                           metavar='TYPE',
                           help="Run an animation. Choices: firework, breathing, sparkle, "
                                "gradient, loading, flashing, moving, pomodoro, random, all")

    args = parser.parse_args()

    strip = LedStrip(num_leds = args.num_leds, frequency=800, spi_device='/dev/spidev0.0')
    print(f"Initialized LED strip with {strip.num_leds} LEDs.")

    if args.color:
        color = get_color(args.color)
        display_color(strip=strip, color=color)
    elif args.animation:
        print(f"Running animation: {args.animation}")
        run_animation(strip, args.animation)  # You'd implement this dispatch function
    
    strip.clear()
    print(f"\nClearing the strip. \nGoodbye!")

if __name__ == "__main__":
    run()
