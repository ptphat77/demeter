# import library, module python
from web3 import Web3

# import file
from config.connectDB import connectDB
from checkEnvironment import variableEnv
import preprocessBytecode
import scanVulnerabilities
import setupScanTool

#  Setup scan tool before scanning
setupScanTool()


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
        print(">>> database error: ", error)
    finally:
        if cur != None:
            cur.close()
        if conn != None:
            conn.close()


def insertContractInfoToDB(contractAddress, contractBytecode, label):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        # "ON CONFLICT DO NOTHING" handle duplicate contract address and contract preprocessBytecode
        # scan block again => duplicate contract address
        # preprocessBytecode, merge operations => duplicate contract preprocessBytecode
        insert_script = """
            INSERT INTO contract (address, preprocessBytecode, label)
            VALUES ('{}'::varchar, '{}'::text, {}::bool)
            ON CONFLICT DO NOTHING
            returning address
        """.format(
            contractAddress, contractBytecode, str(label)
        )

        cur.execute(insert_script)

        conn.commit()
    except Exception as error:
        print(">>> database error: ", error)


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
        cur.execute(update_script)

        conn.commit()
    except Exception as error:
        print(">>> database error: ", error)


##### Get contract information #####

# Connect to Ethereum node
w3 = Web3(
    Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/{}".format(variableEnv["INFURA_API_KEY"])
    )
)

# startBlockNumber = getStartBlockNumber()
# startBlockNumber = 14047678
startBlockNumber = 14047684
endBlockNumber = w3.eth.get_block_number()

for blockNumber in range(startBlockNumber, endBlockNumber):
    block = w3.eth.get_block(blockNumber, True)
    print(blockNumber)
    for transaction in block["transactions"]:
        if hexToString(transaction["input"]).startswith("0x60806040"):
            transactionInfo = w3.eth.get_transaction_receipt(
                hexToString(transaction["hash"])
            )

            contractAddress = transactionInfo["contractAddress"]
            if len(contractAddress) == 42:
                print("Found contract!!!")
                ugly_bytecode = w3.eth.get_code(contractAddress)
                contractBytecode = hexToString(ugly_bytecode)

                # Remove prefix 0x
                contractBytecode = contractBytecode.replace("0x", "", 1)

                # preprocessBytecode
                preprocessedBytecode = preprocessBytecode(contractBytecode)

                # scan vulnerability
                label = scanVulnerabilities(contractBytecode)

                insertContractInfoToDB(contractAddress, preprocessedBytecode, label)

    updateStartBlockNumber(blockNumber)
