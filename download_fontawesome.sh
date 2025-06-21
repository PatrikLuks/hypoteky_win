#!/bin/bash
# Stáhne a rozbalí Font Awesome Free do složky static/fontawesome
# Optimalizováno pro MacBook a zjednodušené použití

set -e

TARGET_DIR="$(dirname "$0")/static/fontawesome"
ZIP_URL="https://use.fontawesome.com/releases/v6.5.0/fontawesome-free-6.5.0-web.zip"
ZIP_FILE="/tmp/fontawesome.zip"

mkdir -p "$TARGET_DIR"
echo "Stahuji Font Awesome..."
curl -L "$ZIP_URL" -o "$ZIP_FILE"
echo "Rozbaluji..."
unzip -o "$ZIP_FILE" -d /tmp/fontawesome_zip
cp -r /tmp/fontawesome_zip/fontawesome-free-6.5.0-web/css "$TARGET_DIR"/
cp -r /tmp/fontawesome_zip/fontawesome-free-6.5.0-web/webfonts "$TARGET_DIR"/
echo "Hotovo! Font Awesome je připraven v $TARGET_DIR."
rm -rf /tmp/fontawesome_zip "$ZIP_FILE"
