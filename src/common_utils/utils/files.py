import yaml

def open_yaml_file(path: str) -> dict:
    # Reads a yaml file.
    # Returns {} if file is empty
    # Throws Exception on error
    with open(path) as file:
        content = yaml.safe_load(file)
    return content if content else {}


