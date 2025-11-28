from pi5neo import Pi5Neo
import time
import argparse 


neo = Pi5Neo('dev/spidev0.0', 10, 800)
parser = argparse.ArgumentParser(description="LED loading bar")
parser.add_argument("--color", "-c")



def loading_bar(neo, color):

    color = color.lower()
    if color == "red":
        for i in range(neo.num_leds):
            neo.set_led_color(i, 255, 0, 0)
            neo.update_strip()
            time.sleep(0.1)
    elif color == "blue":
        for i in range(neo.num_leds):
            neo.set_led_color(i, 0, 0, 255)
            neo.update_strip()
            time.sleep(0.1)
    elif color == "green":
        for i in range(neo.num_leds):
            neo.set_led_color(i, 0, 255, 0)
            neo.update_strip()
            time.sleep(0.1)
    elif color == "white":
        for i in range(neo.num_leds):
            neo.set_led_color(i, 255, 255, 255)
            neo.update_strip()
            time.sleep(0.1)
    else:
        raise ValueError("Unsupported color. Please choose from red, blue, green, or white.")


    neo.clear_strip()
    neo.update_strip()


args = parser.parse_args()
loading_bar(neo, args.color)