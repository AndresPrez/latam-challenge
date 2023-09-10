import pandas as pd
import numpy as np
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from interfaces import Flight, FIELD_MAP

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
    return f'Service is operational at: {datetime.now()}.', 


@app.post(path="/predict", description="Predict flight delay", tags=["predict"])
async def predict(flight: Flight):

    # The 'latam' package is locally available as a Lambda Layer
    # not as an install python package. So we need to import it
    # after the lambda handler runs.
    from latam.model import Model
    from latam.dataset import Dataset

    parsed_flight = {
        (FIELD_MAP[key] if key in FIELD_MAP else key): value for key, value in flight
    }
    flight_df = pd.DataFrame([parsed_flight])
    ds = Dataset(dataset=flight_df)
    ds.clean()
    ds.encode()
    X, _ = ds.split_target()
    model = Model()
    model.load()
    prediction = Model.predict(model.model, X)
    toReturn = {
        "Atraso menor": True if prediction[0] > 0.5 else False,
        "Probabilidad atraso menor (%)": np.round(prediction[0]* 100, 2),
    }
    return toReturn
