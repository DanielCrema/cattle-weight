from typing import List, Literal
from pydantic import BaseModel

# =========================
# INPUT
# =========================
class PredictRequest(BaseModel):
    raca: Literal["Angus", "Nelore", "Hereford", "Brahman"]
    idade_meses: int
    altura_cm: float
    comprimento_corpo_cm: float
    circunferencia_peito_cm: float
    cor_pelagem: Literal["marrom", "preta", "branca"]
    sexo: Literal["macho", "femea"]

# =========================
# OUTPUT
# =========================
class Insights(BaseModel):
    comparacao_raca: str
    observacoes: str

class Analise(BaseModel):
    classificacao_peso: Literal["baixo", "adequado", "alto"]
    nivel_risco: Literal["baixo", "medio", "alto"]
    recomendacoes: List[str]
    insights: Insights

class PredictResponse(BaseModel):
    peso_estimado_kg: float
    versao_modelo: str
    analise_IA: Analise