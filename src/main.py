import sys
sys.path.insert(1, './src')

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import logging
from logging.config import dictConfig
from log_config import log_config 

import controllers.deforestation as deforestation

dictConfig(log_config)
logger = logging.getLogger("capstone") # should be this name unless you change it in log_config.py

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/v1/is-deforested")
def isDeforested(lat: float = None, lng: float = None):
    if not lat or not lng:
        raise HTTPException(status_code=400, detail="lat and lng are required")
    else:
        result = deforestation.isDeforested(lat, lng)
        if result == None:
            raise HTTPException(status_code=404, detail="No area found")
        else:
            return {'isDeforested': str(list)}

