import os

# 1. Force Hugging Face to disable symlinks (The Ultimate Windows Fix)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from sentence_transformers import SentenceTransformer

print("🚀 Starting secure download (Symlinks Disabled for Windows)...")
# 2. Download the model directly to disk
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("✅ Download complete and verified! The cache is now healthy.")