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


def getStartBlockNumber(networkName):
    resultQuery = queryExec(
        "SELECT block_number FROM start_block_number WHERE network_name='{}'".format(networkName)
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


def updateStartBlockNumber(networkName, blockNumber):
    queryExec(
        "UPDATE start_block_number SET block_number={} WHERE network_name='{}'".format(
            blockNumber, networkName
        ),
        False,
    )
