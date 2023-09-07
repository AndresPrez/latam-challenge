from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from .interfaces.flight import Flight

app = FastAPI(title="LATAM Challenge", debug=False, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/status", description="Service status", tags=["status"])
async def status():
    return f'Service is operational at: {datetime.now()}', 


@app.post(path="/predict", description="Predict flight delay", tags=["predict"])
async def predict(flight: Flight):
    return flight
