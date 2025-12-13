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
