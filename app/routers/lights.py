from pydantic import BaseModel 
from app.devices.led_strip.classes import Colors, RGB
from fastapi import APIRouter
from app.instance import strip

router = APIRouter()

class ColorRequest(BaseModel):
    color: str

@router.post("/on")
def on():
    red = Colors.RED
    strip.fill(red)
    strip.update()

    return {"status": "on"}  

@router.post("/off")
def off():
    strip.clear()

    return {"status":"off"}


@router.post("/color") 
def set_color(request: ColorRequest):
    color = request.color # FF5500 / #FF5500
    color_instance = RGB.from_hex(color)
    strip.fill(color_instance)
    strip.update()

    return {"new_color": color}

@router.get("/led/debug")
def led_state():
    power = "on" if strip.power_status() else "off"
    num_leds = strip.num_leds
    uniform_color = strip.uniform_color() # (RGB,HEX)
    if not uniform_color: 
        rgb_color = "Not uniform color or animation displaying"
        hex_color = "Not uniform color or animation displaying"
    else:
        rgb_color,hex_color = uniform_color

    state_list = [led.to_dict() for led in strip.state]
    
    response = {
        "power": power,
        "num_leds": num_leds,
        "Current color": {"RGB":rgb_color, "hex":hex_color},
        "state": state_list
    }

    return response 