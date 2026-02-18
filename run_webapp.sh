#!/usr/bin/env bash
# Run the AI Fake Image Detector web app. Uses a virtual environment and Python 3.10–3.12 if available.
set -e
cd "$(dirname "$0")"

PYTHON=""
for p in python3.12 python3.11 python3.10 python; do
  if command -v "$p" &>/dev/null; then
    ver=$("$p" -c "import sys; print(sys.version_info[:2])" 2>/dev/null || true)
    if [[ "$ver" == "(3, 12)" || "$ver" == "(3, 11)" || "$ver" == "(3, 10)" ]]; then
      PYTHON="$p"
      break
    fi
  fi
done

if [[ -z "$PYTHON" ]]; then
  echo "This project requires Python 3.10, 3.11, or 3.12 (TensorFlow does not support 3.14 yet)."
  echo "Install one of them, for example:"
  echo "  brew install python@3.12"
  echo "  # or: pyenv install 3.12.0 && pyenv local 3.12.0"
  echo "Then run this script again."
  exit 1
fi

echo "Using: $($PYTHON --version)"

if [[ ! -d .venv ]]; then
  echo "Creating virtual environment..."
  "$PYTHON" -m venv .venv
fi

source .venv/bin/activate
echo "Installing dependencies (first time may take 5–10 min for TensorFlow)..."
pip install --upgrade pip
pip install -r frontend/requirements.txt
echo "Starting Streamlit app..."
exec streamlit run frontend/app.py --server.headless true
