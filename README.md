# BIP-😸: Emoji Address Encoding

BIP-😸 is an **informational BIP** that explores encoding Bitcoin addresses as strings of emoji. The proposal maps Bitcoin's Base58 character set to 58 carefully selected emoji characters, creating a novel visual representation of addresses.

## 📋 Project Status

**Phase**: Visual Analysis Complete ✅
**Type**: Informational BIP (Educational/Exploratory)
**Goal**: Investigate feasibility and document challenges of emoji-based address encoding

### Recent Achievements

✅ Analyzed 3,781 emoji from Unicode 16.0
✅ Selected 58 most visually distinct emoji (distinctiveness: 0.356-0.382)
✅ Identified 127 confusable pairs to avoid
✅ Created optimized Base58→Emoji mapping
✅ Built reference encoder/decoder with Base58Check validation
✅ Validated with real Bitcoin addresses

**Next:** Cross-platform rendering validation

## 📚 Documentation

- **[EMOJI_SELECTION_REPORT.md](EMOJI_SELECTION_REPORT.md)** - Visual similarity analysis and final emoji selection
- **[TODO.md](TODO.md)** - Comprehensive task breakdown with 8 development phases
- **[BIP_REVIEW.md](BIP_REVIEW.md)** - Detailed analysis of strengths, weaknesses, and challenges

### Key Files

- **`emoji_codec.py`** - Reference encoder/decoder implementation
- **`demo.py`** - Interactive demonstration of all features
- **`visual_similarity.py`** - Perceptual hash-based similarity analyzer
- **`base58_frequency.py`** - Character frequency analyzer for optimal mapping
- **`data/base58_emoji_mapping.json`** - Final Base58→Emoji mapping table

## 🎯 Core Concept

Map Bitcoin Base58 characters (58 total) to 58 distinct emoji:
```
Base58: 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
Emoji:  🏠🚗💰🎉🌟... (58 visually distinct emoji)
```

**Example** (Satoshi's address from Genesis Block):
- Standard: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
- Emoji: `🧔🤶🧔🐞🥝🧔🫅🥝🤚🦪🍁🫅🤴🕸️🤫🍎🍏🥝🌸🤴🌸🍈🤚🫑🍈👱👦👊🍎🕸️👦🤴😶🐣`

## 🔬 Research Phases

### Phase 1: Data Collection
1. Scrape emoji images from [Unicode Emoji List](https://unicode.org/emoji/charts/full-emoji-list.html)
2. Parse platform-specific renderings (Apple, Google, Windows, etc.)
3. Save images as `cldr_short_name-platform.png`
4. Build comprehensive emoji dataset with metadata

### Phase 2: Visual Analysis
4. Apply image transformations using Keras/TensorFlow
5. Train classification model to identify emoji across platforms
6. Generate confusion matrix to detect similar-looking emoji

### Phase 3: Emoji Selection
6. Identify 58 robustly classified emoji with >95% cross-platform accuracy
7. Create Base58 mapping table prioritizing visual distinctiveness

### Phase 4: Implementation
8. Develop encoder/decoder libraries in multiple languages
9. Add comprehensive tests and validation

See **[TODO.md](TODO.md)** for complete task breakdown.

## ⚠️ Key Challenges

1. **Cross-Platform Rendering** - Emoji appear differently on iOS vs Android vs Windows
2. **Visual Similarity** - Many emoji look alike, creating security risks
3. **Input Difficulty** - Typing emoji sequences is cumbersome
4. **Accessibility** - Screen readers handle emoji inconsistently
5. **Security** - Potential for phishing attacks using similar emoji

See **[BIP_REVIEW.md](BIP_REVIEW.md)** for detailed analysis.

## 🎓 Educational Value

While emoji addresses face significant practical challenges for production use, this project offers valuable insights into:
- Bitcoin address encoding principles
- Base58 vs other encoding schemes
- Cross-platform compatibility challenges
- Security considerations in address representation
- UX tradeoffs in cryptocurrency design

## 📖 Technical Notes

### Emoji Classification vs OCR
**Decision**: Use classification approach
- Controlled emoji set makes classification more appropriate
- OCR would be unnecessarily complex
- Focus on identifying most reliably rendered emoji

### Platform Compatibility
Target platforms for consistency testing:
- iOS (iPhone/iPad)
- Android (various vendors)
- Windows 10/11
- macOS
- Linux (various desktop environments)

### Unicode Considerations
- Restrict to Unicode 12.0+ for compatibility
- Handle normalization (NFC vs NFD)
- Address ZWJ sequences and variation selectors
- Consider skin tone modifiers

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
uv pip install --system pillow numpy imagehash scikit-image requests beautifulsoup4
```

### Usage

**Encode a Bitcoin address to emoji:**
```bash
python emoji_codec.py encode 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
```

**Decode an emoji address back to Base58:**
```bash
python emoji_codec.py decode '🧔🤶🧔🐞🥝🧔🫅🥝🤚🦪🍁🫅🤴🕸️🤫🍎🍏🥝🌸🤴🌸🍈🤚🫑🍈👱👦👊🍎🕸️👦🤴😶🐣'
```

**Scan and validate with checksum:**
```bash
python emoji_codec.py scan '🧔🤶🧔🐞🥝🧔🫅🥝🤚🦪🍁🫅🤴🕸️🤫🍎🍏🥝🌸🤴🌸🍈🤚🫑🍈👱👦👊🍎🕸️👦🤴😶🐣'
```

**Run interactive demo:**
```bash
python demo.py
```

### Example Output

```
📝 Encoding Base58 address...
   Input: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

✅ Encoding successful!

   Base58: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
   Emoji:  🧔🤶🧔🐞🥝🧔🫅🥝🤚🦪🍁🫅🤴🕸️🤫🍎🍏🥝🌸🤴🌸🍈🤚🫑🍈👱👦👊🍎🕸️👦🤴😶🐣

   Character mapping:
     1 → 🧔  (person: beard)
     A → 🤶  (Mrs. Claus)
     1 → 🧔  (person: beard)
     z → 🐞  (lady beetle)
     ...
```

## 📜 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a research project. Contributions welcome for:
- Cross-platform emoji rendering data
- Visual similarity analysis
- Implementation libraries
- Security analysis
- Usability studies

## ⚡ Quick Reference

| Document | Purpose |
|----------|---------|
| README.md | Project overview and quick start |
| EMOJI_SELECTION_REPORT.md | Visual similarity analysis results |
| TODO.md | Detailed task breakdown (8 phases) |
| BIP_REVIEW.md | Critical analysis and recommendations |

---

**Status**: ✅ Phase 2 Complete - Visual Analysis & Reference Implementation
**Last Updated**: 2025-11-09

