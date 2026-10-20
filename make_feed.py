"""Build an RSS feed of the newest datasets in a Borealis (Dataverse) collection.

Run by the GitHub Action every few hours; writes docs/feed.xml, which GitHub
Pages serves at https://<account>.github.io/<repo>/feed.xml.

Uses only the Python standard library. Published datasets are public, so no
API key is needed.
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

SERVER = "https://borealisdata.ca"
COLLECTION = "ubc"          # Borealis collection alias (includes sub-collections)
COUNT = 20                  # items in the feed; the WordPress block picks how many to show
FEED_TITLE = "UBC Borealis: recently published datasets"
OUTPUT = Path(__file__).parent / "docs" / "feed.xml"


def fetch_items():
    params = urllib.parse.urlencode({
        "q": "*",
        "type": "dataset",
        "subtree": COLLECTION,
        "sort": "date",
        "order": "desc",
        "per_page": COUNT,
    })
    req = urllib.request.Request(
        f"{SERVER}/api/search?{params}",
        headers={"Accept": "application/json", "User-Agent": "ubc-borealis-feed"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("status") != "OK":
        raise RuntimeError(f"Borealis API returned: {body}")
    return body["data"]["items"]


def parse_date(value):
    """Dataverse dates look like 2026-10-14T18:22:05Z."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_authors(authors, limit=3):
    if not authors:
        return ""
    text = "; ".join(authors[:limit])
    return text + " et al." if len(authors) > limit else text


def build_rss(items):
    collection_url = f"{SERVER}/dataverse/{COLLECTION}"
    now = format_datetime(datetime.now(timezone.utc))
    entries = []
    for item in items:
        title = item.get("name") or "Untitled dataset"
        link = item.get("url") or collection_url          # DOI link
        guid = item.get("global_id") or link
        published = parse_date(item.get("published_at"))
        authors = format_authors(item.get("authors"))
        description = (item.get("description") or "").strip()
        if len(description) > 400:
            description = description[:400].rsplit(" ", 1)[0] + "…"

        parts = [
            "    <item>",
            f"      <title>{escape(title)}</title>",
            f"      <link>{escape(link)}</link>",
            f'      <guid isPermaLink="false">{escape(guid)}</guid>',
        ]
        if published:
            parts.append(f"      <pubDate>{format_datetime(published)}</pubDate>")
        if authors:
            parts.append(f"      <dc:creator>{escape(authors)}</dc:creator>")
        if item.get("name_of_dataverse"):
            parts.append(f"      <category>{escape(item['name_of_dataverse'])}</category>")
        parts.append(f"      <description>{escape(description)}</description>")
        parts.append("    </item>")
        entries.append("\n".join(parts))

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        "  <channel>\n"
        f"    <title>{escape(FEED_TITLE)}</title>\n"
        f"    <link>{escape(collection_url)}</link>\n"
        "    <description>The newest datasets published in the UBC collection on Borealis.</description>\n"
        "    <language>en-ca</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        + "\n".join(entries)
        + "\n  </channel>\n</rss>\n"
    )


def main():
    try:
        items = fetch_items()
    except Exception as exc:  # keep the previous feed if Borealis is unavailable
        print(f"Could not fetch datasets, keeping existing feed: {exc}", file=sys.stderr)
        return 1 if not OUTPUT.exists() else 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_rss(items), encoding="utf-8")
    print(f"Wrote {len(items)} datasets to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
