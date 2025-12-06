# WS2812B LED Strip Controller for Raspberry Pi 5

A Python project for controlling WS2812B addressable LED strips using a Raspberry Pi 5. Features a clean object-oriented design with multiple party-ready animations.

## Features

- **Object-oriented design** with `RGB`, `Colors`, and `LedStrip` classes
- **10 built-in animations** for parties and ambient lighting
- **CLI interface** for easy control
- **Hex color support** for custom static colors
- **Pomodoro timer** with visual countdown

---

## Hardware Requirements

| Component | Specification |
|-----------|---------------|
| **LED Strip** | WS2812B (5V addressable RGB) |
| **Controller** | Raspberry Pi 5 |
| **Power Supply** | 5V 6A DC adapter (supports up to 300 LEDs at full brightness) |
| **Wiring** | Jumper wires for connections |

### Power Considerations

Each WS2812B LED can draw up to **60mA at full white brightness**. For a 300 LED strip:

```
300 LEDs × 60mA = 18A (theoretical max)
```

In practice, animations rarely hit full white on all LEDs simultaneously. A **5V 6A power supply** works well for typical usage patterns with 300 LEDs.

> ⚠️ **Never power more than 8-10 LEDs from the Raspberry Pi's 5V GPIO pin.** Always use an external power supply for larger strips.

---

## Hardware Setup

### Wiring Diagram

<!-- TODO: Add wiring diagram image here -->

### Pin Connections

This project uses **SPI** (via the Pi5Neo library), so the data pin is different from traditional PWM-based setups:

| LED Strip | Raspberry Pi 5 | Notes |
|-----------|----------------|-------|
| **DIN** (Data In) | GPIO10 (Pin 19) | SPI MOSI pin |
| **GND** | GND (Pin 6) | Common ground |
| **5V** | External PSU (+) | Do not use Pi's 5V for >10 LEDs |

```
External 5V PSU
      │
      ├──────► LED Strip 5V (+)
      │
      └──────► PSU GND ◄────┐
                            │
Raspberry Pi 5              │
      │                     │
      ├── GPIO10 (Pin 19) ──► LED Strip DIN
      │
      └── GND (Pin 6) ──────┘ (Common Ground)
```

> **Critical:** Always connect all grounds together (Pi GND + LED Strip GND + Power Supply GND). Without a common ground, the data signal won't work.

### Raspberry Pi 5 GPIO Reference

```
   3.3V  (1) (2)  5V
  GPIO2  (3) (4)  5V
  GPIO3  (5) (6)  GND     ◄── Connect LED GND here
  GPIO4  (7) (8)  GPIO14
    GND  (9) (10) GPIO15
 GPIO17 (11) (12) GPIO18
 GPIO27 (13) (14) GND
 GPIO22 (15) (16) GPIO23
   3.3V (17) (18) GPIO24
 GPIO10 (19) (20) GND      ◄── Connect LED DIN to Pin 19 (GPIO10/MOSI)
  GPIO9 (21) (22) GPIO25
 GPIO11 (23) (24) GPIO8
    GND (25) (26) GPIO7
```

---

## Installation

### 1. Enable SPI on your Raspberry Pi

```bash
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable
```

Verify SPI is enabled:

```bash
ls /dev/spidev*
# Should show: /dev/spidev0.0 and /dev/spidev0.1
```

### 2. Clone the repository

```bash
git clone https://github.com/ruyca/ws2812b-manager.git
cd ws2812b-rpi5-controller
```

### 3. Install dependencies

```bash
pip install pi5neo
```

### 4. Increase SPI buffer size (required for >170 LEDs)

The default `spidev` buffer of 4096 bytes only accommodates ~170 LEDs. For 300 LEDs, you need to increase the buffer.

**Calculate the required buffer size:**

```
Buffer size = Number of LEDs × 24 bytes
300 LEDs × 24 = 7,200 bytes (minimum)
```

**Recommended: Set to 32KB for headroom**

Edit the boot configuration:

```bash
sudo nano /boot/firmware/cmdline.txt
```

Add `spidev.bufsiz=32768` to the **end** of the existing single line (separated by a space):

```
console=serial0,115200 console=tty1 root=PARTUUID=xxxx ... spidev.bufsiz=32768
```

> ⚠️ **Important:** Do not create a new line. Everything must stay on one line.

Save and reboot:

```bash
sudo reboot
```

**Verify the change:**

```bash
cat /sys/module/spidev/parameters/bufsiz
# Should output: 32768
```

---

## Usage

### Display a Static Color

```bash
python main.py --color '#ff0000'      # Red
python main.py --color 'ff6600'       # Orange (# is optional)
python main.py -c '#00ff00'           # Green (short flag)
```

