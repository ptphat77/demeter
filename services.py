from config.connectDB import connectDB


def queryExec(queryScript, isHasReturn=True, *datas):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        cur.execute(queryScript, (datas))
        conn.commit()

        if isHasReturn:
            resultQuery = cur.fetchone()
            return resultQuery

    except Exception as error:
        print(">>> Database error: ", error)
        print(">>> Query script: ", " ".join((queryScript.split())[:2]), "...")
        # print(">>> Query script: ", queryScript)
        exit()


def getStartBlockNumber():
    resultQuery = queryExec(
        "SELECT block_number FROM start_block_number WHERE network_name=%s",
        True,
        "mainnet",
    )
    return resultQuery[0]


def isExistsPreprocessedBytecode(preprocessedBytecode):
    resultQuery = queryExec(
        "SELECT label FROM contract_dataset WHERE md5_index = md5(%s)",
        True,
        preprocessedBytecode,
    )
    return resultQuery


def insertPreprocessedBytecodeToDB(
    contractAddress, preprocessedBytecode, vulnerabilities, label
):
    queryExec(
        """ INSERT INTO contract_dataset (address, md5_index, preprocess_bytecode, vulnerabilities, label)
            VALUES (%s, md5(%s), %s, %s, %s)
        """,
        False,
        contractAddress,
        preprocessedBytecode,
        preprocessedBytecode,
        vulnerabilities,
        str(label),
    )


def updateStartBlockNumber(blockNumber):
    queryExec(
        "UPDATE start_block_number SET block_number=%s WHERE network_name=%s",
        False,
        blockNumber,
        "mainnet",
    )


def insertCotnractInfoToDB(address, sourceCode, bytecode, abi):
    queryExec(
        "INSERT INTO contract_info (address, source_code, bytecode, abi) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
        False,
        address,
        sourceCode,
        bytecode,
        abi,
    )
