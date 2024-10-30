from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_NAME: str

    class Config:
        env_file = '../.env'


config = Settings(BOT_TOKEN='6241229619:AAEdftuk2GqMTqy2HJ4clKMo625DxbH6ppM',BOT_NAME='inglishbotsnewsbot')
