#!/bin/bash
echo "[Joy AI Setup] Initializing Local Environment for Linux..."

# 1. Set paths
PYTHON_EXE="python3"
LOCAL_LIB="joy_libs"

# 2. Always check/update dependencies
# Create local lib folder
if [ ! -d "$LOCAL_LIB" ]; then
    mkdir "$LOCAL_LIB"
fi

echo "[Joy AI Setup] Installing dependencies locally to '$LOCAL_LIB'..."
echo "(This avoids touching your system files)"

# Install pip script if missing
if [ ! -f "get-pip.py" ]; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
fi

# Install requirements
"$PYTHON_EXE" get-pip.py --target "$LOCAL_LIB" -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Installation failed."
    exit 1
fi

echo "[Joy AI Setup] Checking Ollama Models..."
echo "Pulling nomic-embed-text for RAG embedding..."
ollama list | grep -q 'nomic-embed-text' || ollama pull nomic-embed-text

echo "[Joy AI Setup] Launching Joy..."

# 4. Run the app with PYTHONPATH set to local lib
export PYTHONPATH="$PWD/$LOCAL_LIB"
"$PYTHON_EXE" main.py &
