#!/bin/sh
# Rebuilds the reading copy and the PDF. Run after editing anything in content/.
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
python3 .build/build.py
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=tegwell-archive.pdf --virtual-time-budget=30000 \
  "file://$PWD/tegwell-archive.html" 2>/dev/null
python3 .build/build.py   # second pass picks up the new PDF size for the download link
