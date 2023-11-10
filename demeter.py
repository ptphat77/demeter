# import library, module python
from web3 import Web3

# import file
from checkEnvironment import variableEnv
import preprocessBytecode
import scanVulnerabilities
import setupScanTool
from services import *


#  Setup scan tool before scanning
setupScanTool()


def hexToString(hex):
    return w3.to_hex(hex)


##### Get contract information #####


networkNames = ["mainnet", "goerli", "sepolia"]

for networkName in networkNames:
    # Connect to Ethereum node
    w3 = Web3(
        Web3.HTTPProvider(
            "https://{}.infura.io/v3/{}".format(
                networkName, variableEnv["INFURA_API_KEY"]
            )
        )
    )

    # startBlockNumber = getStartBlockNumber(networkName)
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

                    # After preprocess bytecode, merge operations => may be duplicate contract preprocessBytecode
                    if isExistsPreprocessedBytecode(preprocessedBytecode):
                        print("Duplicate bytecode!!!")
                        continue

                    # scan vulnerability
                    scanResult = scanVulnerabilities(contractBytecode)

                    insertContractInfoToDB(
                        preprocessedBytecode,
                        scanResult["vulnerabilitiesSummary"],
                        scanResult["labelSummary"],
                    )

        updateStartBlockNumber(networkName, blockNumber + 1)
