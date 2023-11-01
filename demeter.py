import etherscan
from web3 import Web3

from config.connectDB import connectDB
from checkEnvironment import variableEnv


def getStartBlockNumber():
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        select_script = """
            SELECT block_number from last_block_number_scanned LIMIT 1
        """
        cur.execute(select_script)
        resultQuery = cur.fetchone()

        conn.commit()

        return resultQuery[0]
    except Exception as error:
        print(">>> error: ", error)
    finally:
        if cur != None:
            cur.close()
        if conn != None:
            conn.close()


def insertContractInfoToDB(contractAddress, contractBytecode):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        insert_script = """
            INSERT INTO contract (address, preprocessBytecode, label)
            VALUES ('{}'::varchar, '{}'::text, {}::bool)
            returning address
        """.format(
            contractAddress, contractBytecode, "true"
        )
        print(">>>insert_script: ", insert_script)
        cur.execute(insert_script)

        conn.commit()
    except Exception as error:
        print(">>> error: ", error)

def hexToString(hex):
    return w3.to_hex(hex)
##### Get contract information #####

es = etherscan.Client(
    api_key=variableEnv["ETHERSCAN_API_KEY"],
    cache_expire_after=5,
)

# Connect to Ethereum node
w3 = Web3(
    Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/{}".format(variableEnv["INFURA_API_KEY"])
    )
)

# startBlockNumber = getStartBlockNumber()
startBlockNumber = 14047678
endBlockNumber = w3.eth.get_block_number()
# contractBytecode = w3.eth.get_code("0x7849423162af40B474281dD679337cb2E2A93176")
# contractBytecode = w3.eth.get_code("0xCE88547eF1E2A005059Fc73BA6E82DbC6FFbe336")
# print(">>> contractBytecode: ", contractBytecode)
# exit()
for blockNumber in range(startBlockNumber, endBlockNumber):
    block = w3.eth.get_block(blockNumber, True)

    # block = es.get_block_by_number(blockNumber)
    # print(block)
    # import json
    # with open("scanBlockResult.json", "w") as file:
    #     file.write(json.dumps(block, separators=(',', ':')))
    # exit()
    
    print(blockNumber)
    for transaction in block["transactions"]:
        # if transaction["input"] == None => error
        if hexToString(transaction["input"]).startswith("0x60806040"):
            transactionInfo = w3.eth.get_transaction_receipt(hexToString(transaction["hash"]))
            # transactionInfo = es.get_transactions_by_address(hexToString(transaction["hash"]))

            print('>>>transaction["hash"]',type(hexToString(transaction["hash"])), hexToString(transaction["hash"]))

            contractAddress = transactionInfo["contractAddress"]
            print(">>>contractAddress", type(contractAddress), transactionInfo["contractAddress"])
            print(len(contractAddress))
            if len(contractAddress) == 42:
                print("Found contract!!!")
                print(">>>contractAddress#IF42", type(contractAddress), contractAddress)
                ugly_bytecode = w3.eth.get_code(contractAddress)
                contractBytecode = hexToString(ugly_bytecode)
                insertContractInfoToDB(contractAddress, contractBytecode)
                


# block = es.get_block_by_number(block_number=14047678)

# for transaction in block["transactions"]:
#     print(transaction["nonce"])
