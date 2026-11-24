import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchText"

FIELDS = ",".join([
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.rating",
    "places.userRatingCount",
    "places.googleMapsUri",
    "nextPageToken",
])


def search_places(query, max_results=20):
    """Google Places se businesses dhoondta hai."""
    if not API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY .env mein nahi mili")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": FIELDS,
    }
    body = {"textQuery": query, "pageSize": 20}
    results = []

    while len(results) < max_results:
        r = requests.post(URL, json=body, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        for p in data.get("places", []):
            results.append({
                "name": p.get("displayName", {}).get("text", ""),
                "address": p.get("formattedAddress", ""),
                "phone": p.get("nationalPhoneNumber", ""),
                "website": p.get("websiteUri", ""),
                "rating": p.get("rating", 0),
                "reviews": p.get("userRatingCount", 0),
                "maps_url": p.get("googleMapsUri", ""),
            })
        token = data.get("nextPageToken")
        if not token:
            break
        body["pageToken"] = token

    return results[:max_results]


if __name__ == "__main__":
    leads = search_places("restaurants in Gulshan-e-Iqbal Karachi", 10)
    for b in leads:
        print(b["name"], "|", b["phone"], "|", b["website"] or "NO WEBSITE")
