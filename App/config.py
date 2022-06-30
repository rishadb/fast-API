from pydantic import BaseSettings #for the defenition of settings schema class

class Settings(BaseSettings):
    database_hostname: str # = default_val can be added here for all fields
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    class Config: #to connect to .env file
        env_file = ".env"
#.env file: in production, we set these vals on machine,var name is here in caps, but pydantic looks at varname at case insensitive perspective
#put the .env files in git ignore to not upload to git

settings = Settings()