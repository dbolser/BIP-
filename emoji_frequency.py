#!/usr/bin/env python3
"""
Emoji Usage Frequency Analyzer

Analyzes real-world emoji usage to identify most common emoji
for steganographic mapping (hiding addresses in plain text).

Strategy: Map common Base58 characters to common emoji to obscure
the fact that a message contains an address.
"""

import json
from typing import List, Dict


def get_common_emoji_list() -> List[Dict]:
    """
    Get list of most commonly used emoji based on:
    - Unicode Emoji Frequency Report
    - Social media usage statistics
    - Cross-platform availability

    Returns list sorted by usage frequency (most common first)
    """

    # Based on research from:
    # - Emojitracker (Twitter real-time stats)
    # - Unicode CLDR annotations
    # - Various social media studies

    common_emoji = [
        # Tier 1: Ultra-common (billions of uses)
        {"emoji": "😂", "name": "face with tears of joy", "usage_tier": 1},
        {"emoji": "❤️", "name": "red heart", "usage_tier": 1},
        {"emoji": "🥰", "name": "smiling face with hearts", "usage_tier": 1},
        {"emoji": "😍", "name": "smiling face with heart-eyes", "usage_tier": 1},
        {"emoji": "😊", "name": "smiling face with smiling eyes", "usage_tier": 1},

        # Tier 2: Very common (hundreds of millions)
        {"emoji": "🎉", "name": "party popper", "usage_tier": 2},
        {"emoji": "😭", "name": "loudly crying face", "usage_tier": 2},
        {"emoji": "😘", "name": "face blowing a kiss", "usage_tier": 2},
        {"emoji": "🥺", "name": "pleading face", "usage_tier": 2},
        {"emoji": "🤣", "name": "rolling on the floor laughing", "usage_tier": 2},
        {"emoji": "💕", "name": "two hearts", "usage_tier": 2},
        {"emoji": "✨", "name": "sparkles", "usage_tier": 2},
        {"emoji": "🙏", "name": "folded hands", "usage_tier": 2},
        {"emoji": "😁", "name": "beaming face with smiling eyes", "usage_tier": 2},
        {"emoji": "💖", "name": "sparkling heart", "usage_tier": 2},

        # Tier 3: Common (tens of millions)
        {"emoji": "👍", "name": "thumbs up", "usage_tier": 3},
        {"emoji": "🔥", "name": "fire", "usage_tier": 3},
        {"emoji": "💪", "name": "flexed biceps", "usage_tier": 3},
        {"emoji": "🌟", "name": "glowing star", "usage_tier": 3},
        {"emoji": "😉", "name": "winking face", "usage_tier": 3},
        {"emoji": "🤗", "name": "hugging face", "usage_tier": 3},
        {"emoji": "😎", "name": "smiling face with sunglasses", "usage_tier": 3},
        {"emoji": "💯", "name": "hundred points", "usage_tier": 3},
        {"emoji": "🙌", "name": "raising hands", "usage_tier": 3},
        {"emoji": "💙", "name": "blue heart", "usage_tier": 3},

        # Tier 4: Moderately common
        {"emoji": "🤔", "name": "thinking face", "usage_tier": 4},
        {"emoji": "😌", "name": "relieved face", "usage_tier": 4},
        {"emoji": "🎊", "name": "confetti ball", "usage_tier": 4},
        {"emoji": "💜", "name": "purple heart", "usage_tier": 4},
        {"emoji": "😄", "name": "grinning face with smiling eyes", "usage_tier": 4},
        {"emoji": "🤷", "name": "person shrugging", "usage_tier": 4},
        {"emoji": "💚", "name": "green heart", "usage_tier": 4},
        {"emoji": "🎈", "name": "balloon", "usage_tier": 4},
        {"emoji": "🥳", "name": "partying face", "usage_tier": 4},
        {"emoji": "😇", "name": "smiling face with halo", "usage_tier": 4},

        # Tier 5: Regular use
        {"emoji": "🤩", "name": "star-struck", "usage_tier": 5},
        {"emoji": "😃", "name": "grinning face with big eyes", "usage_tier": 5},
        {"emoji": "🙃", "name": "upside-down face", "usage_tier": 5},
        {"emoji": "💛", "name": "yellow heart", "usage_tier": 5},
        {"emoji": "😬", "name": "grimacing face", "usage_tier": 5},
        {"emoji": "🤞", "name": "crossed fingers", "usage_tier": 5},
        {"emoji": "👏", "name": "clapping hands", "usage_tier": 5},
        {"emoji": "🥹", "name": "face holding back tears", "usage_tier": 5},
        {"emoji": "😅", "name": "grinning face with sweat", "usage_tier": 5},
        {"emoji": "👋", "name": "waving hand", "usage_tier": 5},

        # Additional distinct emoji to reach 58
        {"emoji": "🎁", "name": "wrapped gift", "usage_tier": 6},
        {"emoji": "🍀", "name": "four leaf clover", "usage_tier": 6},
        {"emoji": "🌈", "name": "rainbow", "usage_tier": 6},
        {"emoji": "⭐", "name": "star", "usage_tier": 6},
        {"emoji": "🌺", "name": "hibiscus", "usage_tier": 6},
        {"emoji": "🌸", "name": "cherry blossom", "usage_tier": 6},
        {"emoji": "🍕", "name": "pizza", "usage_tier": 6},
        {"emoji": "🍔", "name": "hamburger", "usage_tier": 6},
        {"emoji": "☕", "name": "hot beverage", "usage_tier": 6},
        {"emoji": "🎮", "name": "video game", "usage_tier": 6},
        {"emoji": "⚡", "name": "high voltage", "usage_tier": 6},
        {"emoji": "🌙", "name": "crescent moon", "usage_tier": 6},
        {"emoji": "☀️", "name": "sun", "usage_tier": 6},
        {"emoji": "🎵", "name": "musical note", "usage_tier": 6},
        {"emoji": "🎶", "name": "musical notes", "usage_tier": 6},
        {"emoji": "🌻", "name": "sunflower", "usage_tier": 6},
        {"emoji": "🐶", "name": "dog face", "usage_tier": 6},
        {"emoji": "🐱", "name": "cat face", "usage_tier": 6},
    ]

    return common_emoji


