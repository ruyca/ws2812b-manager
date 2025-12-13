from fastapi import FastAPI
from .routers import lights
import uvicorn

app = FastAPI()
app.include_router(lights.router)


@app.get("/")
async def root():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
