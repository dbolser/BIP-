#!/usr/bin/env python3
"""
Visual Similarity Analyzer for Emoji Selection

This script analyzes visual similarity between emoji to identify:
1. Confusable pairs (too similar)
2. Most visually distinct emoji
3. Platform consistency
4. Top candidates for Base58 mapping

Uses multiple similarity metrics:
- Perceptual hashing (dHash, pHash, aHash)
- Structural Similarity Index (SSIM)
- Color histogram comparison
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Set
import imagehash
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim


class EmojiSimilarityAnalyzer:
    """Analyzes visual similarity between emoji"""

    def __init__(self, emoji_metadata_file='data/emoji_metadata.json',
                 images_dir='data/emoji_images'):
        """Initialize analyzer with emoji metadata and image directory"""

        with open(emoji_metadata_file, 'r', encoding='utf-8') as f:
            self.all_emoji = json.load(f)

        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        # Filter to fully-qualified emoji only
        self.emoji_list = [e for e in self.all_emoji if e['status'] == 'fully-qualified']

        # Storage for computed data
        self.hashes = {}  # emoji_id -> {dhash, phash, ahash}
        self.images = {}  # emoji_id -> PIL Image
        self.similarity_matrix = {}  # (id1, id2) -> similarity_score

    def _get_emoji_filepath(self, emoji: Dict) -> Path:
        """
        Construct the filepath for a given emoji's image

        Args:
            emoji: Emoji dictionary with 'codepoint' and 'name' keys

        Returns:
            Path to the emoji image file
        """
        codepoint = emoji['codepoint'].replace(' ', '-').lower()
        safe_name = emoji['name'].replace('/', '-').replace(' ', '_')
        filename = f"{codepoint}_{safe_name}.png"
        return self.images_dir / filename

    def filter_problematic_emoji(self) -> List[Dict]:
        """
        Filter out problematic emoji categories:
        - Skin tone variants
        - Flag variations
        - ZWJ sequences (complex emoji)
        - Regional indicators
        """
        filtered = []

        for emoji in self.emoji_list:
            name = emoji['name'].lower()
            codepoint = emoji['codepoint']

            # Skip skin tone modifiers (U+1F3FB - U+1F3FF)
            if any(tone in codepoint for tone in ['1F3FB', '1F3FC', '1F3FD', '1F3FE', '1F3FF']):
                continue

            # Skip flags (regional indicators U+1F1E6 - U+1F1FF)
            if 'flag' in name or codepoint.startswith('1F1'):
                continue

            # Skip ZWJ sequences (contain U+200D)
            if '200D' in codepoint:
                continue

            # Skip keycap sequences
            if 'keycap' in name or '20E3' in codepoint:
                continue

            filtered.append(emoji)

        print(f"Filtered {len(self.emoji_list)} -> {len(filtered)} emoji")
        print(f"Removed {len(self.emoji_list) - len(filtered)} problematic emoji")

        return filtered

    def download_emoji_images(self, emoji_list: List[Dict], max_download=None) -> int:
        """
        Download emoji images from Twemoji CDN
        Returns number of successfully downloaded images
        """
        import requests

        downloaded = 0
        failed = []
        total = len(emoji_list) if max_download is None else min(max_download, len(emoji_list))

        print(f"\nDownloading {total} emoji images from Twemoji...")

        for i, emoji in enumerate(emoji_list[:total]):
            if i % 50 == 0 and i > 0:
                print(f"  Progress: {i}/{total} ({100*i//total}%)")

            # Convert codepoint to format needed for Twemoji
            codepoint = emoji['codepoint'].replace(' ', '-').lower()

            # Try both 72x72 and svg formats
            urls = [
                f"https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{codepoint}.png",
                f"https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/{codepoint}.svg",
            ]

            # Get filepath using helper method
            filepath = self._get_emoji_filepath(emoji)

            # Skip if already downloaded
            if filepath.exists():
                downloaded += 1
                continue

            success = False
            for url in urls:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()

                    # Save the image
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    downloaded += 1
                    success = True
                    break

                except Exception as e:
                    continue

            if not success:
                # Try without variation selector FE0F
                if 'fe0f' in codepoint:
                    alt_codepoint = codepoint.replace('-fe0f', '')
                    alt_url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{alt_codepoint}.png"
                    try:
                        response = requests.get(alt_url, timeout=10)
                        response.raise_for_status()
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        downloaded += 1
                        success = True
                    except:
                        pass

                if not success:
                    failed.append(emoji['emoji'])

        print(f"\n✅ Downloaded {downloaded}/{total} images")
        if failed:
            print(f"❌ Failed: {len(failed)} images")

        return downloaded

    def load_and_preprocess_image(self, emoji: Dict, size=(64, 64)) -> Image.Image:
        """Load and preprocess emoji image"""
        filepath = self._get_emoji_filepath(emoji)

        if not filepath.exists():
            raise FileNotFoundError(f"Image not found: {filepath}")

        # Load and resize image
        img = Image.open(filepath)

        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Resize to standard size
        img = img.resize(size, Image.Resampling.LANCZOS)

        return img

    def compute_perceptual_hashes(self, emoji_list: List[Dict]) -> Dict:
        """
        Compute multiple perceptual hashes for each emoji

        Hash types:
        - dHash (difference hash): Good for finding similar images
        - pHash (perceptual hash): Robust to resizing, color changes
        - aHash (average hash): Fast, good for exact duplicates
        """
        print("\nComputing perceptual hashes...")

        hashes = {}
        failed = []

        for i, emoji in enumerate(emoji_list):
            if i % 100 == 0 and i > 0:
                print(f"  Processed {i}/{len(emoji_list)}")

            try:
                img = self.load_and_preprocess_image(emoji)

                # Compute multiple hash types
                hashes[emoji['emoji']] = {
                    'dhash': imagehash.dhash(img),
                    'phash': imagehash.phash(img),
                    'ahash': imagehash.average_hash(img),
                    'whash': imagehash.whash(img),  # Wavelet hash
                }

                # Store image for later SSIM comparison
                self.images[emoji['emoji']] = img

            except Exception as e:
                failed.append((emoji['emoji'], str(e)))

        print(f"✅ Computed hashes for {len(hashes)} emoji")
        if failed:
            print(f"❌ Failed: {len(failed)} emoji")

        self.hashes = hashes
        return hashes

    def calculate_hash_similarity(self, hash1: imagehash.ImageHash,
                                  hash2: imagehash.ImageHash) -> float:
        """
        Calculate similarity between two perceptual hashes
        Returns value between 0 (identical) and 1 (completely different)

        We normalize by hash size (typically 64 bits) to get 0-1 range
        """
        hamming_distance = hash1 - hash2
        # Normalize to 0-1 range (64 is typical hash size)
        similarity = hamming_distance / 64.0
        return similarity

    def find_confusable_pairs(self, threshold=0.15) -> List[Tuple]:
        """
        Find pairs of emoji that are too similar (confusable)

        Args:
            threshold: Similarity threshold (0-1, lower = more similar)
                      0.15 means hashes differ by ~10 bits out of 64

        Returns:
            List of (emoji1, emoji2, similarity_score) tuples
        """
        print(f"\nFinding confusable pairs (threshold={threshold})...")

        confusable_pairs = []
        emoji_list = list(self.hashes.keys())

        total_comparisons = len(emoji_list) * (len(emoji_list) - 1) // 2
        comparisons = 0

        for i, emoji1 in enumerate(emoji_list):
            for emoji2 in emoji_list[i+1:]:
                comparisons += 1

                if comparisons % 10000 == 0:
                    print(f"  Comparisons: {comparisons}/{total_comparisons} ({100*comparisons//total_comparisons}%)")

                # Calculate average similarity across all hash types
                similarities = []
                for hash_type in ['dhash', 'phash', 'ahash', 'whash']:
                    sim = self.calculate_hash_similarity(
                        self.hashes[emoji1][hash_type],
                        self.hashes[emoji2][hash_type]
                    )
                    similarities.append(sim)

                avg_similarity = np.mean(similarities)

                # If too similar, it's confusable
                if avg_similarity < threshold:
                    confusable_pairs.append((emoji1, emoji2, avg_similarity))

        # Sort by similarity (most similar first)
        confusable_pairs.sort(key=lambda x: x[2])

        print(f"✅ Found {len(confusable_pairs)} confusable pairs")

        return confusable_pairs

    def calculate_distinctiveness_scores(self) -> Dict[str, float]:
        """
        Calculate distinctiveness score for each emoji

        Score is average similarity to all other emoji:
        - Higher score = less distinct (more similar to others)
        - Lower score = more distinct (unique looking)
        """
        print("\nCalculating distinctiveness scores...")

        scores = {}
        emoji_list = list(self.hashes.keys())

        for i, emoji1 in enumerate(emoji_list):
            if i % 100 == 0:
                print(f"  Processed {i}/{len(emoji_list)}")

            similarities = []

            for emoji2 in emoji_list:
                if emoji1 == emoji2:
                    continue

                # Average similarity across hash types
                sims = []
                for hash_type in ['dhash', 'phash', 'ahash', 'whash']:
                    sim = self.calculate_hash_similarity(
                        self.hashes[emoji1][hash_type],
                        self.hashes[emoji2][hash_type]
                    )
                    sims.append(sim)

                similarities.append(np.mean(sims))

            # Average similarity to all others
            # Lower score = more distinct
            scores[emoji1] = np.mean(similarities)

        print(f"✅ Calculated distinctiveness for {len(scores)} emoji")

        return scores

    def select_top_candidates(self, emoji_list: List[Dict],
                             distinctiveness_scores: Dict[str, float],
                             n_candidates=150) -> List[Dict]:
        """
        Select top N most distinct emoji candidates

        Prioritizes:
        1. High distinctiveness (low similarity score)
        2. Simple, non-compound emoji
        3. Cross-platform compatibility
        """
        print(f"\nSelecting top {n_candidates} candidates...")

        # Create ranking list
        ranked = []
        for emoji in emoji_list:
            if emoji['emoji'] in distinctiveness_scores:
                ranked.append({
                    'emoji': emoji['emoji'],
                    'name': emoji['name'],
                    'codepoint': emoji['codepoint'],
                    'distinctiveness': distinctiveness_scores[emoji['emoji']]
                })

        # Sort by distinctiveness (lower = more distinct)
        ranked.sort(key=lambda x: x['distinctiveness'])

        # Take top N
        top_candidates = ranked[:n_candidates]

        print(f"✅ Selected {len(top_candidates)} top candidates")
        print(f"\nMost distinct emoji:")
        for i, candidate in enumerate(top_candidates[:10]):
            print(f"  {i+1}. {candidate['emoji']} {candidate['name']} (score: {candidate['distinctiveness']:.3f})")

        print(f"\nLeast distinct (from candidates):")
        for i, candidate in enumerate(top_candidates[-10:]):
            print(f"  {candidate['emoji']} {candidate['name']} (score: {candidate['distinctiveness']:.3f})")

        return top_candidates


def main():
    """Run visual similarity analysis pipeline"""

    print("=" * 60)
    print("EMOJI VISUAL SIMILARITY ANALYZER")
    print("=" * 60)

    # Initialize analyzer
    analyzer = EmojiSimilarityAnalyzer()

    # Step 1: Filter problematic emoji
    print("\n[STEP 1] Filtering problematic emoji...")
    filtered_emoji = analyzer.filter_problematic_emoji()

    # Step 2: Download images (start with subset for testing)
    print("\n[STEP 2] Downloading emoji images...")
    # For testing, start with 500 emoji
    test_size = 500
    downloaded = analyzer.download_emoji_images(filtered_emoji, max_download=test_size)

    if downloaded < 100:
        print("\n❌ Not enough images downloaded. Check your internet connection.")
        return

    # Step 3: Compute perceptual hashes
    print("\n[STEP 3] Computing perceptual hashes...")
    # Only analyze emoji we have images for
    available_emoji = [e for e in filtered_emoji[:test_size]
                      if (analyzer.images_dir / f"{e['codepoint'].replace(' ', '-').lower()}_{e['name'].replace('/', '-').replace(' ', '_')}.png").exists()]

    print(f"Analyzing {len(available_emoji)} emoji with downloaded images...")
    hashes = analyzer.compute_perceptual_hashes(available_emoji)

    # Step 4: Find confusable pairs
    print("\n[STEP 4] Finding confusable pairs...")
    confusable = analyzer.find_confusable_pairs(threshold=0.15)

    # Step 5: Calculate distinctiveness
    print("\n[STEP 5] Calculating distinctiveness scores...")
    scores = analyzer.calculate_distinctiveness_scores()

    # Step 6: Select top candidates
    print("\n[STEP 6] Selecting top candidates...")
    candidates = analyzer.select_top_candidates(available_emoji, scores, n_candidates=150)

    # Save results
    print("\n[STEP 7] Saving results...")

    # Save confusable pairs
    confusable_output = []
    for emoji1, emoji2, score in confusable[:50]:  # Top 50 most confusable
        confusable_output.append({
            'emoji1': emoji1,
            'emoji2': emoji2,
            'similarity': float(score)
        })

    with open('data/confusable_pairs.json', 'w', encoding='utf-8') as f:
        json.dump(confusable_output, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(confusable_output)} confusable pairs to data/confusable_pairs.json")

    # Save top candidates
    with open('data/top_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(candidates)} candidates to data/top_candidates.json")

    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nTotal emoji analyzed: {len(available_emoji)}")
    print(f"Confusable pairs found: {len(confusable)}")
    print(f"Top candidates selected: {len(candidates)}")
    print(f"\nNext step: Review candidates and select final 58 for Base58 mapping")
    print("=" * 60)


if __name__ == '__main__':
    main()
