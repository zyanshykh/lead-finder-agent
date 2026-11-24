import argparse
import csv
import glob

from search import search_places
from filter import filter_leads
from message import write_message, whatsapp_link
from export import save_leads


def seen_phones():
    """Pehle save hui leads ke phone numbers, taake dobara message na jaye."""
    seen = set()
    for path in glob.glob("data/leads_*.csv"):
        with open(path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                seen.add(row["phone"])
    return seen


def run(query, limit, pool):
    found = search_places(query, pool)
    leads = filter_leads(found)
    seen = seen_phones()
    fresh = [b for b in leads if b["phone"] not in seen][:limit]

    print(f"{len(found)} mile, {len(leads)} leads, {len(fresh)} naye")
    rows = []
    for b in fresh:
        msg = write_message(b)
        link = whatsapp_link(b["phone"], msg)
        rows.append({**b, "message": msg,
                     "whatsapp_link": link or "LANDLINE: call karo",
                     "status": "new"})
    if rows:
        print("Saved:", save_leads(rows))
    else:
        print("Koi naya lead nahi, doosra area try karo.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="restaurants in Gulshan-e-Iqbal Karachi")
    ap.add_argument("--limit", type=int, default=10, help="kitne naye leads")
    ap.add_argument("--pool", type=int, default=40, help="kitne results search karne")
    a = ap.parse_args()
    run(a.query, a.limit, a.pool)
