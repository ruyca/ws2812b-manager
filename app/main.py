from fastapi import FastAPI, Request
from .routers import lights
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(lights.router)
app.mount("/static", StaticFiles(directory="static/", html=True), name="static")

@app.get("/")
async def root():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)


