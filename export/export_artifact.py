import os
import pickle
from datetime import datetime
from version_control.get_model_version import get_model_version
from version_control.update_env_variable import update_env_variable
from version_control.log_version_control import log_version_control


def export_model_artifact(
    model,
    encoder,
    categorical_cols: list,
    filename: str,
    timestamp: bool = False
) -> str:
    '''
    Exporta um artifact completo contendo modelo, encoder e metadados.

    Parâmetros
    ----------
    model : object
        - Modelo treinado.
    encoder : object
        - Encoder ajustado (ex: OneHotEncoder).
    categorical_cols : list
        - Lista de colunas categóricas utilizadas no encoding.
    filename : str
        - Nome do arquivo (sem extensão).
    timestamp : bool, opcional
        - Se True, adiciona timestamp ao nome do arquivo.

    Retorna
    -------
    str
        - Nome do arquivo salvo (com extensão .pkl).

    Notas
    -----
    - O diretório ./models/ é criado automaticamente caso não exista.
    '''

    if '.' in filename:
        raise ValueError("O nome do arquivo não deve conter extensão.")

    # 📁 Garante diretório
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    os.makedirs(models_dir, exist_ok=True)

    # 🔢 Gerencia versão automaticamente
    previous_model_version = get_model_version()
    current_version = previous_model_version + 1
    filename = f"{filename}_v{current_version}"

    # 🕒 Timestamp opcional
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{ts}"

    filepath = os.path.join(models_dir, filename)

    # 📦 Artifact completo
    artifact = {
        "model": model,
        "encoder": encoder,
        "categorical_cols": categorical_cols,
        "created_at": datetime.now().isoformat(),
        "version": filename
    }

    print("Artifact:\n")
    for key, value in artifact.items():
        print(f"  {key}: {value}")

    # 💾 Save
    with open(f"{filepath}.pkl", "wb") as file:
        pickle.dump(artifact, file)

    print("\n📦 Artifact salvo com sucesso:")
    print(f"   → ./models/{filename}.pkl\n")

    model_artifact_filename = f"{filename}.pkl"

    # 🔄 Atualiza variável de ambiente
    update_env_variable(file_path = ".env", key = "MODEL_ARTIFACT_NAME", new_value = model_artifact_filename)

    # 📝 Log de versionamento
    log_version_control(model_artifact_filename = model_artifact_filename)

    return model_artifact_filename