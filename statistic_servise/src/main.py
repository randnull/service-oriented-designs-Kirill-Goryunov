from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/")
async def check():
    return JSONResponse(content={"message": "Ok"}, status_code=200)
