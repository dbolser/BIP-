#!/usr/bin/env python3
"""
Select a diverse test sample of emoji for prototyping visual similarity analysis
"""

import json
import random

def select_test_sample(input_file='data/emoji_metadata.json', output_file='data/test_sample.json', sample_size=100):
    """Select a diverse sample of emoji for testing"""

    with open(input_file, 'r', encoding='utf-8') as f:
        all_emoji = json.load(f)

    # Filter to fully-qualified only
    fully_qualified = [e for e in all_emoji if e['status'] == 'fully-qualified']
    print(f"Total fully-qualified emoji: {len(fully_qualified)}")

    # Categorize by emoji type based on name patterns
    categories = {
        'faces': [],
        'hands': [],
        'animals': [],
        'food': [],
        'objects': [],
        'symbols': [],
        'flags': [],
        'other': []
    }

    for emoji in fully_qualified:
        name = emoji['name'].lower()

        if 'face' in name or 'smile' in name or 'grin' in name:
            categories['faces'].append(emoji)
        elif 'hand' in name or 'finger' in name or 'fist' in name:
            categories['hands'].append(emoji)
        elif any(word in name for word in ['cat', 'dog', 'bird', 'animal', 'monkey', 'bear', 'lion']):
            categories['animals'].append(emoji)
        elif any(word in name for word in ['food', 'fruit', 'pizza', 'burger', 'coffee']):
            categories['food'].append(emoji)
        elif 'flag' in name:
            categories['flags'].append(emoji)
        elif any(word in name for word in ['heart', 'star', 'circle', 'square', 'triangle', 'arrow']):
            categories['symbols'].append(emoji)
        elif any(word in name for word in ['phone', 'computer', 'book', 'pen', 'car', 'house']):
            categories['objects'].append(emoji)
        else:
            categories['other'].append(emoji)

    print("\nCategory distribution:")
    for cat, items in categories.items():
        print(f"  {cat}: {len(items)}")

    # Sample proportionally from each category
    sample = []
    total_in_cats = sum(len(items) for items in categories.values())

    for cat, items in categories.items():
        if not items:
            continue

        # Calculate sample size for this category
        proportion = len(items) / total_in_cats
        cat_sample_size = max(1, int(sample_size * proportion))

        # Sample randomly
        cat_sample = random.sample(items, min(cat_sample_size, len(items)))
        sample.extend(cat_sample)
        print(f"  Sampled {len(cat_sample)} from {cat}")

    # Trim to exact sample size if needed
    if len(sample) > sample_size:
        sample = random.sample(sample, sample_size)

    print(f"\nFinal sample size: {len(sample)}")

    # Add some known confusable pairs
    confusable_names = [
        'grinning face', 'grinning face with big eyes',  # 😀😃
        'full moon', 'waning gibbous moon',  # 🌕🌖
        'red heart', 'orange heart', 'yellow heart',  # ❤️🧡💛
        'cat face', 'cat',  # 🐱🐈
    ]

    for name in confusable_names:
        matching = [e for e in fully_qualified if e['name'] == name]
        if matching and matching[0] not in sample:
            sample.append(matching[0])

    print(f"Sample size with confusables: {len(sample)}")

    # Save sample
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2, ensure_ascii=False)

    print(f"\nSaved test sample to {output_file}")

    # Show some examples
    print("\nSample emoji:")
    for emoji in sample[:20]:
        print(f"  {emoji['emoji']} - {emoji['name']}")

    return sample

if __name__ == '__main__':
    random.seed(42)  # Reproducible sampling
    select_test_sample()