def create_steganographic_mapping(
    candidates_file='data/top_candidates.json',
    output_file='data/base58_emoji_mapping_stego.json'
) -> Dict:
    """
    Create Base58→Emoji mapping optimized for steganography

    Strategy:
    1. Most common Base58 chars (1, 3) → Most common emoji
    2. Address prefix patterns (bc, xpub, ypub, zpub) → Common emoji
    3. Balance between common usage and visual distinctiveness

    This makes addresses look like normal emoji messages.
    """

    # Load visual distinctiveness data
    with open(candidates_file, 'r', encoding='utf-8') as f:
        distinct_candidates = json.load(f)

    # Get common emoji list
    common_emoji = get_common_emoji_list()

    # Base58 alphabet
    base58_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    # Base58 character frequency (from base58_frequency.py analysis)
    # Prioritize mapping by:
    # 1. Address prefixes: 1, 3, bc (but bc is bech32, not base58)
    # 2. Key prefixes: xpub, ypub, zpub (x, y, z, p, u, b)
    # 3. High frequency: e, f, i, F, u, X, Y, H, p, J, Z, r, L, b, n, 9

    priority_order = [
        # Address prefixes (70% of addresses start with 1, 30% with 3)
        '1', '3',

        # Common in xpub/ypub/zpub prefixes
        'x', 'p', 'u', 'b', 'y', 'z',

        # High frequency in addresses
        'e', 'f', 'i', 'F', 'X', 'Y', 'H', 'J', 'Z', 'r', 'L', 'n', '9',

        # Medium frequency
        'P', 'A', 'D', 'm', 'a', 'c', 'M', 'v', 'E', '4',

        # Lower frequency
        'Q', 'S', 'N', 'o', 'W', 'q', 'K', '5', 't', 'B',

        # Least frequent
        'G', '2', 'T', 'R', 'k', '8', 's', 'g', '6', 'j',
        'C', 'w', 'd', 'V', 'h', 'U', '7',
    ]

    print("Creating steganographic mapping...")
    print()
    print("Strategy: Common Base58 chars → Common emoji")
    print("Goal: Addresses blend into normal emoji messages")
    print()

    # Filter common emoji to avoid confusables
    # From visual_similarity analysis, we know heart variants are too similar
    # Keep only ONE heart variant
    confusable_patterns = {
        'heart': ['❤️'],  # Keep only red heart
        # Other patterns can be added
    }

    filtered_common = []
    seen_patterns = {}

    for emoji_data in common_emoji:
        name = emoji_data['name']
        emoji = emoji_data['emoji']

        # Check if this emoji matches a confusable pattern
        is_confusable = False
        for pattern, allowed in confusable_patterns.items():
            if pattern in name:
                if emoji not in allowed:
                    if pattern in seen_patterns:
                        is_confusable = True
                        break
                    seen_patterns[pattern] = True

        if not is_confusable:
            filtered_common.append(emoji_data)

    print(f"Filtered common emoji: {len(common_emoji)} → {len(filtered_common)}")
    print()

    # Check if we have enough
    if len(filtered_common) < 58:
        # Add distinct emoji to fill remaining slots
        for candidate in distinct_candidates:
            if len(filtered_common) >= 58:
                break

            # Check if already in list
            if candidate['emoji'] not in [e['emoji'] for e in filtered_common]:
                filtered_common.append({
                    'emoji': candidate['emoji'],
                    'name': candidate['name'],
                    'usage_tier': 7,  # Lower priority
                    'distinctiveness': candidate['distinctiveness']
                })

    # Create mapping
    mapping = {}

    for i, char in enumerate(priority_order[:58]):
        if i < len(filtered_common):
            emoji_data = filtered_common[i]
            mapping[char] = {
                'emoji': emoji_data['emoji'],
                'name': emoji_data['name'],
                'usage_tier': emoji_data.get('usage_tier', 7),
                'priority': i + 1
            }

    # Save mapping
    output = {
        'base58_alphabet': base58_alphabet,
        'mapping_strategy': 'steganographic',
        'description': 'Common Base58 characters mapped to common emoji for hiding addresses in text',
        'mapping': mapping,
        'priority_order': priority_order[:58],
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Steganographic mapping saved to: {output_file}")
    print()

    # Print summary
    print("=" * 80)
    print("TOP 20 STEGANOGRAPHIC MAPPINGS")
    print("=" * 80)
    print(f"{'Base58':<8} {'Emoji':<6} {'Name':<40} {'Tier':<6}")
    print("-" * 80)

    for i, char in enumerate(priority_order[:20]):
        if char in mapping:
            m = mapping[char]
            tier = m.get('usage_tier', 'N/A')
            print(f"{char:<8} {m['emoji']:<6} {m['name']:<40} {tier:<6}")

    print()
    print("Tier 1-2: Ultra-common emoji (billions of uses)")
    print("Tier 3-4: Common emoji (millions of uses)")
    print("Tier 5+:   Regular emoji")
    print()

    return mapping


def main():
    """Generate steganographic mapping"""
    print("=" * 80)
    print("STEGANOGRAPHIC EMOJI MAPPING GENERATOR")
    print("=" * 80)
    print()

    mapping = create_steganographic_mapping()

    print("=" * 80)
    print("EXAMPLE ENCODING")
    print("=" * 80)
    print()

    example_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    encoded = ""

    for char in example_address:
        if char in mapping:
            encoded += mapping[char]['emoji']
        else:
            encoded += "❓"

    print(f"Address: {example_address}")
    print(f"Encoded: {encoded}")
    print()
    print("Notice: The encoded address uses common emoji that blend naturally")
    print("into messaging (hearts, smiles, celebration), unlike distinct emoji")
    print("which would stand out.")
    print()


if __name__ == '__main__':
    main()
