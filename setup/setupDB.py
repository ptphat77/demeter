import sys

# setting path
sys.path.append(".")

from config.connectDB import connectDB

conn = None
cur = None

try:
    conn = connectDB

    cur = conn.cursor()

    # Create contract table
    # BUG: UNIQUE(preprocess_bytecode)
    create_script = """
        CREATE TABLE IF NOT EXISTS contract (
            md5_index text NOT NULL,
            preprocess_bytecode text NOT NULL,
            vulnerabilities text NOT NULL,
            label bool NOT NULL,
            UNIQUE(md5_index)
        )
    """
    cur.execute(create_script)

    # Create last block number scanned table
    select_script = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name='start_block_number'
        )
    """
    cur.execute(select_script)
    resultQuery = cur.fetchone()

    isLastBlockBumberBcannedTableExists = resultQuery[0]
    if not isLastBlockBumberBcannedTableExists:
        create_script = """
            CREATE TABLE IF NOT EXISTS start_block_number (
                network_name varchar(20) NOT NULL,
                block_number int NOT NULL,
                UNIQUE(network_name)
            )
        """
        cur.execute(create_script)

        # add start_block_number default value is 0
        networkNames = ["mainnet", "goerli", "sepolia"]
        for network in networkNames:
            insert_script = """
                INSERT INTO start_block_number (network_name, block_number)
                VALUES ('{}',0);
            """.format(
                network
            )
            cur.execute(insert_script)

    print("Setup database successfully!!!")
    conn.commit()
except Exception as error:
    print(">>> database error: ", error)
finally:
    if cur != None:
        cur.close()
    if conn != None:
        conn.close()
