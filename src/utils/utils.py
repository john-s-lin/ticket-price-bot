from pathlib import Path

LOG_DIR = Path(__file__).parents[2].joinpath("logs")
OUTPUT_DIR = Path(__file__).parents[2].joinpath("output")
TICKET_INFO_FILE = OUTPUT_DIR.joinpath("ticket_info.json")
