# File reading/writing
from typing import List

def read_url_file(file_path: str) -> List[str]:
    try:
        with open(file_path, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Error: file not found {file_path}")
        return []
