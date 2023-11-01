from dotenv import dotenv_values, load_dotenv

# Check production or development environment
isDevelopment = load_dotenv(".env.development")
variableEnv = ""
if isDevelopment:
    variableEnv = dotenv_values(".env.development")
else:
    variableEnv = dotenv_values(".env.production")
export = variableEnv
