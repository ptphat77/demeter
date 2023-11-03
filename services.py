from config.connectDB import connectDB


def getStartBlockNumber():
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        select_script = """
            SELECT block_number from last_block_number_scanned LIMIT 1
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


def insertContractInfoToDB(contractAddress, contractBytecode, label):
    conn = None
    cur = None
    try:
        conn = connectDB

        cur = conn.cursor()

        # "ON CONFLICT DO NOTHING" handle duplicate contract address and contract preprocessBytecode
        # scan block again => duplicate contract address
        # preprocessBytecode, merge operations => duplicate contract preprocessBytecode
        insert_script = """
            INSERT INTO contract (address, preprocess_bytecode, label)
            VALUES ('{}'::varchar, '{}'::text, {}::bool)
            ON CONFLICT DO NOTHING
            returning address
        """.format(
            contractAddress, contractBytecode, str(label)
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
