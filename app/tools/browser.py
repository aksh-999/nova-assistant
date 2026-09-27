import webbrowser
from urllib.parse import quote_plus


WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "spotify": "https://open.spotify.com",
    "whatsapp": "https://web.whatsapp.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "google drive": "https://drive.google.com",
    "google docs": "https://docs.google.com",
    "google calendar": "https://calendar.google.com",
    "netflix": "https://www.netflix.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "reddit": "https://www.reddit.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "chatgpt": "https://chatgpt.com",
    "claude": "https://claude.ai",
    "gemini": "https://gemini.google.com",
}


def open_website(site_name):
    site_name = site_name.lower().strip()

    url = WEBSITES.get(site_name)

    if not url:
        return None

    webbrowser.open(url)

    return f"Opening {site_name}."


def search_google(query):
    query = query.strip()

    if not query:
        return None

    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    webbrowser.open(url)

    return f"Searching Google for {query}."


def search_youtube(query):
    query = query.strip()

    if not query:
        return None

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )

    webbrowser.open(url)

    return f"Searching YouTube for {query}."


def handle_browser_command(text):

    text = text.lower().strip()

    # Google search
    if text.startswith("search google for "):

        query = text[len("search google for "):].strip()

        return search_google(query)

    # Generic Google search
    if text.startswith("google "):

        query = text[len("google "):].strip()

        return search_google(query)

    # YouTube search
    if text.startswith("search youtube for "):

        query = text[len("search youtube for "):].strip()

        return search_youtube(query)

    # Generic YouTube search
    if text.startswith("youtube "):

        query = text[len("youtube "):].strip()

        return search_youtube(query)

    # Open website
    if text.startswith("open "):

        requested_site = text[5:].strip()

        return open_website(requested_site)

    return None