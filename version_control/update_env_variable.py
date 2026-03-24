import os

def update_env_variable(file_path, key, new_value):
    # Get directory of THIS script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go one level up (project root)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    # Build absolute path to .env
    env_path = os.path.join(project_root, file_path)

    lines = []
    
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip().startswith(f"{key}="):
                f.write(f"{key}={new_value}\n")
            else:
                f.write(line)

    print(f"\n=> Updated {key} in {file_path} to {new_value}\n")