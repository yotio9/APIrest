from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")


    TOKEN: str =Field(default="")
    DATABASE_URL: str
    JWT_SECRET: str

settings=Setting()