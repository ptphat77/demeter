from config.connectDB import connectDB


def getStartBlockNumber():
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        select_script = """
            SELECT block_number FROM last_block_number_scanned LIMIT 1
        """
        cur.execute(select_script)
        resultQuery = cur.fetchone()

        conn.commit()

        return resultQuery[0]
    except Exception as error:
        print(">>> database error: ", error)
    finally:
        if cur != None:
            cur.close()
        if conn != None:
            conn.close()


def isExistsPreprocessedBytecode(preprocessedBytecode):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        select_script = """
            SELECT label FROM contract WHERE preprocess_bytecode = '{}'
        """.format(
            preprocessedBytecode
        )
        cur.execute(select_script)
        resultQuery = cur.fetchone()

        conn.commit()

        return resultQuery
    except Exception as error:
        print(">>> database error: ", error)


def insertContractInfoToDB(preprocessedBytecode, vulnerabilities, label):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        insert_script = """
            INSERT INTO contract (preprocess_bytecode, vulnerabilities, label)
            VALUES ('{}'::text, '{}'::text, {}::bool)
        """.format(
            preprocessedBytecode, vulnerabilities, str(label)
        )
        cur.execute(insert_script)

        conn.commit()
    except Exception as error:
        print(">>> database error: ", error)


def updateStartBlockNumber(blockNumber):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        update_script = """
            UPDATE last_block_number_scanned SET block_number={} WHERE id=1
        """.format(
            blockNumber
        )
        cur.execute(update_script)

        conn.commit()
    except Exception as error:
        print(">>> database error: ", error)
