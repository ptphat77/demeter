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

        # "ON CONFLICT DO NOTHING" handle duplicate contract address and contract preprocessBytecode
        insert_script = """
            INSERT INTO contract (address, preprocessBytecode, label)
            VALUES ('{}'::varchar, '{}'::text, {}::bool)
            ON CONFLICT DO NOTHING
            returning address
        """.format(
            contractAddress, contractBytecode, "true"
        )

        cur.execute(insert_script)

        conn.commit()
    except Exception as error:
        print(">>> error: ", error)


def hexToString(hex):
    return w3.to_hex(hex)


def updateStartBlockNumber(blockNumber):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        update_script = """
            UPDATE last_block_number_scanned SET block_number={} WHERE id=1
        """.format(
            blockNumber
        )
        print(update_script)
        cur.execute(update_script)

        conn.commit()
    except Exception as error:
        print(">>> error: ", error)


##### Get contract information #####

# Connect to Ethereum node
w3 = Web3(
    Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/{}".format(variableEnv["INFURA_API_KEY"])
    )
)

# startBlockNumber = getStartBlockNumber()
startBlockNumber = 14047678
endBlockNumber = w3.eth.get_block_number()

for blockNumber in range(startBlockNumber, endBlockNumber):
    block = w3.eth.get_block(blockNumber, True)
    print(blockNumber)
    for transaction in block["transactions"]:
        # if transaction["input"] == None => error
        if hexToString(transaction["input"]).startswith("0x60806040"):
            transactionInfo = w3.eth.get_transaction_receipt(
                hexToString(transaction["hash"])
            )

            contractAddress = transactionInfo["contractAddress"]
            if len(contractAddress) == 42:
                print("Found contract!!!")
                ugly_bytecode = w3.eth.get_code(contractAddress)
                contractBytecode = hexToString(ugly_bytecode)

                # preprocessBytecode
                # preprocessBytecode()

                insertContractInfoToDB(contractAddress, contractBytecode)

    updateStartBlockNumber(blockNumber)
