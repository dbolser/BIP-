#!/usr/bin/env python3
"""
BIP-😸 Reference Implementation: Emoji Address Codec

Encoder/decoder for Bitcoin addresses using emoji representation.
Implements 1:1 Base58 character mapping with validation.

Usage:
    python emoji_codec.py encode 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    python emoji_codec.py decode "🧔🤶🧔🐞🥝..."
    python emoji_codec.py scan "🧔🤶🧔🐞🥝..."  # with validation
"""

import json
import hashlib
import sys
from typing import Optional, Tuple, Dict


class EmojiCodec:
    """Encode and decode Bitcoin addresses to/from emoji"""

    def __init__(self, mapping_file='data/base58_emoji_mapping.json'):
        """Initialize codec with Base58→Emoji mapping"""

        # Load mapping
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.base58_alphabet = data['base58_alphabet']
        self.mapping = data['mapping']

        # Create reverse mapping (emoji → Base58)
        self.reverse_mapping = {}
        for base58_char, emoji_data in self.mapping.items():
            emoji = emoji_data['emoji']
            self.reverse_mapping[emoji] = base58_char

        print(f"✅ Loaded mapping: {len(self.mapping)} Base58 chars → {len(self.reverse_mapping)} emoji")

    def encode(self, base58_address: str) -> Tuple[str, bool]:
        """
        Encode Base58 address to emoji

        Returns:
            (emoji_address, success)
        """
        emoji_address = ""
        unknown_chars = []

        for char in base58_address:
            if char in self.mapping:
                emoji_address += self.mapping[char]['emoji']
            else:
                # Unknown character (not in Base58 alphabet)
                emoji_address += "❓"
                unknown_chars.append(char)

        success = len(unknown_chars) == 0

        if not success:
            print(f"⚠️  Warning: Unknown characters found: {unknown_chars}")

        return emoji_address, success

    def decode(self, emoji_address: str) -> Tuple[str, bool]:
        """
        Decode emoji address to Base58

        Returns:
            (base58_address, success)
        """
        base58_address = ""
        unknown_emoji = []

        # Split emoji string into individual emoji
        # (Some emoji are multi-codepoint, so we need to be careful)
        emoji_list = self._split_emoji(emoji_address)

        for emoji in emoji_list:
            if emoji in self.reverse_mapping:
                base58_address += self.reverse_mapping[emoji]
            else:
                # Unknown emoji
                base58_address += "?"
                unknown_emoji.append(emoji)

        success = len(unknown_emoji) == 0

        if not success:
            print(f"⚠️  Warning: Unknown emoji found: {unknown_emoji}")

        return base58_address, success

    def _split_emoji(self, emoji_string: str) -> list:
        """
        Split emoji string into individual emoji characters

        This handles multi-codepoint emoji correctly.
        """
        emoji_list = []
        i = 0

        while i < len(emoji_string):
            # Start with current character
            emoji = emoji_string[i]
            i += 1

            # Check for variation selectors (U+FE0F, U+FE0E)
            while i < len(emoji_string) and emoji_string[i] in ['\uFE0F', '\uFE0E']:
                emoji += emoji_string[i]
                i += 1

            # Check for skin tone modifiers (U+1F3FB - U+1F3FF)
            while i < len(emoji_string) and '\U0001F3FB' <= emoji_string[i] <= '\U0001F3FF':
                emoji += emoji_string[i]
                i += 1

            # Check for ZWJ sequences (U+200D)
            while i < len(emoji_string) and emoji_string[i] == '\u200D':
                # ZWJ followed by another emoji
                emoji += emoji_string[i]  # ZWJ
                i += 1
                if i < len(emoji_string):
                    emoji += emoji_string[i]  # Next character
                    i += 1

            emoji_list.append(emoji)

        return emoji_list

    def validate_base58check(self, address: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Base58Check encoding (Bitcoin address checksum)

        Returns:
            (is_valid, error_message)
        """
        # Check if all characters are valid Base58
        for char in address:
            if char not in self.base58_alphabet:
                return False, f"Invalid character '{char}' (not in Base58 alphabet)"

        # Decode Base58
        try:
            decoded = self._base58_decode(address)
        except Exception as e:
            return False, f"Base58 decode error: {e}"

        # Must be at least 5 bytes (1 version + 4 checksum)
        if len(decoded) < 5:
            return False, f"Address too short: {len(decoded)} bytes"

        # Split payload and checksum
        payload = decoded[:-4]
        checksum = decoded[-4:]

        # Calculate expected checksum
        hash_result = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
        expected_checksum = hash_result[:4]

        # Validate
        if checksum != expected_checksum:
            return False, f"Checksum mismatch (expected {expected_checksum.hex()}, got {checksum.hex()})"

        return True, None

    def _base58_decode(self, address: str) -> bytes:
        """Decode Base58 string to bytes"""
        decoded = 0

        for char in address:
            decoded = decoded * 58 + self.base58_alphabet.index(char)

        # Convert to bytes
        result = decoded.to_bytes((decoded.bit_length() + 7) // 8, byteorder='big')

        # Handle leading zeros (represented as '1' in Base58)
        num_leading_ones = len(address) - len(address.lstrip('1'))
        result = b'\x00' * num_leading_ones + result

        return result

    def scan(self, emoji_address: str, validate: bool = True) -> Dict:
        """
        Scan and validate emoji address

        Returns:
            {
                'emoji': str,
                'base58': str,
                'decode_success': bool,
                'checksum_valid': bool,
                'errors': list,
            }
        """
        result = {
            'emoji': emoji_address,
            'base58': None,
            'decode_success': False,
            'checksum_valid': False,
            'errors': [],
        }

        # Decode
        base58_address, decode_success = self.decode(emoji_address)
        result['base58'] = base58_address
        result['decode_success'] = decode_success

        if not decode_success:
            result['errors'].append("Failed to decode emoji address")
            return result

        # Validate checksum
        if validate:
            is_valid, error_msg = self.validate_base58check(base58_address)
            result['checksum_valid'] = is_valid

            if not is_valid:
                result['errors'].append(f"Checksum validation failed: {error_msg}")
            else:
                result['errors'].append("✓ Checksum valid")

        return result


def print_banner():
    """Print application banner"""
    print()
    print("=" * 70)
    print("  BIP-😸 EMOJI ADDRESS CODEC")
    print("  Reference Implementation v0.1.0")
    print("=" * 70)
    print()


def cmd_encode(codec: EmojiCodec, base58_address: str):
    """Encode command"""
    print(f"📝 Encoding Base58 address...")
    print(f"   Input: {base58_address}")
    print()

    # Validate input first
    is_valid, error = codec.validate_base58check(base58_address)
    if not is_valid:
        print(f"⚠️  Warning: Invalid Base58Check address")
        print(f"   Error: {error}")
        print()

    # Encode
    emoji_address, success = codec.encode(base58_address)

    if success:
        print(f"✅ Encoding successful!")
    else:
        print(f"⚠️  Encoding completed with warnings")

    print()
    print(f"   Base58: {base58_address}")
    print(f"   Emoji:  {emoji_address}")
    print()

    # Show character-by-character mapping
    print("   Character mapping:")
    emoji_list = list(codec._split_emoji(emoji_address))
    for i, char in enumerate(base58_address[:20]):  # Show first 20
        if i < len(emoji_list):
            if char in codec.mapping:
                name = codec.mapping[char]['name']
                print(f"     {char} → {emoji_list[i]}  ({name})")
            else:
                print(f"     {char} → {emoji_list[i]}  (unknown)")

    if len(base58_address) > 20:
        print(f"     ... ({len(base58_address) - 20} more characters)")

    print()


def cmd_decode(codec: EmojiCodec, emoji_address: str):
    """Decode command"""
    print(f"🔍 Decoding emoji address...")
    print(f"   Input: {emoji_address}")
    print()

    # Decode
    base58_address, success = codec.decode(emoji_address)

    if success:
        print(f"✅ Decoding successful!")
    else:
        print(f"⚠️  Decoding completed with warnings")

    print()
    print(f"   Emoji:  {emoji_address}")
    print(f"   Base58: {base58_address}")
    print()


def cmd_scan(codec: EmojiCodec, emoji_address: str):
    """Scan and validate command"""
    print(f"🔎 Scanning emoji address with validation...")
    print(f"   Input: {emoji_address}")
    print()

    # Scan
    result = codec.scan(emoji_address, validate=True)

    print("=" * 70)
    print("SCAN RESULTS")
    print("=" * 70)
    print()
    print(f"Emoji Address:  {result['emoji']}")
    print(f"Base58 Address: {result['base58']}")
    print()
    print(f"Decode Success: {'✅ Yes' if result['decode_success'] else '❌ No'}")
    print(f"Checksum Valid: {'✅ Yes' if result['checksum_valid'] else '❌ No'}")
    print()

    if result['errors']:
        print("Messages:")
        for error in result['errors']:
            print(f"  • {error}")
        print()

    print("=" * 70)
    print()


def main():
    """Main CLI interface"""
    print_banner()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python emoji_codec.py encode <base58_address>")
        print("  python emoji_codec.py decode <emoji_address>")
        print("  python emoji_codec.py scan <emoji_address>")
        print()
        print("Examples:")
        print("  python emoji_codec.py encode 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        print("  python emoji_codec.py decode '🧔🤶🧔🐞🥝...'")
        print("  python emoji_codec.py scan '🧔🤶🧔🐞🥝...'")
        print()
        sys.exit(1)

    # Initialize codec
    codec = EmojiCodec()
    print()

    command = sys.argv[1].lower()

    if command == 'encode':
        if len(sys.argv) < 3:
            print("❌ Error: Missing Base58 address")
            sys.exit(1)

        base58_address = sys.argv[2]
        cmd_encode(codec, base58_address)

    elif command == 'decode':
        if len(sys.argv) < 3:
            print("❌ Error: Missing emoji address")
            sys.exit(1)

        emoji_address = sys.argv[2]
        cmd_decode(codec, emoji_address)

    elif command == 'scan':
        if len(sys.argv) < 3:
            print("❌ Error: Missing emoji address")
            sys.exit(1)

        emoji_address = sys.argv[2]
        cmd_scan(codec, emoji_address)

    else:
        print(f"❌ Error: Unknown command '{command}'")
        print("   Valid commands: encode, decode, scan")
        sys.exit(1)


if __name__ == '__main__':
    main()
