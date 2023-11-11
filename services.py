from config.connectDB import connectDB


def queryExec(queryScript, isHasReturn=True):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()
        cur.execute(queryScript)
        conn.commit()

        if isHasReturn:
            resultQuery = cur.fetchone()
            return resultQuery

    except Exception as error:
        print(">>> Database error: ", error)
        print(">>> Query script: ", " ".join((queryScript.split())[:2]), "...")
        # print(">>> Query script: ", queryScript)
        exit()


def getStartBlockNumber(networkName):
    resultQuery = queryExec(
        "SELECT block_number FROM start_block_number WHERE network_name='{}'".format(
            networkName
        )
    )
    return resultQuery[0]


def isExistsPreprocessedBytecode(preprocessedBytecode):
    resultQuery = queryExec(
        "SELECT label FROM contract_dataset WHERE md5_index = md5('{}'::text)".format(
            preprocessedBytecode
        )
    )
    return resultQuery


def insertPreprocessedBytecodeToDB(preprocessedBytecode, vulnerabilities, label):
    queryExec(
        """ INSERT INTO contract_dataset (md5_index, preprocess_bytecode, vulnerabilities, label)
            VALUES (md5('{}'::text), '{}'::text, '{}'::text, {}::bool)
        """.format(
            preprocessedBytecode, preprocessedBytecode, vulnerabilities, str(label)
        ),
        False,
    )


def updateStartBlockNumber(networkName, blockNumber):
    queryExec(
        "UPDATE start_block_number SET block_number={} WHERE network_name='{}'".format(
            blockNumber, networkName
        ),
        False,
    )


def insertCotnractInfoToDB(address, sourceCode, bytecode, abi):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()
        queryScript = """INSERT INTO contract_info (address, source_code, bytecode, abi) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"""
        data = (address, sourceCode, bytecode, abi)
        cur.execute(queryScript, data)
        conn.commit()

    except Exception as error:
        print(">>> Database error: ", error)
        print(">>> Query script: ", " ".join((queryScript.split())[:2]), "...")
        # print(">>> Query script: ", queryScript)
        exit()
