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
        """WITH resultPreviousQuery as (UPDATE start_block_number SET block_number=block_number + 1 WHERE network_name='mainnet' RETURNING block_number - 1 AS previous_block_number)
            INSERT INTO pending_block_number (block_number, time) VALUES ((SELECT previous_block_number FROM resultPreviousQuery), (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')) ON CONFLICT DO NOTHING RETURNING block_number - 1
        """,
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
            ON CONFLICT DO NOTHING
        """,
        False,
        contractAddress,
        preprocessedBytecode,
        preprocessedBytecode,
        vulnerabilities,
        str(label),
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


def getTimeoutPendingBlockNumber():
    resultQuery = queryExec(
        "UPDATE pending_block_number SET time=(CURRENT_TIMESTAMP AT TIME ZONE 'UTC') WHERE block_number IN ( SELECT block_number FROM pending_block_number WHERE time < ((CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '1 hour') ORDER BY time LIMIT 1) RETURNING block_number",
        True,
    )
    if resultQuery:
        return resultQuery[0]
    else:
        return None


def removePendingBlockNumber(blockNumber):
    queryExec(
        "DELETE FROM pending_block_number WHERE block_number=%s",
        False,
        blockNumber,
    )
