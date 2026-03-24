import json
import os
from datetime import datetime
from version_control.get_model_version import get_model_version
from version_control.get_model_artifact_filename import get_model_artifact_filename


LOG_DIR = "version_control/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    f"version_control_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
)
        
def log_version_control(model_artifact_filename: str):
    previous_model_artifact_filename = f'{get_model_artifact_filename()}.pkl'
    version = get_model_version(previous_model_artifact_filename) + 1
    log_entry = {
        "event": "model_version_update",
        "message": f"New model deployed. Previous: '{previous_model_artifact_filename}' → New: '{model_artifact_filename}'",
        "previous_model_artifact": previous_model_artifact_filename,
        "new_model_artifact": model_artifact_filename,
        "timestamp": datetime.now().isoformat(),
        "version": version
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=4, sort_keys=False)
        f.write("\n")  # separate each log entry with a newline
    
    print(f"\n=> Logged version control event to {LOG_FILE}:\n\n{json.dumps(log_entry, indent=4)}\n")