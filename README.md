# Lead Finder Agent

Finds local Karachi businesses that have no real website and prepares a ready-to-send WhatsApp message for each one. Built to find web development clients.

## How it works

1. `search.py` searches Google Places for businesses in an area.
2. `filter.py` keeps businesses with no real website (social pages only) that have a phone number and some reviews.
3. `message.py` writes a short personalized message with Gemini and builds a `wa.me` link.
4. `export.py` and `main.py` (coming soon) save leads to CSV and run everything in one command.

## Setup

    git clone https://github.com/zyanshykh/lead-finder-agent.git
    cd lead-finder-agent
    pip install -r requirements.txt
    cp .env.example .env

Add your keys to `.env`:

    GOOGLE_PLACES_API_KEY=your_key
    GEMINI_API_KEY=your_key
    GEMINI_MODEL=gemini-flash-latest

## Usage

    python src/search.py     # test business search
    python src/filter.py     # show leads without a website
    python src/message.py    # generate messages and WhatsApp links

## Notes

- Messages are sent manually. Tap the link, review the message, press Send.
- Never commit your `.env` file.
- Landline numbers cannot use WhatsApp, so call those leads.

## Roadmap

- [x] Places search
- [x] No-website filter
- [x] Gemini message and WhatsApp link
- [ ] CSV export
- [ ] Single `main.py` runner
- [ ] Daily run with GitHub Actions

## Author

Zayyan Shaikh, Karachi
