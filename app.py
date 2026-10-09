import socket
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = joblib.load("model.joblib")
SPECIE = ["setosa", "versicolor", "virginica"]


class Fiore(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(f: Fiore):
    x = [[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]]
    pred = int(model.predict(x)[0])
    return {"specie": SPECIE[pred], "servito_da": socket.gethostname()}
