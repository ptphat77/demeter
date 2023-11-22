# import library, module python
from web3 import Web3
import threading

# import file
from checkEnvironment import variableEnv
import preprocessBytecode
import scanVulnerabilities
import setupScanTool
from services import *
from contractLoader import contractLoader


def hexToString(hex):
    return w3.to_hex(hex)


##### Get contract information #####


# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{variableEnv['INFURA_API_KEY']}"))


def demeter(threadNo):
    #  Setup scan tool before scanning
    setupScanTool(threadNo)

    endBlockNumber = w3.eth.get_block_number()

    while True:
        PendingBlockNumber = getTimeoutPendingBlockNumber()

        blockNumber = (
            PendingBlockNumber if PendingBlockNumber else getStartBlockNumber()
        )

        if blockNumber > endBlockNumber:
            endBlockNumber = w3.eth.get_block_number()
            continue

        block = w3.eth.get_block(blockNumber, True)
        print(">>>blockNumber", blockNumber)
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

                    # Collect contract information
                    contractLoader(contractAddress, contractBytecode)

                    # Remove prefix 0x
                    contractBytecode = contractBytecode.replace("0x", "", 1)

                    # preprocessBytecode
                    preprocessedBytecode = preprocessBytecode(contractBytecode)

                    # After preprocess bytecode, merge operations => may be duplicate contract preprocessBytecode
                    if isExistsPreprocessedBytecode(preprocessedBytecode):
                        print("Duplicate bytecode!!!")
                        continue

                    # scan vulnerability
                    scanResult = scanVulnerabilities(contractBytecode, threadNo)

                    insertPreprocessedBytecodeToDB(
                        contractAddress,
                        preprocessedBytecode,
                        scanResult["vulnerabilitiesSummary"],
                        scanResult["labelSummary"],
                    )
        removePendingBlockNumber(blockNumber)


if __name__ == "__main__":
    threadNumber = int(variableEnv['THREAD_NUMBER'])
    threads = []
    for threadNo in range(threadNumber):
        thread = threading.Thread(target=demeter, args=(threadNo,))
        threads.append(thread)
        thread.start()
