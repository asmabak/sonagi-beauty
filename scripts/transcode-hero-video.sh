#!/usr/bin/env bash
# Transcode the Sonagi rain-encounter hero clip into a web-optimized
# MP4 sized for the homepage hero slot.
#
# Input:  images/2026-04-20/sonagi-rain-encounter/sonagi - rain encounter_Enhanced.mp4
#         (2160x3840 portrait, 15s, ~80 MB)
# Output: files/videos/sonagi-hero-web.mp4
#         (1080x1920 portrait, H.264, no audio, faststart, target 3-5 MB)
#
# Run from the repo root:
#   bash scripts/transcode-hero-video.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT="$REPO_ROOT/images/2026-04-20/sonagi-rain-encounter/sonagi - rain encounter_Enhanced.mp4"
OUTPUT_DIR="$REPO_ROOT/files/videos"
OUTPUT="$OUTPUT_DIR/sonagi-hero-web.mp4"

mkdir -p "$OUTPUT_DIR"

ffmpeg -y -i "$INPUT" \
  -vf scale=1080:1920 \
  -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p \
  -an \
  -movflags +faststart \
  "$OUTPUT"

echo "Wrote $OUTPUT"
ls -lh "$OUTPUT"
