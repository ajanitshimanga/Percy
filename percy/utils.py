import os
from pathlib import Path


PERCY_PROJECT_ROOT = str(Path(__file__).parent)
RELATIVE_RESOURCE_PATH = "resources/characters/valorant/agents"
RESOURCE_PATH = str(os.path.join(PERCY_PROJECT_ROOT, "resources/characters/valorant/agents"))


def get_absolute_path(relative_path: str) -> str:
    # Get the current working directory or the directory of the script
    base_dir = PERCY_PROJECT_ROOT  # Use __file__ to get the script's directory

    # Create the full path by joining the base directory with the relative path
    full_path = base_dir / relative_path
    # Convert to absolute path
    return str(full_path.resolve())  # Resolve to get the absolute path

