import csv
import os
from datetime import date


def save_leads(rows, folder="data"):
    """Leads ko data/leads_YYYY-MM-DD.csv mein save karta hai."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"leads_{date.today()}.csv")
    fields = ["name", "phone", "address", "rating", "reviews",
              "website", "message", "whatsapp_link", "status"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


if __name__ == "__main__":
    from search import search_places
    from filter import filter_leads
    from message import write_message, whatsapp_link

    leads = filter_leads(search_places("restaurants in Gulshan-e-Iqbal Karachi", 20))
    rows = []
    for b in leads[:5]:
        msg = write_message(b)
        link = whatsapp_link(b["phone"], msg)
        rows.append({**b, "message": msg,
                     "whatsapp_link": link or "LANDLINE: call karo",
                     "status": "new"})
    print("Saved:", save_leads(rows))
