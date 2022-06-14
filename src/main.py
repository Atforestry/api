import sys
import os
sys.path.insert(1, './src')

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import logging
from logging.config import dictConfig
from log_config import log_config 

import controllers.deforestation as deforestation

import requests

dictConfig(log_config)
logger = logging.getLogger("capstone") # should be this name unless you change it in log_config.py

app = FastAPI()

origins = [
    "http://www.atforestry.com",
    "http://atforestry.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="http://localhost\:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    logger.info('Healthcheck ok')
    return {'healthcheck': 'Ok'}

@app.get("/")
def main():
    content = """
<body>
<p>Hello World !</p>
</body>
    """
    return HTMLResponse(content=content)

@app.get("/model-predict")
def modelpredict():
    url = f'http://{os.environ["MODEL_PREDICT_URL"]}/healthcheck'
    print(url)
    r = requests.get(f'http://{os.environ["MODEL_PREDICT_URL"]}/healthcheck')
    return JSONResponse(content=r.status_code)

@app.get("/v1/is-deforested")
async def isDeforested(lat: float = None, lng: float = None):
    if not lat or not lng:
        raise HTTPException(status_code=400, detail="lat and lng are required")
    else:
        result = deforestation.isDeforested(lat, lng)
        if result == None:
            raise HTTPException(status_code=404, detail="No area found")
        else:
            return JSONResponse(content=result)

