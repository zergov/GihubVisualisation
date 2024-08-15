from pydantic import BaseSettings

class Settings(BaseSettings):
    title: str = "Github Repo Commit Fetcher API"
    description: str = "API fetching commits from a given github repo"
    version: str = "0.0.1"

    class Config:
        env_file = ".env"