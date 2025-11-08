#!/usr/bin/env python3
"""
Download emoji images for test sample from multiple platforms
Uses Twemoji (Twitter) as a starting point for prototyping
"""

import json
import requests
import os
from pathlib import Path

def download_test_images(sample_file='data/test_sample.json'):
    """Download emoji images for test sample"""

    with open(sample_file, 'r', encoding='utf-8') as f:
        sample = json.load(f)

    print(f"Downloading images for {len(sample)} emoji...")

    # Create directories
    output_dir = Path('data/test_images')
    output_dir.mkdir(parents=True, exist_ok=True)

    # We'll use Twemoji (Twitter's emoji) as they're free and open source
    # URL format: https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{codepoint}.png

    downloaded = 0
    failed = []

    for emoji in sample:
        # Convert codepoint to lowercase and handle multi-codepoint emoji
        codepoint = emoji['codepoint'].replace(' ', '-').lower()

        # Twemoji URL
        url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{codepoint}.png"

        # Create safe filename
        safe_name = emoji['name'].replace('/', '-').replace(' ', '_')
        filename = f"{codepoint}_{safe_name}.png"
        filepath = output_dir / filename

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(response.content)

            downloaded += 1
            if downloaded % 10 == 0:
                print(f"  Downloaded {downloaded}/{len(sample)}...")

        except Exception as e:
            failed.append((emoji['emoji'], emoji['name'], str(e)))
            # Try without variation selectors for some emoji
            if 'fe0f' in codepoint.lower():
                alt_codepoint = codepoint.replace('-fe0f', '')
                alt_url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{alt_codepoint}.png"
                try:
                    response = requests.get(alt_url, timeout=10)
                    response.raise_for_status()
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    downloaded += 1
                    failed.pop()  # Remove from failed list
                except:
                    pass

    print(f"\n✅ Downloaded {downloaded}/{len(sample)} images")

    if failed:
        print(f"\n❌ Failed to download {len(failed)} images:")
        for emoji, name, error in failed[:10]:  # Show first 10
            print(f"  {emoji} {name}: {error}")

    print(f"\nImages saved to: {output_dir}")

    return downloaded, failed

if __name__ == '__main__':
    download_test_images()
