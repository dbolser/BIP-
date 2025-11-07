#!/usr/bin/env python3
"""
Scrape emoji data from Unicode.org full emoji list
Downloads emoji images and creates metadata JSON
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin

def scrape_emoji_list():
    """Scrape the Unicode emoji list and download images"""

    url = "https://unicode.org/emoji/charts/full-emoji-list.html"
    print(f"Fetching {url}...")

    response = requests.get(url)
    response.raise_for_status()

    print("Parsing HTML...")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the emoji table
    table = soup.find('table')
    if not table:
        print("ERROR: Could not find emoji table!")
        return

    emoji_data = []

    # Parse table rows
    rows = table.find_all('tr')
    print(f"Found {len(rows)} rows in table")

    for i, row in enumerate(rows):
        if i == 0:  # Skip header
            continue

        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        # Extract data
        try:
            # Column 0: Number
            # Column 1: Code (codepoints)
            # Column 2+: Images from different platforms
            # Last column: CLDR short name

            code_col = cols[1] if len(cols) > 1 else None
            name_col = cols[-1] if len(cols) > 0 else None

            if not code_col or not name_col:
                continue

            codepoint = code_col.get_text(strip=True)
            cldr_name = name_col.get_text(strip=True)

            # Get platform images
            platform_images = {}
            image_cols = cols[2:-1]  # All columns between code and name

            for img_col in image_cols:
                img_tag = img_col.find('img')
                if img_tag and img_tag.get('src'):
                    # Platform name might be in header
                    platform_images[f"platform_{len(platform_images)}"] = img_tag['src']

            emoji_info = {
                'codepoint': codepoint,
                'cldr_name': cldr_name,
                'platform_images': platform_images
            }

            emoji_data.append(emoji_info)

            if i % 100 == 0:
                print(f"Processed {i} rows...")

        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue

    print(f"\nExtracted {len(emoji_data)} emoji entries")

    # Save metadata
    os.makedirs('data', exist_ok=True)

    with open('data/emoji_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(emoji_data, f, indent=2, ensure_ascii=False)

    print(f"Saved metadata to data/emoji_metadata.json")

    # Show sample
    if emoji_data:
        print("\nSample entries:")
        for item in emoji_data[:5]:
            print(f"  {item['codepoint']} - {item['cldr_name']}")

    return emoji_data

if __name__ == '__main__':
    try:
        scrape_emoji_list()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
