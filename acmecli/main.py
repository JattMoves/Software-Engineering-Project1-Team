# CLI entry point
import sys
from utils.file_ops import read_url_file
from scoring.orchestrator import process_resources

def main():
    if len(sys.argv) != 2:
        print("Usage: main.py URL_FILE")
        sys.exit(1)

    url_file = sys.argv[1]
    urls = read_url_file(url_file)
    results = process_resources(urls)

    for res in results:
        print(res.to_ndjson())

if __name__ == "__main__":
    main()
