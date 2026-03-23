import os
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from API.api_interface import PredictRequest, PredictResponse
from API.predict import predict_weight

load_dotenv()
app = FastAPI()

MODEL_ARTIFACT_NAME = os.getenv("MODEL_ARTIFACT_NAME")
API_TOKEN = os.getenv("PREDICTION_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("PREDICTION_API_TOKEN não configurado!")

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest, authorization: str = Header(None)):
    """
    Endpoint para estimativa de peso de gado.

    Retorna:
    - peso_estimado_kg: valor contínuo previsto pelo modelo
    - versao_modelo: identificação da versão do modelo
    """

    if authorization != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not MODEL_ARTIFACT_NAME:
        raise HTTPException(status_code=500, detail="Modelo não configurado")

    # Executa inferência
    result = predict_weight(MODEL_ARTIFACT_NAME, dict(data))

    peso_estimado = round(float(np.float64(result["peso_estimado_kg"])), 2)
    versao_modelo = result["versao_modelo"]

    return PredictResponse(
        peso_estimado_kg=peso_estimado,
        versao_modelo=versao_modelo
    )