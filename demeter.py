# import library, module python
from web3 import Web3
import asyncio

# import file
from checkEnvironment import variableEnv
import preprocessBytecode
import scanVulnerabilities
import setupScanTool
from services import *
from contractLoader import contractLoader


#  Setup scan tool before scanning
# setupScanTool()


def hexToString(hex):
    return w3.to_hex(hex)


##### Get contract information #####


# Connect to Ethereum node
w3 = Web3(
    Web3.HTTPProvider(
        "https://mainnet.infura.io/v3/{}".format(variableEnv["INFURA_API_KEY"])
    )
)


async def demeter():
    # startBlockNumber = getStartBlockNumber()
    # startBlockNumber = 14047678
    # startBlockNumber = 14047731
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
                    # contractLoader(contractAddress, contractBytecode, networkName)

                    # Remove prefix 0x
                    contractBytecode = contractBytecode.replace("0x", "", 1)

                    # preprocessBytecode
                    preprocessedBytecode = preprocessBytecode(contractBytecode)

                    # After preprocess bytecode, merge operations => may be duplicate contract preprocessBytecode
                    if isExistsPreprocessedBytecode(preprocessedBytecode):
                        print("Duplicate bytecode!!!")
                        continue

                    # scan vulnerability
                    # scanResult = scanVulnerabilities(contractBytecode)

                    insertPreprocessedBytecodeToDB(
                        contractAddress,
                        preprocessedBytecode,
                        "vulner1;vulner2",
                        True,
                    )
        removePendingBlockNumber(blockNumber)


async def main():
    # Create Multi-thread scanner
    threadNumber = 4
    tasks = []
    for _ in range(threadNumber):
        task = asyncio.create_task(demeter())
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
