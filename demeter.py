import etherscan

# Get contract information
es = etherscan.Client(
    api_key="SIHIX7SCIYTGBS54GTVQQA2W5GXDISD9XU",
    cache_expire_after=5,
)

block = es.get_block_by_number(block_number=14047678)

# for transaction in block["transactions"]:
#     print(transaction["nonce"])

"""
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b95233c79a394b72b5cab7300878c2b3'))

print(w3.eth.get_transaction("0x63c7ee673db3f49437d595ae7288cd6edaf59e25284e5a3a45fdbb34d63ecaa3"))
print(w3.eth.get_transaction_receipt("0x63c7ee673db3f49437d595ae7288cd6edaf59e25284e5a3a45fdbb34d63ecaa3"))

# for txHash in blackListTransaction.iloc[:, 0]:
# 	print(w3.eth.(txHash))


# print(txHashCol)

# write Txhash column to file1.csv
# txHashCol.to_csv('file1.csv', mode='w', index=False)

# print(pd.read_csv("./file1.csv"))
exit()

##### WRITE FILE #####
fields = ["Txhash"]

# writing to csv file
with open("AfterRecord.csv", "w") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing name column
    csvwriter.writerow(fields)

    for txHash in txHashs:
        arrayRow = [txHash]
        csvwriter.writerow(arrayRow)
"""
