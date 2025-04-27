# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv init && uv add 
python -m pip install --upgrade pip
# python -m venv .venv 
# source .venv/bin/activate
#python -m pip install -r req.txt
python -m pip install playwright beautifulsoup4 python-dotenv playwright-stealth
playwright install
playwright install-deps 