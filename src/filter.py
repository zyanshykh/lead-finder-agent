SOCIAL_DOMAINS = ("facebook.com", "instagram.com", "tiktok.com", "linktr.ee", "wa.me")


def has_real_website(url):
    """True agar apni asli website hai (social page nahi)."""
    if not url:
        return False
    return not any(d in url.lower() for d in SOCIAL_DOMAINS)


def filter_leads(businesses, min_reviews=5):
    """Wo businesses jinki apni website nahi, magar phone hai aur kaam chal raha hai."""
    leads = []
    for b in businesses:
        if has_real_website(b["website"]):
            continue
        if not b["phone"]:
            continue
        if b["reviews"] < min_reviews:
            continue
        leads.append(b)
    return leads


if __name__ == "__main__":
    from search import search_places

    found = search_places("restaurants in Gulshan-e-Iqbal Karachi", 20)
    leads = filter_leads(found)
    print(f"{len(found)} mein se {len(leads)} leads:")
    for b in leads:
        print(b["name"], "|", b["phone"], "|", b["website"] or "NO WEBSITE")
