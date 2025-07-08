import configparser
import json
import yaml
import os
import shutil

REQUIRED_KEYS = ['DEBUG', 'LOG_LEVEL', 'API_KEY', 'DATABASE_URL']
CONFIG_DIR = "configs"

def generate_config(env, file_type='ini'):
    data = {
        "DEBUG": True if env == "dev" else False,
        "LOG_LEVEL": "DEBUG" if env == "dev" else "INFO",
        "API_KEY": f"{env}-key",
        "DATABASE_URL": f"localhost:5432/{env}_db"
    }

    filename = f"{env}_config.{file_type}"
    filepath = os.path.join(CONFIG_DIR, filename)

    if file_type == 'ini':
        config = configparser.ConfigParser()
        config['DEFAULT'] = {k: str(v) for k, v in data.items()}
        with open(filepath, 'w') as f:
            config.write(f)
    elif file_type == 'json':
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    elif file_type == 'yaml':
        with open(filepath, 'w') as f:
            yaml.dump(data, f)

    return filepath

def validate_config(path, file_type):
    missing_keys = []

    if file_type == 'ini':
        config = configparser.ConfigParser()
        config.read(path)
        config_data = config['DEFAULT']
    elif file_type == 'json':
        with open(path) as f:
            config_data = json.load(f)
    elif file_type == 'yaml':
        with open(path) as f:
            config_data = yaml.safe_load(f)
    else:
        return ['Invalid file type']

    for key in REQUIRED_KEYS:
        if key not in config_data:
            missing_keys.append(key)

    return missing_keys

def switch_config(env, file_type):
    src = os.path.join(CONFIG_DIR, f"{env}_config.{file_type}")
    dest = os.path.join(CONFIG_DIR, f"active_config.{file_type}")
    shutil.copy(src, dest)
    return dest
