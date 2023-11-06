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
        print(">>> database error: ", error)
        print(">>> queryScript: ", " ".join((queryScript.split())[:2]), "...")


def getStartBlockNumber():
    resultQuery = queryExec(
        "SELECT block_number FROM last_block_number_scanned LIMIT 1"
    )
    return resultQuery[0]


def isExistsPreprocessedBytecode(preprocessedBytecode):
    resultQuery = queryExec(
        "SELECT label FROM contract WHERE md5_index = md5('{}'::text)".format(
            preprocessedBytecode
        )
    )

    return resultQuery


def insertContractInfoToDB(preprocessedBytecode, vulnerabilities, label):
    queryExec(
        """ INSERT INTO contract (md5_index, preprocess_bytecode, vulnerabilities, label)
            VALUES (md5('{}'::text), '{}'::text, '{}'::text, {}::bool)
        """.format(
            preprocessedBytecode, preprocessedBytecode, vulnerabilities, str(label)
        ),
        False,
    )


def updateStartBlockNumber(blockNumber):
    queryExec(
        "UPDATE last_block_number_scanned SET block_number={} WHERE id=1 RETURNING block_number".format(
            blockNumber
        ),
        False,
    )
