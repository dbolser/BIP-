#!/usr/bin/env python3
"""
BIP-😸 Interactive Demo

Demonstrates the emoji codec with real Bitcoin addresses
"""

from emoji_codec import EmojiCodec


def print_header(title):
    """Print section header"""
    print()
    print("=" * 80)
    print(f"  {title}")
    print("=" * 80)
    print()


def demo_encode_decode():
    """Demo basic encoding and decoding"""
    print_header("DEMO 1: Encoding and Decoding")

    codec = EmojiCodec()

    # Test addresses
    addresses = [
        ("Satoshi's Address (Genesis Block)", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
        ("P2PKH Address", "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"),
        ("Coinbase Address", "1CounterpartyXXXXXXXXXXXXXXXUWLpVr"),
    ]

    for label, address in addresses:
        print(f"📍 {label}")
        print(f"   Base58: {address}")

        # Encode
        emoji_address, _ = codec.encode(address)
        print(f"   Emoji:  {emoji_address}")

        # Decode back
        decoded_address, _ = codec.decode(emoji_address)
        print(f"   Verify: {decoded_address}")

        # Check round-trip
        if decoded_address == address:
            print(f"   ✅ Round-trip successful!")
        else:
            print(f"   ❌ Round-trip failed!")

        print()


def demo_validation():
    """Demo checksum validation"""
    print_header("DEMO 2: Checksum Validation")

    codec = EmojiCodec()

    print("✅ Valid Address:")
    valid_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    is_valid, error = codec.validate_base58check(valid_address)
    print(f"   Address: {valid_address}")
    print(f"   Valid:   {is_valid}")
    print(f"   Error:   {error}")
    print()

    print("❌ Invalid Address (bad checksum):")
    invalid_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNb"  # Changed last char
    is_valid, error = codec.validate_base58check(invalid_address)
    print(f"   Address: {invalid_address}")
    print(f"   Valid:   {is_valid}")
    print(f"   Error:   {error}")
    print()


def demo_visual_distinction():
    """Demo visual distinction of prefixes"""
    print_header("DEMO 3: Visual Distinction of Address Prefixes")

    codec = EmojiCodec()

    print("Notice how P2PKH (1...) and P2SH (3...) addresses have distinct prefixes:")
    print()

    # P2PKH addresses (start with 1)
    p2pkh_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        "1CounterpartyXXXXXXXXXXXXXXXUWLpVr",
    ]

    print("P2PKH Addresses (legacy, start with '1' → 🧔):")
    for addr in p2pkh_addresses:
        emoji_addr, _ = codec.encode(addr)
        print(f"   {emoji_addr[:10]}... ← {addr[:10]}...")
    print()

    # P2SH addresses (start with 3)
    p2sh_addresses = [
        "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy",
        "3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC",
        "3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v",
    ]

    print("P2SH Addresses (script, start with '3' → 🍊):")
    for addr in p2sh_addresses:
        emoji_addr, _ = codec.encode(addr)
        print(f"   {emoji_addr[:10]}... ← {addr[:10]}...")
    print()

    print("Key Observation:")
    print("   🧔 = P2PKH (person: beard)")
    print("   🍊 = P2SH (tangerine)")
    print("   → Instantly recognizable address types!")
    print()


def demo_character_mapping():
    """Demo character-by-character mapping"""
    print_header("DEMO 4: Character-by-Character Mapping")

    codec = EmojiCodec()

    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    emoji_address, _ = codec.encode(address)

    print(f"Address: {address}")
    print(f"Emoji:   {emoji_address}")
    print()

    print("Mapping breakdown:")
    emoji_list = list(codec._split_emoji(emoji_address))

    for i, char in enumerate(address):
        if i < len(emoji_list):
            emoji = emoji_list[i]
            name = codec.mapping[char]['name']
            score = codec.mapping[char]['distinctiveness']
            print(f"  [{i+1:2d}] {char} → {emoji}  ({name}, distinctiveness: {score:.3f})")

    print()


def demo_error_handling():
    """Demo error handling"""
    print_header("DEMO 5: Error Handling")

    codec = EmojiCodec()

    print("❌ Decoding with invalid emoji:")
    invalid_emoji = "🧔🤶🧔❤️🥝🧔"  # ❤️ not in mapping
    decoded, success = codec.decode(invalid_emoji)
    print(f"   Input:   {invalid_emoji}")
    print(f"   Output:  {decoded}")
    print(f"   Success: {success}")
    print()

    print("❌ Encoding with invalid Base58 character:")
    invalid_base58 = "1A1zP1eP5QGefi2DMPT0TL5SLmv7DivfNa"  # Contains '0' (not in Base58)
    encoded, success = codec.encode(invalid_base58)
    print(f"   Input:   {invalid_base58}")
    print(f"   Output:  {encoded}")
    print(f"   Success: {success}")
    print()


def demo_statistics():
    """Demo mapping statistics"""
    print_header("DEMO 6: Mapping Statistics")

    codec = EmojiCodec()

    # Count emoji categories
    categories = {
        'people': 0,
        'hands': 0,
        'food': 0,
        'animals': 0,
        'objects': 0,
    }

    for base58_char, emoji_data in codec.mapping.items():
        name = emoji_data['name'].lower()

        if any(word in name for word in ['face', 'person', 'man', 'woman', 'child', 'boy', 'girl', 'baby', 'beard', 'prince', 'princess', 'claus']):
            categories['people'] += 1
        elif any(word in name for word in ['hand', 'fist', 'finger', 'palm', 'clap']):
            categories['hands'] += 1
        elif any(word in name for word in ['fruit', 'apple', 'pear', 'peach', 'melon', 'kiwi', 'orange', 'tangerine', 'pepper', 'plant', 'tree', 'flower', 'leaf', 'blossom']):
            categories['food'] += 1
        elif any(word in name for word in ['animal', 'dog', 'cat', 'monkey', 'beetle', 'hedgehog', 'chick', 'oyster', 'ladybug']):
            categories['animals'] += 1
        else:
            categories['objects'] += 1

    print("Emoji Category Distribution:")
    total = len(codec.mapping)
    for category, count in categories.items():
        percentage = (count / total) * 100
        bar = "█" * (count // 2)
        print(f"   {category:10s}: {bar} {count:2d} ({percentage:5.1f}%)")

    print()
    print(f"Total emoji: {total}")
    print(f"Base58 alphabet size: {len(codec.base58_alphabet)}")
    print()


def main():
    """Run all demos"""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  BIP-😸 EMOJI ADDRESS CODEC - INTERACTIVE DEMO".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    demo_encode_decode()
    demo_validation()
    demo_visual_distinction()
    demo_character_mapping()
    demo_error_handling()
    demo_statistics()

    print()
    print("=" * 80)
    print("  Demo complete! Try it yourself:")
    print("=" * 80)
    print()
    print("  Encode:  python emoji_codec.py encode <base58_address>")
    print("  Decode:  python emoji_codec.py decode <emoji_address>")
    print("  Scan:    python emoji_codec.py scan <emoji_address>")
    print()


if __name__ == '__main__':
    main()
