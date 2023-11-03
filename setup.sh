apt-get update
apt install docker.io python3-pip -y

# install pip3 package
pip3 install web3 python-dotenv psycopg2-binary

# Setup Database
python3 ./setupDB.py

# Install Oyente
docker pull luongnguyen/oyente

# Install Mythril
mkdir scanVulnTool
git clone https://github.com/Consensys/mythril.git scanVulnTool/mythril
pip3 install mythril