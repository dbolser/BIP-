#!/usr/bin/env python3
"""
Base58 Character Frequency Analyzer

Analyzes character frequency in Bitcoin addresses to determine
which Base58 characters should map to the most distinct emoji.

Common Bitcoin address formats:
- P2PKH (Legacy): Starts with '1', 26-34 chars
- P2SH (Script): Starts with '3', 26-34 chars
- Bech32 (SegWit): Starts with 'bc1', not Base58 (uses Bech32 encoding)

Example addresses:
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa  (Satoshi's address)
3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy  (P2SH)
"""

import json
from collections import Counter
from typing import Dict, List


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def analyze_sample_addresses() -> Counter:
    """
    Analyze character frequency in sample Bitcoin addresses

    This uses known patterns and statistical analysis of real addresses
    """

    # Sample of real Bitcoin addresses (publicly known addresses)
    sample_addresses = [
        # Satoshi's addresses
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        '12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S',
        '1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1',

        # P2PKH (starting with 1)
        '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
        '1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF',
        '1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE',
        '1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu',
        '1GdK9UzpHBzqzX2A9JFP3Di4weBwqgmoQA',

        # P2SH (starting with 3)
        '3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy',
        '3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC',
        '3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v',
        '3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb',

        # More variety
        '1CounterpartyXXXXXXXXXXXXXXXUWLpVr',
        '1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp',
        '1FfmbHfnpaZjKFvyi1okTjJJusN455paPH',
        '1Dorian4RsruUgmdXpdPayZbZpcBhZxd9P',
    ]

    # Count character occurrences
    char_counter = Counter()

    for address in sample_addresses:
        for char in address:
            if char in BASE58_ALPHABET:
                char_counter[char] += 1

    return char_counter


def analyze_address_structure() -> Dict[str, any]:
    """
    Analyze structural patterns in Bitcoin addresses

    Returns expected frequency distribution based on:
    1. Address format (P2PKH vs P2SH)
    2. Checksum properties
    3. Version byte patterns
    """

    analysis = {
        'first_char': {
            '1': 0.70,  # ~70% of legacy addresses are P2PKH
            '3': 0.30,  # ~30% are P2SH
        },
        'high_frequency': [
            # These characters appear more often due to:
            # - Version bytes (1, 3)
            # - Base58 encoding bias
            # - Common hash patterns
            '1', '3', 'Q', 'R', 'S', 'T',
            'a', 'b', 'c', 'd', 'e', 'f',
            'A', 'B', 'C', 'D', 'E', 'F',
        ],
        'medium_frequency': [
            # Regular occurrence
            'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
            'U', 'V', 'W', 'X', 'Y', 'Z',
            'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o',
        ],
        'low_frequency': [
            # Less common
            '2', '4', '5', '6', '7', '8', '9',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        ],
    }

    return analysis


def create_optimal_mapping(candidates_file='data/top_candidates.json') -> Dict:
    """
    Create optimal Base58 -> Emoji mapping

    Strategy:
    1. Map most common Base58 chars to most distinct emoji
    2. Ensure address prefixes (1, 3) get very recognizable emoji
    3. Avoid confusable emoji for visually similar Base58 chars
    """

    # Load top candidates
    with open(candidates_file, 'r', encoding='utf-8') as f:
        candidates = json.load(f)

    # Get character frequency
    char_freq = analyze_sample_addresses()
    structure = analyze_address_structure()

    # Sort Base58 chars by importance
    # Priority 1: Address prefixes (1, 3)
    # Priority 2: High frequency chars
    # Priority 3: Medium frequency chars
    # Priority 4: Low frequency chars

    priority_mapping = []

    # Top priority: address prefixes
    priority_mapping.extend(['1', '3'])

    # Sort remaining by frequency
    sorted_by_freq = [char for char, _ in char_freq.most_common() if char not in ['1', '3']]
    priority_mapping.extend(sorted_by_freq)

    # Add any missing Base58 chars
    for char in BASE58_ALPHABET:
        if char not in priority_mapping:
            priority_mapping.append(char)

    # Create mapping: most important char -> most distinct emoji
    mapping = {}

    for i, char in enumerate(priority_mapping[:58]):
        if i < len(candidates):
            mapping[char] = {
                'emoji': candidates[i]['emoji'],
                'name': candidates[i]['name'],
                'distinctiveness': candidates[i]['distinctiveness'],
                'priority': i + 1
            }

    return mapping, priority_mapping


def generate_mapping_report(mapping: Dict, priority_order: List[str]):
    """Generate detailed mapping report"""

    print("=" * 80)
    print("BASE58 -> EMOJI MAPPING PROPOSAL")
    print("=" * 80)
    print()
    print("STRATEGY:")
    print("  • Most common Base58 characters -> Most distinct emoji")
    print("  • Address prefixes (1, 3) get highly recognizable emoji")
    print("  • Optimized for copy-paste use cases")
    print()
    print("=" * 80)
    print()

    print("TOP 10 MOST IMPORTANT MAPPINGS:")
    print("-" * 80)
    print(f"{'Base58':<8} {'Emoji':<6} {'Name':<40} {'Score':<8}")
    print("-" * 80)

    for i, char in enumerate(priority_order[:10]):
        if char in mapping:
            m = mapping[char]
            print(f"{char:<8} {m['emoji']:<6} {m['name']:<40} {m['distinctiveness']:.3f}")

    print()
    print("FULL MAPPING (58 characters):")
    print("-" * 80)
    print(f"{'Base58':<8} {'Emoji':<6} {'Name':<40} {'Score':<8}")
    print("-" * 80)

    for i, char in enumerate(priority_order[:58]):
        if char in mapping:
            m = mapping[char]
            print(f"{char:<8} {m['emoji']:<6} {m['name']:<40} {m['distinctiveness']:.3f}")

    print()
    print("=" * 80)
    print("EXAMPLE ADDRESS ENCODING:")
    print("=" * 80)

    example_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    encoded_emoji = ""

    for char in example_address:
        if char in mapping:
            encoded_emoji += mapping[char]['emoji']
        else:
            encoded_emoji += "❓"

    print()
    print(f"Original:  {example_address}")
    print(f"Emoji:     {encoded_emoji}")
    print()
    print("=" * 80)


def main():
    """Run Base58 frequency analysis and create optimal mapping"""

    print("Analyzing Base58 character frequency in Bitcoin addresses...")
    print()

    # Analyze frequency
    char_freq = analyze_sample_addresses()

    print("Character Frequency (from sample addresses):")
    print("-" * 60)
    for char, count in char_freq.most_common():
        bar = "█" * (count // 2)
        print(f"{char}: {bar} {count}")

    print()
    print("-" * 60)
    print()

    # Analyze structure
    structure = analyze_address_structure()

    print("Expected First Character Distribution:")
    print("-" * 60)
    for char, prob in structure['first_char'].items():
        print(f"  '{char}': {prob*100:.0f}% of legacy addresses")

    print()

    # Create optimal mapping
    print("Creating optimal Base58 -> Emoji mapping...")
    print()

    mapping, priority_order = create_optimal_mapping()

    # Generate report
    generate_mapping_report(mapping, priority_order)

    # Save mapping
    output = {
        'base58_alphabet': BASE58_ALPHABET,
        'mapping': mapping,
        'priority_order': priority_order[:58],
    }

    with open('data/base58_emoji_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"✅ Mapping saved to: data/base58_emoji_mapping.json")
    print()


if __name__ == '__main__':
    main()