### Run an Animation

```bash
python main.py --animation firework
python main.py -a breathing
python main.py -a all                 # Run all animations in sequence
```

### Specify Number of LEDs

```bash
python main.py -n 150 -a sparkle      # Use 150 LEDs instead of default 300
```

### Full Help

```bash
python main.py --help
```

---

## Available Animations

| Animation | Description |
|-----------|-------------|
| `random` | Randomly sets RGB colors across the strip |
| `loading` | Sequential loading bar effect |
| `flashing` | Full strip flashes random colors |
| `firework` | Expanding burst effect from random center points |
| `breathing` | Smooth fade in/out pulsing effect |
| `sparkle` | Twinkling white sparkles on a dim blue base |
| `gradient` | Smooth color gradient that shifts along the strip |
| `moving` | Colored segments that rotate along the strip |
| `pomodoro` | 25-minute timer with visual LED countdown |
| `all` | Runs through all animations in sequence |

---

## Project Structure

```
ws2812b-rpi5-controller/
├── main.py          # CLI entry point and animation dispatcher
├── classes.py       # RGB, Colors, and LedStrip class definitions
└── README.md        # This file
```

### Class Overview

**`RGB`** - Represents an RGB color value
- Supports creation from hex strings: `RGB.from_hex('#ff6600')`
- Includes `dim_color(factor)` for brightness control
- Immutable design prevents accidental color mutations

**`Colors`** - Preset color constants
- `Colors.RED`, `Colors.GREEN`, `Colors.BLUE`, `Colors.WHITE`
- `Colors.WARM_LIGHT`, `Colors.PINK`, `Colors.PURPLE`, `Colors.CYAN`
- `Colors.OFF` for turning LEDs off

**`LedStrip`** - Main controller class
- Wraps the Pi5Neo library with a cleaner interface
- Tracks internal state of all LEDs
- Contains all animation methods

---

## Customization

### Adding New Animations

Add a new method to the `LedStrip` class in `classes.py`:

```python
def my_custom_animation(self, color: RGB = Colors.RED, delay: float = 0.1):
    try:
        while True:
            # Your animation logic here
            self.set_led(index, color)
            self.update()
            time.sleep(delay)
    except KeyboardInterrupt:
        self.clear()
```

Then register it in `main.py`:

```python
elif animation_type == 'mycustom':
    strip.my_custom_animation()
```

And add it to the `choices` list in the argument parser.

### Using as a Library

```python
from classes import LedStrip, Colors, RGB

# Initialize strip
strip = LedStrip(num_leds=300, frequency=800, spi_device='/dev/spidev0.0')

# Set individual LEDs
strip.set_led(0, Colors.RED)
strip.set_led(1, RGB.from_hex('#ff6600'))
strip.update()

# Fill entire strip
strip.fill(Colors.WARM_LIGHT)
strip.update()

# Run an animation
strip.breathing_animation(color=Colors.BLUE)

# Clean up
strip.clear()
```

---

## Troubleshooting

### LEDs not lighting up

1. **Check wiring:** Ensure DIN is connected to GPIO10 (Pin 19), not GPIO18
2. **Verify SPI is enabled:** `ls /dev/spidev*` should show devices
3. **Check common ground:** All grounds must be connected together
4. **Power supply:** Ensure adequate amperage for your LED count

### Only first ~170 LEDs work

Increase the SPI buffer size. See the [installation section](#4-increase-spi-buffer-size-required-for-170-leds).

### "Permission denied" errors

The SPI device may require elevated permissions:

```bash
sudo python main.py -a firework
```

Or add your user to the `spi` group:

```bash
sudo usermod -a -G spi $USER
# Log out and back in for changes to take effect
```

### Flickering or wrong colors

- Try a shorter data wire between the Pi and the first LED
- Add a 470Ω resistor on the data line for signal protection
- Ensure your power supply provides stable 5V

---

## Why Pi5Neo Instead of rpi_ws281x?

The traditional `rpi_ws281x` library uses PWM/DMA and had compatibility issues with the Raspberry Pi 5's new RP1 chipset. While there is now beta support available, **Pi5Neo** offers a simpler SPI-based approach that works reliably without kernel module setup.

The tradeoff is that you must use **GPIO10 (MOSI)** instead of GPIO18 for the data line.

---

## License

MIT License - feel free to use and modify for your own projects.

---

## Acknowledgments

- [Pi5Neo](https://github.com/WS2812B/Pi5Neo) library for Raspberry Pi 5 SPI support
- Built as a learning project for Python class design and hardware integration
