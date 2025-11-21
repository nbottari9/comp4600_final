sudo apt -y update
sudo apt install -y unzip curl
curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'
unzip awscliv2.zip
sudo ./aws/install
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
curl -fsSL https://ramalama.ai/install.sh | bash
git clone https://github.com/nbottari9/comp4600_final.git
cd comp4600_final/rag-scripts/
uv init .
uv add pip-system-certs aiohttp
uv run parallel_download.py && ./vectorize.sh ecr rag-data
