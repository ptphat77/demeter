import requests

from checkEnvironment import variableEnv
from services import insertCotnractInfoToDB

networkLink = {"mainnet": "", "goerli": "-goerli", "sepolia": "-sepolia"}


def contractLoader(contractAddress, contractBytecode):
    url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}".format(
        contractAddress, variableEnv["ETHERSCAN_API_KEY"]
    )

    try:
        # Send a GET request to the Etherscan API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the API call was successful
            if data["status"] == "1":
                # Get source code vs abi
                sourceCode = str(data["result"][0]["SourceCode"])
                abi = str(data["result"][0]["ABI"])

                insertCotnractInfoToDB(
                    contractAddress, sourceCode, contractBytecode, abi
                )
            else:
                print("API call failed. Check your API key and contract address.")
        else:
            print(
                "Request to Etherscan API failed. Please check your network connection or try again later."
            )
    except Exception as e:
        print(f">>> Etherscan Error: {str(e)}")
        contractLoader(contractAddress, contractBytecode)
