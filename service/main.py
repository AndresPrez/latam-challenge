from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="Prez API", debug=False, version="1.0.0")
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