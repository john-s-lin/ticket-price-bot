import dotenv
import json
import logging
import os
import requests
import sys

from utils.utils import LOG_DIR, TICKET_INFO_FILE

dotenv.load_dotenv()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_ticket_info_from_file(filename: str) -> dict:
    with open(filename, "r") as f:
        ticket_info = json.load(f)
    return ticket_info


def post_messages(messages: list) -> None:
    for message in messages:
        payload = {
            "username": "Twice Ticket Notification Bot",
            "avatar_url": "https://pbs.twimg.com/media/FAsTIRoUcAArn67.jpg",  # Optional, this is Jihyo's meme face
            "embeds": [{"description": message, "color": 1673044}],
        }

        with requests.post(WEBHOOK_URL, json=payload) as response:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logging.error(err)
            else:
                logging.info(
                    f"Payload delivered successfully, code {response.status_code}"
                )


def parse_message_from_ticket_info(ticket_info: dict) -> list:
    messages = []
    for url, data in ticket_info.items():
        if "stubhub" in url:
            messages.append(parse_message_from_stubhub_ticket_info(url, data))
        elif "seatgeek" in url:
            messages.append(parse_message_from_seatgeek_ticket_info(url, data))
    return messages


def parse_message_from_stubhub_ticket_info(url: str, data: dict) -> str:
    title = f"Stubhub: {data['date']}"
    min_price = data["min_price"]
    max_price = data["max_price"]
    lowest_ticket_price = data["lowest_price_ticket"]["ticket_price"]
    section = data["lowest_price_ticket"]["section"]
    available_tickets = data["lowest_price_ticket"]["available_tickets"]
    seated_together = data["lowest_price_ticket"]["seated_together"]
    message = f"[{title}]({url})\nmin price: ${min_price}\nmax price: ${max_price}\nlowest ticket price: ${lowest_ticket_price}\nsection: {section}\navailable tickets: {available_tickets}\nseated together: {seated_together}"
    return message


def parse_message_from_seatgeek_ticket_info(url: str, data: dict) -> str:
    title = f"Seatgeek: {data['date']}"
    min_price = data["min_price"]
    max_price = data["max_price"]
    median_price = data["median_price"]
    avg_price = data["avg_price"]
    lowest_ticket_price = data["lowest_price_ticket"]["ticket_price"]
    section = data["lowest_price_ticket"]["section"]
    message = f"[{title}]({url})\nmin price: ${min_price:.2f}\nmax price: ${max_price:.2f}\nmedian price: ${median_price:.2f}\navg price: ${avg_price:.2f}\nlowest ticket price: ${lowest_ticket_price:.2f}\nsection: {section}"
    return message


def main():
    ticket_info = get_ticket_info_from_file(TICKET_INFO_FILE)
    messages = parse_message_from_ticket_info(ticket_info)
    post_messages(messages)


if __name__ == "__main__":
    main()
