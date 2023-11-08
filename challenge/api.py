from typing import List, Dict

import fastapi
import pandas as pd

from .model import DelayModel
from .schemas import PredictSchema

app = fastapi.FastAPI()

model: DelayModel


@app.on_event("startup")
async def load_model():
    global model
    model = DelayModel()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights: Dict) -> dict:
    input_schema = PredictSchema(**flights)
    input_schema.validate_schema()

    data = pd.DataFrame(flights['flights'])
    data = pd.concat([
        pd.get_dummies(data['OPERA'], prefix='OPERA'),
        pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
        pd.get_dummies(data['MES'], prefix='MES')],
        axis=1
    )
    needed_cols = set(model.train_columns).difference(set(data.columns))
    data = pd.concat([
        data,
        pd.DataFrame([[0]*len(needed_cols)], columns=needed_cols)],
        axis=1
    )
    print(data)
    return {"predict": model.predict(data[model.train_columns])}
