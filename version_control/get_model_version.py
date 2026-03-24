import os
import re
from dotenv import load_dotenv

def get_model_version(model_artifact_filename: str | None = None) -> int:
    if model_artifact_filename is not None:
        MODEL_ARTIFACT_NAME = model_artifact_filename
    else:
        load_dotenv()
        MODEL_ARTIFACT_NAME = os.getenv("MODEL_ARTIFACT_NAME")
        
    # 🔍 Extrair versão do nome do arquivo (ex: "cattle_weight_model_v1" → v1)
    version = 0
    if MODEL_ARTIFACT_NAME != None:
        match = re.search(r"_v(\d+)", MODEL_ARTIFACT_NAME)
            
        if match:
            version = int(match.group(1))
    
    return version