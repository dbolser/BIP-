#!/usr/bin/env python3
"""
Scrape emoji data from Unicode.org emoji test file
Much faster and lighter than the full HTML page
"""

import requests
import json
import os
import re

def scrape_emoji_test():
    """Scrape the Unicode emoji test file for emoji data"""

    url = "https://unicode.org/Public/emoji/16.0/emoji-test.txt"
    print(f"Fetching {url}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    print("Parsing emoji test data...")

    emoji_data = []
    lines = response.text.split('\n')

    for line in lines:
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue

        # Parse emoji test format:
        # codepoint ; status # emoji E version name
        # Example: 1F600 ; fully-qualified # 😀 E1.0 grinning face

        match = re.match(r'^([0-9A-F\s]+)\s*;\s*(\S+)\s*#\s*(\S+)\s+E(\S+)\s+(.+)$', line)
        if match:
            codepoints = match.group(1).strip()
            status = match.group(2)
            emoji_char = match.group(3)
            version = match.group(4)
            name = match.group(5).strip()

            emoji_info = {
                'codepoint': codepoints,
                'status': status,
                'emoji': emoji_char,
                'version': version,
                'name': name
            }

            emoji_data.append(emoji_info)

    print(f"\nExtracted {len(emoji_data)} emoji entries")

    # Save metadata
    os.makedirs('data', exist_ok=True)

    with open('data/emoji_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(emoji_data, f, indent=2, ensure_ascii=False)

    print(f"Saved metadata to data/emoji_metadata.json")

    # Show sample and statistics
    if emoji_data:
        print("\nSample entries:")
        for item in emoji_data[:10]:
            print(f"  {item['emoji']} - {item['name']} (E{item['version']})")

        # Count by status
        fully_qualified = sum(1 for e in emoji_data if e['status'] == 'fully-qualified')
        print(f"\nStatistics:")
        print(f"  Total: {len(emoji_data)}")
        print(f"  Fully-qualified: {fully_qualified}")

    return emoji_data

if __name__ == '__main__':
    try:
        scrape_emoji_test()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
