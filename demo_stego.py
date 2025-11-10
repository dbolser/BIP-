#!/usr/bin/env python3
"""
BIP-😸 Steganographic Demo

Demonstrates hiding Bitcoin addresses in normal-looking emoji messages
using common emoji mapping.
"""

from emoji_codec import EmojiCodec


def print_header(title):
    """Print section header"""
    print()
    print("=" * 80)
    print(f"  {title}")
    print("=" * 80)
    print()


def demo_steganographic_encoding():
    """Demo steganographic encoding vs distinct encoding"""
    print_header("DEMO 1: Steganographic vs Distinct Encoding")

    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

    # Distinct mapping
    codec_distinct = EmojiCodec('data/base58_emoji_mapping.json', verbose=False)
    distinct_emoji, _ = codec_distinct.encode(address)

    # Steganographic mapping
    codec_stego = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)
    stego_emoji, _ = codec_stego.encode(address)

    print(f"Address: {address}")
    print()
    print("DISTINCT ENCODING (visually unique):")
    print(f"  {distinct_emoji}")
    print(f"  Notice: Unusual emoji like 🧔🫅🕸️🦪 stand out as suspicious")
    print()
    print("STEGANOGRAPHIC ENCODING (common emoji):")
    print(f"  {stego_emoji}")
    print(f"  Notice: Common emoji like 😂😌🤣✨ blend into normal messages")
    print()


def demo_hiding_in_messages():
    """Demo hiding addresses in normal text messages"""
    print_header("DEMO 2: Hiding Addresses in Messages")

    codec = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)

    # Encode Satoshi's address
    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    emoji_addr, _ = codec.encode(address)

    # Split emoji into natural-looking chunks
    chunks = [
        emoji_addr[:5],
        emoji_addr[5:13],
        emoji_addr[13:23],
        emoji_addr[23:],
    ]

    # Create a natural-looking message
    messages = [
        f"Hey! {chunks[0]} How are you doing today?",
        f"That's great to hear! {chunks[1]} What are your plans for the weekend?",
        f"Sounds fun! {chunks[2]} Let me know if you want to hang out!",
        f"Talk to you later! {chunks[3]} Have a great day!",
    ]

    print("CONVERSATION WITH HIDDEN ADDRESS:")
    print("-" * 80)
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg}")
    print("-" * 80)
    print()
    print("Notice: The emoji look natural in conversation context.")
    print("No one would suspect they encode a Bitcoin address!")
    print()


def demo_extracting_from_conversation():
    """Demo extracting address from conversation"""
    print_header("DEMO 3: Extracting Address from Conversation")

    codec = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)

    # Create conversation with embedded address
    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    emoji_addr, _ = codec.encode(address)

    # Natural message with embedded address
    message = f"Hey friend! 😂😌😂🥺🤔 hope all is well with you! 😂🤣🤔🎁🙃⭐🤣✨ Let's catch up soon 🙏🌺🎊🥳🤔🌸✨🌸😎🎁😬😎😄😇🍊🎊🙏😇✨🤞🤷 and grab coffee!"

    print("RECEIVED MESSAGE:")
    print(f"  {message}")
    print()

    # Extract address
    results = codec.extract_from_text(message, validate=True)
    result = results[0]

    print("EXTRACTION ANALYSIS:")
    print(f"  Extracted emoji: {result['extracted_emoji']}")
    print(f"  Decoded address: {result['base58']}")
    print(f"  Checksum valid:  {'✅ Yes' if result['checksum_valid'] else '❌ No'}")
    print()
    print("The codec successfully extracted the hidden address!")
    print()


