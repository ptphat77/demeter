import psycopg2
from checkEnvironment import variableEnv

connectDB = psycopg2.connect(
    host=variableEnv["POSTGRES_URL"],
    dbname=variableEnv["POSTGRES_DATABASE_NAME"],
    user=variableEnv["POSTGRES_USERNAME"],
    password=variableEnv["POSTGRES_PASSWORD"],
    port=variableEnv["POSTGRES_PORT"],
)

if connectDB.status:
    print("Connecting to database successfully")
else:
    print("Connecting to database failed")
