from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_env: str = Field(default="dev", alias="APP_ENV")

    sqlserver_host: str = Field(alias="SQLSERVER_HOST")
    sqlserver_db: str = Field(alias="SQLSERVER_DB")
    sqlserver_auth: str = Field(default="windows", alias="SQLSERVER_AUTH")

    sqlserver_user: str | None = Field(default=None, alias="SQLSERVER_USER")
    sqlserver_password: str | None = Field(default=None, alias="SQLSERVER_PASSWORD")

    sqlserver_driver: str = Field(default="ODBC Driver 17 for SQL Server", alias="SQLSERVER_DRIVER")
    sqlserver_trust_cert: bool = Field(default=True, alias="SQLSERVER_TRUST_CERT")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()