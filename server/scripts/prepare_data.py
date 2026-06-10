from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_processing import prepare

products, documents = prepare()
print(f"Prepared {len(products)} products and {len(documents)} RAG documents.")

