#!/usr/bin/env bash
# ============================================================
# download_data.sh — Download HMDA 2023 dataset
# ============================================================
# Source: CFPB HMDA Snapshot National Loan-Level Dataset
# Size: ~4 GB CSV, 11.5M+ rows, 99 columns
#
# Usage:
#   chmod +x scripts/download_data.sh
#   ./scripts/download_data.sh
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RAW_DIR="${PROJECT_DIR}/data/raw"

mkdir -p "$RAW_DIR"

CSV_FILE="${RAW_DIR}/hmda_2023.csv"

if [ -f "$CSV_FILE" ]; then
    SIZE=$(du -h "$CSV_FILE" | cut -f1)
    echo "Dataset already exists: $CSV_FILE ($SIZE)"
    echo "Delete it first if you want to re-download."
    exit 0
fi

echo "============================================================"
echo "  HMDA 2023 Snapshot Download"
echo "============================================================"
echo ""

# Method 1: Hugging Face (preferred — faster, resumable)
echo "Attempting download from Hugging Face..."
if command -v python3 &> /dev/null; then
    python3 -c "
from huggingface_hub import hf_hub_download
import shutil, os

print('Downloading from Hugging Face (this may take a few minutes)...')
path = hf_hub_download(
    repo_id='adi-123/hmda-2023-snapshot',
    filename='hmda_2023.csv',
    repo_type='dataset'
)
dest = '${CSV_FILE}'
shutil.copy2(path, dest)
size_gb = os.path.getsize(dest) / (1024**3)
print(f'Downloaded: {dest} ({size_gb:.2f} GB)')
" 2>/dev/null && exit 0
    echo "Hugging Face download failed. Trying direct download..."
fi

# Method 2: Direct from CFPB
CFPB_URL="https://files.ffiec.cfpb.gov/static-data/snapshot/2023/2023_public_lar_csv.zip"

echo "Downloading from CFPB (this is a large file, ~1.5 GB compressed)..."
echo "URL: $CFPB_URL"

if command -v curl &> /dev/null; then
    curl -L -o "${RAW_DIR}/hmda_2023.zip" "$CFPB_URL"
elif command -v wget &> /dev/null; then
    wget -O "${RAW_DIR}/hmda_2023.zip" "$CFPB_URL"
else
    echo "ERROR: Neither curl nor wget found. Install one and retry."
    exit 1
fi

echo "Extracting..."
cd "$RAW_DIR"
unzip -o hmda_2023.zip
mv 2023_public_lar.csv hmda_2023.csv 2>/dev/null || true
rm -f hmda_2023.zip

SIZE=$(du -h "$CSV_FILE" | cut -f1)
ROWS=$(wc -l < "$CSV_FILE")
echo ""
echo "Download complete!"
echo "  File: $CSV_FILE"
echo "  Size: $SIZE"
echo "  Rows: $ROWS"
