import ticket_notification_bot
import ticket_price_scraper


def main():
    ticket_info = ticket_price_scraper.pass_ticket_info_to_bot()
    messages = ticket_notification_bot.parse_message_from_ticket_info(ticket_info)
    ticket_notification_bot.post_messages(messages)


if __name__ == "__main__":
    main()
