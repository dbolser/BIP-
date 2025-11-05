# TODO: BIP-😸 (Emoji Address Encoding)

## BIP Review Summary

**Concept**: Encode Bitcoin addresses as emoji strings using a base58-like mapping to 58 carefully selected emoji characters.

**Key Challenges Identified**:
- Cross-platform emoji rendering consistency
- Visual distinguishability between similar emoji
- User input methods for emoji
- Backward compatibility with existing address formats
- Security considerations (phishing, visual confusion)

---

## Phase 1: Data Collection & Preparation

### 1.1 Emoji Dataset Collection
- [ ] Scrape emoji images from https://unicode.org/emoji/charts/full-emoji-list.html
- [ ] Parse the HTML table structure to extract:
  - Unicode codepoints
  - CLDR short names
  - Platform-specific renderings (Apple, Google, Facebook, Windows, etc.)
- [ ] Download and save images as: `{cldr_short_name}-{platform}.png`
- [ ] Verify image quality and resolution consistency
- [ ] Create metadata JSON file with emoji properties

**Technical Notes**:
- Handle edge cases: skin tone modifiers, ZWJ sequences, variation selectors
- Consider emoji versions and Unicode support across platforms
- Store both SVG and PNG formats if available

### 1.2 Dataset Organization
- [ ] Create directory structure: `data/emoji/{platform}/`
- [ ] Generate inventory list of all available emoji
- [ ] Filter to emoji available across ALL major platforms
- [ ] Document any platform-specific rendering differences

---

## Phase 2: Visual Similarity Analysis

### 2.1 Image Preprocessing
- [ ] Normalize image sizes (recommend 128x128 or 256x256)
- [ ] Convert to consistent color space
- [ ] Apply augmentation techniques using Keras/TensorFlow:
  - Rotation (±10-15 degrees)
  - Scaling (90%-110%)
  - Brightness variations
  - Color jittering
- [ ] Create augmented dataset for robust training

### 2.2 Classification Model
- [ ] Build CNN classifier for CLDR name prediction
- [ ] Train on augmented dataset with cross-platform images
- [ ] Evaluate per-platform accuracy
- [ ] Identify emoji with >95% accuracy across ALL platforms
- [ ] Generate confusion matrix to identify similar-looking emoji

**Key Question**: Classification vs OCR approach?
- **Recommendation**: Classification is better for controlled emoji set
- OCR would be overkill and less reliable for this use case

---

## Phase 3: Emoji Selection for Base58 Mapping

### 3.1 Selection Criteria
- [ ] Filter to emoji available on iOS, Android, Windows, macOS, Linux
- [ ] Exclude emoji with visual similarity >threshold (e.g., >70% confusion)
- [ ] Prioritize commonly-used, culturally-neutral emoji
- [ ] Ensure emoji are easily distinguishable at small sizes
- [ ] Test with colorblind simulation tools

### 3.2 Create Base58 Mapping
- [ ] Select exactly 58 emoji from robust classification list
- [ ] Map to Base58 characters (same order as Bitcoin Base58Check):
  ```
  123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
  ```
- [ ] Document the mapping table
- [ ] Consider sorting emoji by visual distinctiveness

**Design Decision**: Should the mapping be:
- **Option A**: Direct 1:1 with Base58 alphabet (simple translation)
- **Option B**: Custom ordering optimized for visual distinction
- **Recommendation**: Option A for simplicity and standardization

---

## Phase 4: Library Development

### 4.1 Core Encoding Library
- [ ] Implement address → emoji encoder
- [ ] Implement emoji → address decoder
- [ ] Support all Bitcoin address formats:
  - P2PKH (1...)
  - P2SH (3...)
  - Bech32 (bc1...)
- [ ] Handle checksum verification
- [ ] Add error detection and correction if possible

### 4.2 Language Implementations
- [ ] Python library
- [ ] JavaScript/TypeScript library
- [ ] Rust library
- [ ] Go library
- [ ] Add comprehensive unit tests for each

### 4.3 Validation & Safety
- [ ] Implement strict emoji validation
- [ ] Detect and reject invalid emoji sequences
- [ ] Add warnings for potentially confusing emoji combinations
- [ ] Implement copy/paste handling for different OS platforms

---

## Phase 5: BIP Specification Document

### 5.1 Write Formal BIP
- [ ] Follow BIP-2 format guidelines
- [ ] Include:
  - Abstract
  - Motivation (why emoji addresses?)
  - Specification (technical details)
  - Rationale (design decisions)
  - Backwards Compatibility
  - Test Vectors
  - Reference Implementation
  - Security Considerations
- [ ] Assign BIP number (coordinate with BIP editors)

