# BIP-😸 OCR Scanner

Browser-based OCR scanner for decoding emoji Bitcoin addresses back to Base58 format.

## 🎯 Purpose

This proof-of-concept demonstrates the feasibility of scanning emoji addresses using OCR technology. It allows users to:
- Capture emoji addresses from screens or printed materials
- Extract emoji characters using OCR
- Decode them back to standard Bitcoin addresses

## 📁 Files

### scanner.html
The main OCR scanner interface with:
- **Camera capture** - Use your device camera to scan emoji addresses
- **File upload** - Upload existing images of emoji addresses
- **Tesseract.js OCR** - Advanced OCR engine for text/emoji extraction
- **Real-time decoding** - Converts extracted emoji to Base58 addresses
- **Progress tracking** - Visual feedback during processing

### display.html
A companion page for generating test addresses:
- **Address encoder** - Converts Base58 addresses to emoji
- **Example addresses** - Pre-loaded Bitcoin addresses for testing
- **Adjustable display** - Multiple size options for scanning
- **Copy functions** - Easy copying of both formats

## 🚀 Quick Start

### Method 1: Two-Device Testing (Recommended)

1. **On Device 1** (computer/tablet):
   ```bash
   # Open the display page in a browser
   open display.html
   # Or visit: file:///path/to/BIP-/display.html
   ```
   - Select an example address or enter your own
   - Adjust size to "Large" or "X-Large" for easier scanning

2. **On Device 2** (phone/tablet with camera):
   ```bash
   # Open the scanner page
   open scanner.html
   # Or visit: file:///path/to/BIP-/scanner.html
   ```
   - Click "Start Camera"
   - Point at Device 1's screen
   - Click "Scan & Decode"

### Method 2: Screenshot Testing

1. Open `display.html` in a browser
2. Select an example address (e.g., Satoshi's Genesis address)
3. Take a screenshot of the emoji address display
4. Open `scanner.html`
5. Click "Upload Image" and select your screenshot
6. Click "Scan & Decode"

### Method 3: Python Generation + Browser Scan

1. Generate an emoji address with Python:
   ```bash
   python emoji_codec.py encode 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
   ```

2. Display the output on screen

3. Open `scanner.html` and scan

## 🧪 Test Examples

### Example 1: Genesis Block Address
**Base58:** `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
**Emoji:** 🧔🤶🧔🐞🥝🧔🫅🥝🤚🦪🍁🫅🤴🕸️🤫🍎🍏🥝🌸🤴🌸🍈🤚🫑🍈👱👦👊🍎🕸️👦🤴😶🐣

### Example 2: Standard Address
**Base58:** `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2`
**Emoji:** 🧔🫵👦🫵🍏🫑🪲👧🌳🖖👋🫅🖖🍑🌸🏵️👲🤚🤶🧑✋👱✋👴🏵️🍁👊🖐️👩🐣😶😦😶🤫

## 🔧 Technical Details

### OCR Engine
- **Library:** Tesseract.js v5.0.0
- **Language:** English (eng)
- **Mode:** Text recognition with emoji support

### Browser Requirements
- Modern browser with ES6+ support
- Camera API access (for camera scanning)
- File API support (for image upload)

### Limitations

1. **OCR Accuracy**
   - Standard OCR is designed for text, not emoji
   - Recognition accuracy varies by platform and emoji rendering
   - Some emoji may be misrecognized or missed entirely

2. **Cross-Platform Rendering**
   - Emoji appear differently on iOS vs Android vs Windows
   - OCR trained on one platform may struggle with others
   - Best results when scanning and displaying on similar platforms

3. **Image Quality**
   - Requires clear, high-resolution images
   - Good lighting conditions necessary
   - Direct screenshots work better than photos of screens

4. **Performance**
   - OCR processing takes 2-10 seconds depending on device
   - Larger images take longer to process
   - Mobile devices may be slower

## 📊 Expected Results

### ✅ Good Scenarios
- Screenshot of emoji from same device
- High contrast display (emoji on white background)
- Large emoji size (3em or larger)
- Direct camera capture in good lighting

### ⚠️ Challenging Scenarios
- Photos of screens (moiré patterns, glare)
- Small emoji size
- Poor lighting conditions
- Mixed emoji and text

### ❌ Known Issues
- Some emoji render as compound characters (e.g., 🕸️ = spider + web)
- Variation selectors may cause inconsistencies
- Similar-looking emoji may be confused
- OCR may detect non-emoji text as garbage

## 🔍 How It Works

1. **Image Capture**
   - Camera API captures video stream
   - Canvas API converts frame to image
   - Or FileReader API loads uploaded image

2. **OCR Processing**
   - Tesseract.js analyzes image
   - Extracts all text and symbols
   - Returns recognized characters with confidence scores

3. **Emoji Extraction**
   - Regex filters Unicode emoji from OCR text
   - Matches against BIP-😸 mapping table
   - Filters out unmapped emoji

4. **Decoding**
   - Maps each emoji to Base58 character
   - Reconstructs Bitcoin address
   - Validates character mapping

## 💡 Usage Tips

1. **For Best Results:**
   - Use high-contrast backgrounds
   - Maximize emoji size
   - Ensure good lighting
   - Keep camera steady
   - Use screenshots when possible

2. **Debugging:**
   - Check "Raw OCR Text" to see what was detected
   - Compare "Extracted Emoji" with original
   - Look for confidence scores below 80%

3. **Testing:**
   - Start with short addresses
   - Use well-known addresses (Genesis block)
   - Try different emoji sizes
   - Test on multiple devices

## 🎓 Educational Value

This scanner demonstrates:
- Feasibility of emoji address scanning
- Limitations of OCR for emoji recognition
- Cross-platform compatibility challenges
- Practical UX considerations for emoji addresses

## ⚡ Future Improvements

Potential enhancements:
1. **Computer Vision** - Use ML models trained specifically on emoji
2. **Pattern Matching** - Template matching instead of OCR
3. **QR Code Alternative** - Encode emoji addresses as QR codes
4. **Hybrid Approach** - Combine OCR with checksum validation
5. **Progressive Enhancement** - Mobile app with native camera access

## 🐛 Known Issues

1. OCR accuracy highly variable (30-70% depending on conditions)
2. Compound emoji with variation selectors may fail
3. No checksum validation yet
4. Processing time on mobile devices can be slow
5. Camera permission handling needs improvement

## 📝 Notes

- This is a proof-of-concept, not production-ready code
- OCR is not the optimal solution for emoji scanning
- Computer vision or ML models would be more accurate
- Consider QR codes for reliable address transfer
- Educational/research purposes only

## 🔗 Related Files

- `emoji_codec.py` - Python encoder/decoder
- `demo.py` - Interactive Python demo
- `data/base58_emoji_mapping.json` - Character mapping table
- `README.md` - Main project documentation

---

**Last Updated:** 2025-11-10
**Status:** Proof-of-Concept Complete ✅
