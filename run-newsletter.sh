#!/bin/bash
# TheNeuralVault-Newsletter-Agent — Task Runner
# Usage: bash run-newsletter.sh [edition_name]
# Example: bash run-newsletter.sh "issue-001"

EDITION="${1:-issue-$(date +%Y-%m-%d)}"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
OUTPUT_FILE="drafts/newsletter-${EDITION}-${TIMESTAMP}.md"
MEMORY_FILE="memory/newsletter-log.md"

mkdir -p drafts memory intel briefs/brand output/writer

echo "============================================"
echo "TheNeuralVault-Newsletter-Agent"
echo "Edition: $EDITION"
echo "Started: $TIMESTAMP"
echo "SEND IS BLOCKED — draft only"
echo "============================================"

# Pull all upstream inputs from Drive
echo "Pulling federation intelligence from Drive..."
rclone copy NeuralVault:theneuralvault/intel/ intel/ --include "*.md"
rclone copy NeuralVault:theneuralvault/briefs/ briefs/ --include "*.md"
rclone copy NeuralVault:theneuralvault/output/ output/writer/ --include "*.md"

# Find latest inputs
LATEST_INTEL=$(ls -t intel/*.md 2>/dev/null | head -1)
LATEST_SEO=$(ls -t briefs/seo*.md 2>/dev/null | head -1)
LATEST_BRAND=$(ls -t briefs/brand/*.md 2>/dev/null | head -1)
LATEST_ARTICLE=$(ls -t output/writer/*.md 2>/dev/null | head -1)

echo "Intel:   ${LATEST_INTEL:-none}"
echo "SEO:     ${LATEST_SEO:-none}"
echo "Brand:   ${LATEST_BRAND:-none}"
echo "Article: ${LATEST_ARTICLE:-none}"
echo ""

# Generate newsletter draft
python3 newsletter.py \
  "$EDITION" \
  "$OUTPUT_FILE" \
  "$LATEST_INTEL" \
  "$LATEST_SEO" \
  "$LATEST_BRAND" \
  "$LATEST_ARTICLE"

# Sync draft to Drive
echo ""
echo "Syncing draft to Drive..."
rclone copy drafts/ NeuralVault:theneuralvault/output/newsletter/
rclone copy memory/ NeuralVault:theneuralvault/memory/newsletter-agent/

# Log run
echo "$(date) | Edition: $EDITION | Draft: $OUTPUT_FILE" >> "$MEMORY_FILE"

echo ""
echo "============================================"
echo "Newsletter draft complete."
echo "Draft saved: $OUTPUT_FILE"
echo "Synced to: NeuralVault:theneuralvault/output/newsletter/"
echo ""
echo "NEXT STEPS FOR OPERATOR:"
echo "1. Open draft in Drive"
echo "2. Read and approve content"
echo "3. Copy to Beehiiv manually"
echo "4. Review subject line options"
echo "5. Schedule or send from Beehiiv dashboard"
echo "============================================"
