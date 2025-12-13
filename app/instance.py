# Instance declaration 
from app.devices.led_strip.classes import RGB, Colors, LedStrip


strip = LedStrip(num_leds = 300, frequency=800, spi_device='/dev/spidev0.0')
