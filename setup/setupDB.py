import sys

# setting path
sys.path.append(".")


from config.connectDB import connectDB

conn = None
cur = None

try:
    conn = connectDB

    cur = conn.cursor()

    # Create contract_dataset table
    create_script = """
        CREATE TABLE IF NOT EXISTS contract_dataset (
            address varchar(42) NOT NULL,
            md5_index text NOT NULL,
            preprocess_bytecode text NOT NULL,
            vulnerabilities text NOT NULL,
            label bool NOT NULL,
            UNIQUE(md5_index)
        )
    """
    cur.execute(create_script)

    # Create contract_info table
    create_script = """
        CREATE TABLE IF NOT EXISTS contract_info (
            address varchar(42) NOT NULL,
            source_code text NOT NULL,
            bytecode text NOT NULL,
            abi text NOT NULL,
            UNIQUE(address)
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

    # Create pending_block_number table
    create_script = """
        CREATE TABLE IF NOT EXISTS pending_block_number (
            block_number int NOT NULL,
            time TIMESTAMP NOT NULL,
            UNIQUE(block_number)
        )
    """
    cur.execute(create_script)

    print("Setup database successfully!!!")
    conn.commit()
except Exception as error:
    print(">>> database error: ", error)
finally:
    if cur != None:
        cur.close()
    if conn != None:
        conn.close()
