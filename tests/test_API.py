import os
import time
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ===============================
# CONFIG
# ===============================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl") # using .jsonl format for easier parsing of individual entries later

API_URL = "http://localhost:8000/predict"  # replace with your deployed endpoint if needed
API_TOKEN = os.getenv("PREDICTION_API_TOKEN") # ensure this is set in your .env file, e.g. PREDICTION_API_TOKEN=your_token_here
TEST_CSV_PATH = "../data/gado_test.csv" # calling from current directory (tests/), adjust if needed

TIMEOUT = 5000  # timeout for API requests in milliseconds (adjust as needed, especially if LLM analysis can take time)

# ===============================
# READ TEST DATA
# ===============================
test_df = pd.read_csv(TEST_CSV_PATH)

# ===============================
# HELPER TO LOG JSON LINES
# ===============================
def log_result(result_dict):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4, sort_keys=False)
        f.write("\n\n")  # separate each log entry with a newline

# ===============================
# ITERATE OVER TEST DATA
# ===============================
for idx, row in test_df.iterrows():
    payload = {
        "raca": row["raca"],
        "idade_meses": int(row["idade_meses"]),
        "altura_cm": float(row["altura_cm"]),
        "comprimento_corpo_cm": float(row["comprimento_corpo_cm"]),
        "circunferencia_peito_cm": float(row["circunferencia_peito_cm"]),
        "cor_pelagem": row["cor_pelagem"],
        "sexo": row["sexo"]
    }

    try:
        headers = {"Authorization": API_TOKEN}
        response = requests.post(API_URL, json=payload, headers=headers, timeout=50)

        if response.status_code != 200:
            log_result({
                "row_index": idx,
                "payload": payload,
                "error": f"[ERROR] HTTP {response.status_code}",
                "response_text": response.text
            })
            print(f"[ERROR] Row {idx}: HTTP {response.status_code}")
            continue

        data = response.json()

        # Check for internal fallback error in the LLM analysis
        if data.get("analise_IA", {}).get("insights", {}).get("comparacao_raca") == "Erro na análise":
            log_result({
                "row_index": idx,
                "payload": payload,
                "error": "[WARNING] Fallback triggered in LLM analysis",
                "response_data": data
            })
            print(f"[WARNING] Row {idx}: Fallback triggered in LLM analysis")
        else:
            log_result({
                "row_index": idx,
                "payload": payload,
                "response_data": data
            })
            print(f"[OK] Row {idx}: peso_estimado={data['peso_estimado_kg']} kg")

    except requests.exceptions.RequestException as e:
        log_result({
            "row_index": idx,
            "payload": payload,
            "error": f"[ERROR] RequestException: {str(e)}"
        })
        print(f"[ERROR] Row {idx}: RequestException -> {str(e)}")

    except Exception as e:
        log_result({
            "row_index": idx,
            "payload": payload,
            "error": f"InternalException: {str(e)}"
        })
        print(f"[ERROR] Row {idx}: InternalException -> {str(e)}")

    finally:
        # Timeout
        time.sleep(TIMEOUT / 1000)  # convert milliseconds to seconds


print(f"Test finished. Log saved to {LOG_FILE}")