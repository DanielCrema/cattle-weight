from pydantic import BaseModel

# =========================
# INPUT
# =========================
class PredictRequest(BaseModel):
    raca: str
    idade_meses: int
    altura_cm: float
    comprimento_corpo_cm: float
    circunferencia_peito_cm: float
    cor_pelagem: str
    sexo: str

# =========================
# OUTPUT
# =========================
class PredictResponse(BaseModel):
    peso_estimado_kg: float
    versao_modelo: str