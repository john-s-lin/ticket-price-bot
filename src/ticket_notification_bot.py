import dotenv
import json
import logging
import os
import requests
import sys

from utils.utils import TICKET_INFO_FILE

dotenv.load_dotenv()
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_ticket_info_from_file(filename: str) -> dict:
    with open(filename, "r") as f:
        ticket_info = json.load(f)
    return ticket_info


def post_messages(messages: list) -> None:
    for message in messages:
        event = message.split("\n")[0].split(",")[0].split(":")[1].strip()
        # Avatar URL is optional
        avatar_url = (
            "https://img.buzzfeed.com/buzzfeed-static/static/2015-05/27/9/campaign_images/webdr07/beyonce-has-managed-to-become-a-meme-and-its-abso-2-7569-1432732297-9_dblbig.jpg?resize=1200:*"
            if "Beyonce" in event
            else "https://pbs.twimg.com/media/FAsTIRoUcAArn67.jpg"
        )
        payload = {
            "username": f"{event} Ticket Notification Bot",
            "avatar_url": avatar_url,
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
    title = f"Stubhub: {data['event_name']}, {data['date']}"
    min_price = data["min_price"]
    max_price = data["max_price"]
    lowest_ticket_price = data["lowest_price_ticket"]["ticket_price"]
    section = data["lowest_price_ticket"]["section"]
    available_tickets = data["lowest_price_ticket"]["available_tickets"]
    seated_together = data["lowest_price_ticket"]["seated_together"]
    message = (
        f"[{title}]({url})\n"
        + f"min price (estimate): ${min_price:.2f}\n"
        + f"max price (estimate): ${max_price:.2f}\n"
        + f"lowest ticket price (estimate): ${lowest_ticket_price:.2f}\n"
        + f"section: {section}\n"
        + f"available tickets: {available_tickets}\n"
        + f"seated together: {seated_together}"
    )
    return message


def parse_message_from_seatgeek_ticket_info(url: str, data: dict) -> str:
    title = f"Seatgeek: {data['event_name']}, {data['date']}"
    min_price = data["min_price"]
    max_price = data["max_price"]
    median_price = data["median_price"]
    avg_price = data["avg_price"]
    lowest_ticket_price = data["lowest_price_ticket"]["ticket_price"]
    lowest_ticket_section = data["lowest_price_ticket"]["section"]
    best_deal_price = data["best_deal_ticket"]["ticket_price"]
    best_deal_section = data["best_deal_ticket"]["section"]
    message = (
        f"[{title}]({url})\n"
        + f"min price (estimate): ${min_price:.2f}\n"
        + f"max price (estimate): ${max_price:.2f}\n"
        + f"median price (estimate): ${median_price:.2f}\n"
        + f"avg price (estimate): ${avg_price:.2f}\n"
        + f"lowest ticket price (estimate): ${lowest_ticket_price:.2f}\n"
        + f"section: {lowest_ticket_section}\n"
        + f"best deal price (estimate): ${best_deal_price:.2f}\n"
        + f"section: {best_deal_section}"
    )
    return message


def main():
    ticket_info = get_ticket_info_from_file(TICKET_INFO_FILE)
    messages = parse_message_from_ticket_info(ticket_info)
    post_messages(messages)


if __name__ == "__main__":
    main()
