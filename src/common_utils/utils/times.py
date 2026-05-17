from datetime import datetime
import yaml

def format_date(ts: datetime) -> str:
    # Returns string from given datetime object in format `01.12.2026-04:12:12`
    return ts.strftime("%d.%m.%Y-%H:%M:%S")


def open_yaml_file(path: str) -> dict:
    # Reads a yaml file.
    # Returns {} if file is empty
    # Throws Exception on error
    with open(path) as file:
        content = yaml.safe_load(file)
    return content if content else {}