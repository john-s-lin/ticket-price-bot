# ticket-price-bot

## Premise

Due to the nature of Ticketmaster and Live Nation's anti-consumer practices, I was unable to purchase tickets to see Twice in Toronto, the first time they've ever come to Canada. Not having the time to check ticket resellers (scalpers are the worst!) for the cheapest seats every day, I decided to write a script to check prices for me, then send me updates on Discord, using a scheduled Github Action.

## Usage

1. Clone/fork the repository

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Replace the values in `input/input.txt` with links to the events you want to track. Right now, the script only works for `SeatGeek` and `Stubhub`.

> Why is this manual? Ticketmaster blocks `Selenium` and `requests` anyways, but I don't want to write a scraper for every ticket vendor. If you want to use this for a different vendor, you'll have to write your own scraper. Also, I don't want to build a bot to handle user input, and I don't want to automate buying tickets, since I want to check prices myself. Otherwise, I'd be no better than a ticket scalper, and this bot is not meant to scalp tickets. I just want tickets to see Twice.

4. Copy `.env.example` to `.env` and in your target Discord server, provided you have admin privileges, create a webhook and paste the URL into the `.env` file. If you're running this as a Github Action, you'll need to add the webhook URL as a secret in `Settings > Secrets and Variables`.

```bash
WEBHOOK_URL={your-discord-server-webhook-url}
```

## Running the script on Github Actions

I automated this using Github Actions since I don't need a script running 24/7, just once an hour. I was also moving at the time, so couldn't run it as a cron job on my Raspberry Pi. Finally, I didn't want to run a VM in Azure since it seemed wasteful to spin up a machine for a script that takes a minute to run. If you want to run this locally, you can use `cron` to schedule the script to run every hour.

### What it looks like

![Discord webhook](./docs/assets/discord_bot.png)
