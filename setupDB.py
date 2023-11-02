from config.connectDB import connectDB

conn = None
cur = None

try:
    conn = connectDB

    cur = conn.cursor()

    # Create contract table
    create_script = """
        CREATE TABLE IF NOT EXISTS contract (
            address varchar(42) NOT NULL,
            preprocessBytecode text NOT NULL,
            label bool NOT NULL,
            UNIQUE(address, preprocessBytecode)
        )
    """
    cur.execute(create_script)

    # Create last block number scanned table
    select_script = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name='last_block_number_scanned'
        )
    """
    cur.execute(select_script)
    resultQuery = cur.fetchone()

    isLastBlockBumberBcannedTableExists = resultQuery[0]
    if not isLastBlockBumberBcannedTableExists:
        create_script = """
            CREATE TABLE IF NOT EXISTS last_block_number_scanned (
                id SERIAL PRIMARY KEY,
                block_number int NOT NULL
            )
        """
        cur.execute(create_script)

        insert_script = """
            INSERT INTO last_block_number_scanned (block_number)
            VALUES (0);
        """
        cur.execute(insert_script)

    conn.commit()
except Exception as error:
    print(">>> error: ", error)
finally:
    if cur != None:
        cur.close()
    if conn != None:
        conn.close()