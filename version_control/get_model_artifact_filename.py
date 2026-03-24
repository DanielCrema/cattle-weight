import os
from dotenv import load_dotenv

load_dotenv()

def get_model_artifact_filename() -> str:
    previous_model_artifact_filename = ""

    MODEL_ARTIFACT_NAME = os.getenv("MODEL_ARTIFACT_NAME")
    if MODEL_ARTIFACT_NAME is not None:
        previous_model_artifact_filename = MODEL_ARTIFACT_NAME

    return previous_model_artifact_filename