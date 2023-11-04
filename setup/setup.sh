apt-get update
apt install docker.io python3-pip -y

# install pip3 package
pip3 install web3 python-dotenv psycopg2-binary

# Setup Database
python3 ./setupDB.py

# Install Oyente
docker pull luongnguyen/oyente

# Install Mythril
apt update
apt install software-properties-common -y
add-apt-repository ppa:ethereum/ethereum -y
apt install solc -y
apt install libssl-dev python3-dev python3-pip -y
pip3 install mythril