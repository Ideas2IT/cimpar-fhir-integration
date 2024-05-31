from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    AIDBOX_URL: str = os.getenv("AIDBOX_URL")
    AIDBOX_SERVER_URL: str = os.getenv("AIDBOX_SERVER_URL")
    AIDBOX_CLIENT_USERNAME: str = os.getenv("AIDBOX_CLIENT_USERNAME")
    AIDBOX_CLIENT_PASSWORD: str = os.getenv("AIDBOX_CLIENT_PASSWORD")

settings = Settings()