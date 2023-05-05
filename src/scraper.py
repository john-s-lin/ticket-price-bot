import logging
import os
import sys

from scrapy.http.response.html import HtmlResponse
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule

# Set logging to console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# I just want Twice tickets at the lowest price because actual scalpers are the worst
TARGET_URLS = [
    "https://www.ticketmaster.ca/twice-5th-world-tour-ready-to-toronto-ontario-07-02-2023/event/10005E51A7641B24",  # Ticketmaster might block this because it's a bot
    "https://www.ticketmaster.ca/twice-5th-world-tour-ready-to-toronto-ontario-07-03-2023/event/10005E70271A4DB8",
    "https://seatgeek.ca/twice-tickets/toronto-canada-scotiabank-arena-4-2023-07-02-7-30-pm/concert/5952228",
    "https://seatgeek.ca/twice-tickets/toronto-canada-scotiabank-arena-4-2023-07-03-7-30-pm/concert/5976418",
    "https://www.stubhub.ca/twice-toronto-tickets-7-2-2023/event/151494669/?quantity=2",
    "https://www.stubhub.ca/twice-toronto-tickets-7-3-2023/event/151600390/?quantity=2",
]


class TwiceTicketScraper(CrawlSpider):
    name = "twice_ticket_scraper"
    allowed_domains = ["ticketmaster.ca", "seatgeek.ca", "stubhub.ca"]
    start_urls = TARGET_URLS

    def parse_item(self, response: HtmlResponse):
        """Returns response body as a dict

        Args:
            response (HtmlResponse): _description_
        """
        if response == 403:
            logging.warning("Ticketmaster blocked this bot")
        print(response)
        return None


def crawl():
    process = CrawlerProcess()
    process.crawl(TwiceTicketScraper)
    process.start()


def main():
    crawl()


if __name__ == "__main__":
    main()
