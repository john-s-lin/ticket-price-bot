from pathlib import Path

LOG_DIR = Path(__file__).parents[2].joinpath("logs")
OUTPUT_DIR = Path(__file__).parents[2].joinpath("output")
TICKET_INFO_FILE = OUTPUT_DIR.joinpath("ticket_info.json")
INPUT_FILE = Path(__file__).parents[2].joinpath("input/input_url.txt")


def get_target_urls_from_file(file_path: str) -> list:
    with open(file_path, "r") as f:
        urls = f.readlines()
    return [url.strip() for url in urls]


TARGET_URLS = get_target_urls_from_file(INPUT_FILE)