def demo_address_type_prefixes():
    """Demo how different address types use different common emoji"""
    print_header("DEMO 4: Address Type Prefixes")

    codec = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)

    addresses = [
        ("P2PKH (1)", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
        ("P2PKH (1)", "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"),
        ("P2SH  (3)", "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy"),
        ("P2SH  (3)", "3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC"),
    ]

    print("Address prefixes use ultra-common emoji:")
    print()

    for addr_type, addr in addresses:
        emoji_addr, _ = codec.encode(addr)
        prefix_emoji = emoji_addr[:3]
        print(f"{addr_type}: {addr[:10]}... → {prefix_emoji}...")

    print()
    print("Observation:")
    print("  1 → 😂 (tears of joy) - Most common emoji worldwide")
    print("  3 → ❤️ (red heart) - Second most common emoji")
    print()
    print("These prefixes blend perfectly into casual messaging!")
    print()


def demo_security_through_obscurity():
    """Demo security through obscurity concept"""
    print_header("DEMO 5: Security Through Obscurity")

    codec = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)

    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    emoji_addr, _ = codec.encode(address)

    print("STEGANOGRAPHIC PROPERTIES:")
    print()
    print("1. Casual Observer:")
    print(f"   Sees: {emoji_addr}")
    print("   Thinks: Just a friendly emoji message 😊")
    print()
    print("2. Pattern Recognition:")
    print("   Common emoji usage makes it blend with normal text")
    print("   No obvious structure or unusual character sequences")
    print()
    print("3. Statistical Analysis:")
    print("   Emoji frequency matches typical social media usage")
    print("   😂❤️🤣✨🙏 are among top 10 most-used emoji globally")
    print()
    print("4. Use Cases:")
    print("   • Embedding addresses in public social media posts")
    print("   • Messaging apps that scan for crypto addresses")
    print("   • Sharing addresses in hostile environments")
    print()
    print("⚠️  WARNING: This is obscurity, NOT encryption!")
    print("   Anyone with the mapping can decode the address.")
    print("   For true privacy, use proper encryption.")
    print()


def demo_character_frequency():
    """Demo character frequency comparison"""
    print_header("DEMO 6: Character Frequency Analysis")

    codec_distinct = EmojiCodec('data/base58_emoji_mapping.json', verbose=False)
    codec_stego = EmojiCodec('data/base58_emoji_mapping_stego.json', verbose=False)

    print("MAPPING STRATEGY COMPARISON:")
    print()

    # Show first 10 characters
    base58_chars = ['1', '3', 'e', 'f', 'i', 'p', 'u', 'b', 'x', 'y']

    print(f"{'Char':<6} {'Distinct Mapping':<30} {'Steganographic Mapping':<30}")
    print("-" * 80)

    for char in base58_chars:
        distinct = codec_distinct.mapping[char]
        stego = codec_stego.mapping[char]

        distinct_emoji = f"{distinct['emoji']} ({distinct['name'][:20]})"
        stego_emoji = f"{stego['emoji']} ({stego['name'][:20]})"

        print(f"'{char}'    {distinct_emoji:<30} {stego_emoji:<30}")

    print()
    print("Notice: Distinct mapping uses unique emoji (🧔🍊🫅)")
    print("        Steganographic uses common emoji (😂❤️🤣)")
    print()


def main():
    """Run all steganographic demos"""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  BIP-😸 STEGANOGRAPHIC ENCODING DEMO".center(78) + "║")
    print("║" + "  Hiding Bitcoin Addresses in Plain Sight".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    demo_steganographic_encoding()
    demo_hiding_in_messages()
    demo_extracting_from_conversation()
    demo_address_type_prefixes()
    demo_security_through_obscurity()
    demo_character_frequency()

    print()
    print("=" * 80)
    print("  Demo complete! Try it yourself:")
    print("=" * 80)
    print()
    print("  Encode with steganography:")
    print("    python emoji_codec.py encode <address> --stego")
    print()
    print("  Extract from text:")
    print("    python emoji_codec.py extract '<text_with_emoji>' --stego")
    print()
    print("  Example:")
    print("    python emoji_codec.py encode 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa --stego")
    print("    python emoji_codec.py extract 'Hey! 😂😌😂 how are you?' --stego")
    print()


if __name__ == '__main__':
    main()
