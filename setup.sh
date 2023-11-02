apt-get update
apt install docker.io python3-pip -y

# Setup Database
python ./setupDB.py

# Install Oyente
docker pull luongnguyen/oyente

# Install Mythril
mkdir scanVulnTool
git clone https://github.com/Consensys/mythril.git scanVulnTool/mythril
pip3 install mythril
