#!/usr/bin/env bash
# Build the deck: generate the .pptx, export the .pdf backup, render previews.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m deck.build

# LibreOffice needs its program dir on the library path in this container.
export LD_LIBRARY_PATH="/usr/lib/libreoffice/program:${LD_LIBRARY_PATH:-}"
soffice --headless --convert-to pdf --outdir . future-of-work.pptx

echo "done: future-of-work.pptx + future-of-work.pdf"
