import os
import pickle
import pandas as pd

def test_exported_model(model_artifact_filename: str, X_test: pd.DataFrame) -> None:
    """
    Realiza testes de inferência em um modelo treinado utilizando um
    subconjunto dos dados de teste.

    Parâmetros
    ----------
    model_artifact_filename : str
        - Nome do arquivo do modelo salvo.
    X_test : pandas.DataFrame
        - Conjunto de dados de teste utilizado na inferência.

    Retorna
    -------
    None
    """
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)

    model_path = os.path.join(models_dir, model_artifact_filename.replace('.pkl', ''))
    artifact = pickle.load(open(f'{model_path}.pkl', 'rb'))
    model = artifact['model']

    print(f"\n{'='*60}")
    print(f"📊 Testing model: {model_artifact_filename.replace('_artifact', '')}")
    print(f"{'='*60}\n")

    print("Test data columns:")
    print(X_test.columns)

    pred = model.predict(X_test.head(10))
    pred = pd.Series(pred, name='predicted_peso_kg')

    print("\nPredictions on first 10 samples:\n")
    print(pred.head(10))