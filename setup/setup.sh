apt-get update
apt install docker.io python3-pip -y

# install pip3 package
pip3 install web3 python-dotenv psycopg2-binary

# Setup Database
python3 ./setup/setupDB.py

# Install Oyente
docker pull luongnguyen/oyente

# Install Mythril
apt update
apt install software-properties-common -y
add-apt-repository ppa:ethereum/ethereum -y
apt install solc -y
apt install libssl-dev python3-dev python3-pip -y
pip3 install mythril

# Install Maian tool
#git clone https://github.com/ivicanikolicsg/MAIAN.git
#cd MAIAN/tool
#Suicidal contracts use -c 0
#Prodigal contracts use -c 1
#Greedy contracts use -c 2
#python maian.py -b <bytecode_file> -c <0,1,2>

# -> require go-ethereum
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
# -> require solidity compiler
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc

# -> require z3 
git clone https://github.com/Z3Prover/z3.git
python scripts/mk_make.py
cd build
make
sudo make install
# -> require web3
pip install web3


# Install Vadal tool
# git clone https://github.com/usyd-blockchain/vandal.git
pip3 install Sphinx==1.4.6 sphinx_rtd_theme==0.1.9 networkx==1.11 pydotplus==2.0.2 pytest==3.0.2 termcolor==1.1.0

