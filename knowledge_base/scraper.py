"""Populate the reference-design library by screenshotting well-designed sites.

Uses thum.io (https://www.thum.io) which renders a full screenshot of any public
URL with no API key required. Images are saved into the reference-images folder
using a `{category}_{slug}.png` naming scheme so the existing ingest pipeline
(knowledge_base/ingest.py) can derive the category and caption automatically.

Run:
    python knowledge_base/scraper.py            # download + ingest into LanceDB
    python knowledge_base/scraper.py --no-ingest # download only
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import REFERENCE_IMAGES_DIR

# `wait` lets thum.io finish rendering before responding (avoids the "loading"
# placeholder image); `maxAge/1` busts its cache so re-runs get a fresh render.
THUMIO_TEMPLATE = "https://image.thum.io/get/width/1200/crop/1400/wait/12/maxAge/1/{url}"
REQUEST_TIMEOUT = 90

# Curated set of well-designed, public sites grouped by design category.
# Keep URLs bare (no scheme) — the slug is derived from the host.
CURATED_SITES: dict[str, list[str]] = {
    "landing": [
        "https://stripe.com",
        "https://linear.app",
        "https://vercel.com",
        "https://framer.com",
        "https://www.apple.com",
    ],
    "saas": [
        "https://www.notion.so",
        "https://slack.com",
        "https://www.figma.com",
        "https://www.intercom.com",
        "https://www.airtable.com",
    ],
    "dashboard": [
        "https://www.datadoghq.com",
        "https://www.tableau.com",
        "https://posthog.com",
        "https://www.retool.com",
    ],
    "ecommerce": [
        "https://www.shopify.com",
        "https://www.allbirds.com",
        "https://www.gymshark.com",
        "https://www.glossier.com",
    ],
    "portfolio": [
        "https://bruno-simon.com",
        "https://www.awwwards.com",
        "https://readymag.com",
    ],
    "mobile": [
        "https://www.duolingo.com",
        "https://www.headspace.com",
        "https://cash.app",
        "https://robinhood.com",
    ],
}


def _slug(url: str) -> str:
    host = re.sub(r"^https?://", "", url).strip("/")
    host = host.split("/")[0]
    host = host.replace("www.", "")
    return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")


def _screenshot_url(url: str) -> str:
    return THUMIO_TEMPLATE.format(url=url)


def download_screenshots(overwrite: bool = False) -> list[Path]:
    """Fetch a screenshot for every curated site. Returns the saved file paths."""
    out_dir = Path(REFERENCE_IMAGES_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    saved: list[Path] = []
    for category, urls in CURATED_SITES.items():
        for url in urls:
            dest = out_dir / f"{category}_{_slug(url)}.png"
            if dest.exists() and not overwrite:
                print(f"  skip (exists): {dest.name}")
                saved.append(dest)
                continue
            try:
                print(f"  fetching {url} -> {dest.name}")
                resp = requests.get(
                    _screenshot_url(url),
                    timeout=REQUEST_TIMEOUT,
                    headers={"User-Agent": "design-evaluator-scraper/1.0"},
                )
                resp.raise_for_status()
                content = resp.content
                if not content or len(content) < 1000:
                    print(f"    empty/invalid response for {url}, skipping")
                    continue
                dest.write_bytes(content)
                saved.append(dest)
                time.sleep(1.0)  # be polite to the free service
            except Exception as exc:  # noqa: BLE001 - keep scraping the rest
                print(f"    failed {url}: {exc}")

    print(f"Downloaded/kept {len(saved)} reference screenshots in {out_dir}")
    return saved


def scrape(ingest: bool = True, overwrite: bool = False) -> dict:
    saved = download_screenshots(overwrite=overwrite)
    result = {"downloaded": len(saved)}
    if ingest:
        from knowledge_base.ingest import ingest_knowledge_base

        print("Running ingestion to (re)build the LanceDB index...")
        result.update(ingest_knowledge_base())
    return result


if __name__ == "__main__":
    do_ingest = "--no-ingest" not in sys.argv
    do_overwrite = "--overwrite" in sys.argv
    scrape(ingest=do_ingest, overwrite=do_overwrite)