### 5.2 Security Analysis
- [ ] Document phishing risks (emoji lookalikes)
- [ ] Address visual confusion attacks
- [ ] Consider accessibility for visually impaired users
- [ ] Evaluate input method security (IME, keyboard apps)
- [ ] Review Unicode normalization issues

### 5.3 Use Case Analysis
- [ ] Define primary use cases:
  - Social media sharing?
  - Simplified payments?
  - Novelty/education?
- [ ] Evaluate practicality vs standard addresses
- [ ] Consider when emoji addresses should NOT be used

---

## Phase 6: Testing & Validation

### 6.1 Cross-Platform Testing
- [ ] Test on iOS (Safari, native apps)
- [ ] Test on Android (Chrome, native apps)
- [ ] Test on Windows (Edge, Chrome, Firefox)
- [ ] Test on macOS (Safari, Chrome, Firefox)
- [ ] Test on Linux (various DEs)
- [ ] Document any rendering issues

### 6.2 User Testing
- [ ] Conduct usability studies
- [ ] Measure error rates in manual entry
- [ ] Test copy/paste reliability
- [ ] Evaluate memorability vs standard addresses

### 6.3 Security Testing
- [ ] Test with Unicode normalization attacks
- [ ] Verify no homoglyph vulnerabilities
- [ ] Test with malicious emoji sequences
- [ ] Evaluate clipboard hijacking risks

---

## Phase 7: Documentation & Examples

### 7.1 User Documentation
- [ ] Create usage guide for end users
- [ ] Document how to input emoji on different platforms
- [ ] Provide conversion tools/web interface
- [ ] Create troubleshooting guide

### 7.2 Developer Documentation
- [ ] API reference for each library
- [ ] Integration examples
- [ ] Best practices guide
- [ ] Migration guide from standard addresses

### 7.3 Visual Assets
- [ ] Create emoji mapping chart (visual reference)
- [ ] Design logos/branding
- [ ] Create demo videos
- [ ] Generate example emoji addresses

---

## Phase 8: Community & Standardization

### 8.1 BIP Submission
- [ ] Submit draft BIP to bitcoin-dev mailing list
- [ ] Gather community feedback
- [ ] Iterate on specification
- [ ] Address concerns and criticism

### 8.2 Reference Implementation
- [ ] Create canonical implementation in C/C++
- [ ] Ensure compatibility with Bitcoin Core style
- [ ] Add to test vectors repository
- [ ] Submit for code review

### 8.3 Adoption Strategy
- [ ] Create demo wallet integration
- [ ] Partner with wallet developers
- [ ] Present at Bitcoin conferences
- [ ] Write blog posts and tutorials

---

## Open Questions & Considerations

1. **Character Direction**: Should emoji addresses support RTL/LTR directionality?
2. **Length**: How long will emoji addresses be compared to standard addresses?
3. **QR Codes**: How do emoji addresses perform in QR codes vs standard addresses?
4. **Accessibility**: How do screen readers handle emoji addresses?
5. **Versioning**: How to handle future emoji additions/deprecations?
6. **Normalization**: Which Unicode normalization form to use (NFC, NFD, etc.)?
7. **Input Method**: Should there be a custom keyboard/input tool?
8. **Checksum**: Use existing Base58Check or custom emoji checksum?

---

## Priority Recommendations

**HIGH PRIORITY**:
1. Validate the concept with a prototype (Phase 1-3 minimal version)
2. Test cross-platform rendering consistency EARLY
3. Engage with Bitcoin community for feedback on viability
4. Research existing similar proposals

**MEDIUM PRIORITY**:
5. Develop comprehensive security analysis
6. Create user testing plan
7. Build reference implementations

**LOW PRIORITY**:
8. Branding and marketing materials
9. Conference presentations
10. Wallet integrations

---

## Risk Assessment

**Technical Risks**:
- Emoji rendering inconsistency across platforms (HIGH)
- Unicode version fragmentation (MEDIUM)
- Input method limitations (MEDIUM)

**Security Risks**:
- Visual confusion/phishing attacks (HIGH)
- Clipboard manipulation (MEDIUM)
- Social engineering (MEDIUM)

**Adoption Risks**:
- Limited practical utility (HIGH)
- Wallet developer resistance (MEDIUM)
- User confusion (MEDIUM)

---

## Next Steps

1. Start with Phase 1.1 - collect and analyze emoji dataset
2. Build quick prototype to validate cross-platform rendering
3. Create proof-of-concept encoder/decoder
4. Gather initial feedback before investing in full specification

**Estimated Timeline**: 3-6 months for complete BIP draft with reference implementation
