import json
import logging
import os
import re
import requests

from pathlib import Path
from bs4 import BeautifulSoup
from utils.utils import LOG_DIR, OUTPUT_DIR, TICKET_INFO_FILE


# I just want Twice tickets at the lowest price because actual scalpers are the worst
TARGET_URLS = [
    "https://www.ticketmaster.ca/twice-5th-world-tour-ready-to-toronto-ontario-07-02-2023/event/10005E51A7641B24",  # Ticketmaster might block this because it's a bot
    "https://www.ticketmaster.ca/twice-5th-world-tour-ready-to-toronto-ontario-07-03-2023/event/10005E70271A4DB8",
    "https://seatgeek.ca/twice-tickets/toronto-canada-scotiabank-arena-4-2023-07-02-7-30-pm/concert/5952228",
    "https://seatgeek.ca/twice-tickets/toronto-canada-scotiabank-arena-4-2023-07-03-7-30-pm/concert/5976418",
    "https://www.stubhub.ca/twice-toronto-tickets-7-2-2023/event/151494669/?quantity=2",
    "https://www.stubhub.ca/twice-toronto-tickets-7-3-2023/event/151600390/?quantity=2",
]


# Set logging to console
logging.basicConfig(
    filename=LOG_DIR.joinpath("output.log"), filemode="w", level=logging.INFO
)


class TicketInfoScraper:
    def __init__(self) -> None:
        pass

    def get_lowest_price_ticket_info(self, urls: list) -> dict:
        output = {}
        for url in urls:
            response = requests.get(url)

            if response.status_code != 200:
                logging.error(f"Failed to get response from {url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            logging.info(f"Parsing ticket info from {url}")
            if re.search("stubhub", url):
                output[url] = self.parse_stubhub_for_lowest_price_ticket(soup)
            elif re.search("seatgeek", url):
                output[url] = self.parse_seatgeek_for_lowest_price_ticket(soup)

        return output

    def parse_stubhub_for_lowest_price_ticket(self, soup: BeautifulSoup) -> dict:
        """Returns a dictionary of the lowest price ticket information

        Args:
            soup (BeautifulSoup): soup object of the page

        Returns:
            dict: dictionary of the lowest price ticket information
        """
        raw_target = soup.find("script", {"id": "index-data"}).get_text()
        target = json.loads(raw_target)
        item_list = target["grid"]["items"]
        min_price = target["grid"]["minPrice"]
        max_price = target["grid"]["maxPrice"]
        date = target["formattedEventDateTime"]
        raw_price = max_price

        for item in item_list:
            if item["availableTickets"] > 0:
                curr_price = item["rawPrice"]
                if curr_price < raw_price:
                    raw_price = curr_price
                    section = item["section"]
                    available_tickets = item["availableQuantities"]
                    seated_together = item["isSeatedTogether"]

        return {
            "date": date,
            "min_price": min_price,
            "max_price": max_price,
            "lowest_price_ticket": {
                "ticket_price": raw_price,
                "section": section,
                "available_tickets": available_tickets,
                "seated_together": seated_together,
            },
        }

    def parse_seatgeek_for_lowest_price_ticket(self, soup: BeautifulSoup) -> dict:
        """Return a dictionary of the lowest price ticket information from Seatgeek

        Args:
            soup (BeautifulSoup): soup object of the page

        Returns:
            dict: dictionary of the lowest price ticket information
        """
        raw_target = soup.find(
            "script", {"id": "__NEXT_DATA__", "type": "application/json"}
        ).get_text()
        target = json.loads(raw_target)

        # Store event info
        event = target["props"]["pageProps"]["event"]
        date = event["datetime_local"]

        # Get ticket stats
        stats = event["stats"]
        min_price = stats["lowest_price"]
        max_price = stats["highest_price"]
        median_price = stats["median_price"]
        avg_price = stats["average_price"]

        # Get cheapest ticket info
        cheapest_seat = stats["variants"][0]["stats"]["cheapest_seat_listing"]
        section = cheapest_seat["section"]
        ticket_price = cheapest_seat["price_fees"]

        return {
            "date": date,
            "min_price": min_price,
            "max_price": max_price,
            "median_price": median_price,
            "avg_price": avg_price,
            "lowest_price_ticket": {
                "ticket_price": ticket_price,
                "section": section,
            },
        }


def get_simple_ticket_info():
    ticket_scraper = TicketInfoScraper()
    ticket_info = ticket_scraper.get_lowest_price_ticket_info(TARGET_URLS)

    with open(TICKET_INFO_FILE, "w") as f:
        json.dump(ticket_info, f, indent=2)


def create_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        logging.info(f"Created log directory at {LOG_DIR}")
    else:
        logging.info(f"Log directory already exists at {LOG_DIR}")


def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.info(f"Created output directory at {OUTPUT_DIR}")
    else:
        logging.info(f"Output directory already exists at {OUTPUT_DIR}")


def main():
    create_log_dir()
    create_output_dir()
    get_simple_ticket_info()


if __name__ == "__main__":
    main()
