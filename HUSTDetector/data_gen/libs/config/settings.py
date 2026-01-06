import os
from dotenv import load_dotenv

class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.load_settings()
        return cls._instance

    def load_settings(self):
        load_dotenv()
        self.__OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    @property
    def OPENAI_API_KEY(self) -> str:
        return self.__OPENAI_API_KEY


settings = Settings()
