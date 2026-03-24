import os
import re
import pickle
import pandas as pd
from version_control.get_model_version import get_model_version


def validate_features(df: pd.DataFrame, estimator) -> None:
    """
    Valida se as features do DataFrame batem com o modelo.
    """

    if hasattr(estimator, "feature_names_in_"):
        expected = set(estimator.feature_names_in_)
        provided = set(df.columns)

        if expected != provided:
            raise ValueError(
                "Feature mismatch between model and inference input.\n"
                f"Model expects: {expected}\n"
                f"Input provides: {provided}"
            )


def transform_input(input_data: dict, encoder, categorical_cols) -> pd.DataFrame:
    """
    Converte input bruto em DataFrame compatível com o modelo,
    incluindo encoding.
    """

    df = pd.DataFrame([input_data])

    # 🔧 Tipagem
    df["idade_meses"] = df["idade_meses"].astype(int)
    df["altura_cm"] = df["altura_cm"].astype(float)
    df["comprimento_corpo_cm"] = df["comprimento_corpo_cm"].astype(float)
    df["circunferencia_peito_cm"] = df["circunferencia_peito_cm"].astype(float)

    # Separar categóricas
    df_cat = df[categorical_cols]

    # Aplicar encoder
    encoded = encoder.transform(df_cat)
    encoded_cols = encoder.get_feature_names_out(categorical_cols)

    df_encoded = pd.DataFrame(encoded, columns=encoded_cols)

    # Numéricas
    df_num = df.drop(columns=categorical_cols)

    # Combinar
    df_final = pd.concat([df_num.reset_index(drop=True), df_encoded], axis=1)

    return df_final


def predict_weight(model_artifact_filename: str, input_data: dict) -> dict:
    """
    Predição com modelo + encoder persistidos.
    """

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    model_artifact_path = os.path.abspath(f"{models_dir}/{model_artifact_filename}.pkl")

    # 🔄 Load artifact
    with open(model_artifact_path, "rb") as f:
        artifact = pickle.load(f)

    model = artifact["model"]
    encoder = artifact["encoder"]
    categorical_cols = artifact["categorical_cols"]

    # 🔍 Extrair versão do nome do arquivo (ex: "cattle_weight_model_v1" → v1)
    version = get_model_version(model_artifact_filename)
    if version != 0:
        version = f"v{version}"
    else:
        version = "not found"

    # 🔄 Transform input (já com encoding)
    x = transform_input(input_data, encoder, categorical_cols)

    # 🔍 Validar features finais
    validate_features(x, model)

    # 📈 Predict
    pred = model.predict(x)

    return {
        "peso_estimado_kg": float(pred[0]),
        "versao_modelo": version
    }