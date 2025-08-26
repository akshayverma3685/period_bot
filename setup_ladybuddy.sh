#!/bin/bash

echo "🚀 Starting LadyBuddy bot setup..."

# 1️⃣ Update system packages
sudo apt update && sudo apt upgrade -y

# 2️⃣ Install curl (if not installed)
sudo apt install curl -y

# 3️⃣ Install Rust (for Python 3.12 aiogram)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
echo "✅ Rust installed: $(rustc --version)"

# 4️⃣ Upgrade pip, setuptools, wheel
python3 -m pip install --upgrade pip setuptools wheel

# 5️⃣ Install Python dependencies
pip install aiogram requests

# 6️⃣ Start the bot
echo "🚀 Running LadyBuddy bot..."
python3 main.py
