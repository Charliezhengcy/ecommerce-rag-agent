from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_processing import get_settings, raw_json_files, read_json

settings = get_settings()
items = [read_json(path) for path in raw_json_files(settings.raw_dataset_dir)]
counts = Counter(item.get("category", "未知") for item in items)
missing = sum(not (settings.raw_dataset_dir / item.get("image_path", "")).exists() for item in items)
print("Found categories:")
for category, count in sorted(counts.items()):
    print(f"- {category}: {count} products")
print(f"\nTotal products: {len(items)}")
print(f"Images missing: {missing}")

