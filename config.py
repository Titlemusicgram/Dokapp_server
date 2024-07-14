from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL: str

    @property
    def db_url(self):
        return f"{self.POSTGRES_URL}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

dokapp_temp = "/tmp"
photo_title_lenght = 80
