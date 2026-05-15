from pydantic_settings import BaseSettings, SettingsConfigDict

class MySettings (BaseSettings):
    my_dataBase_url : str
    My_JWT_secret : str
    My_JWT_algorithm : str
    REDIS_HOST : str
    REDIS_PORT : int
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    DOMAIN: str
    BROKER_URL : str = "redis://localhost:6379/1"
    RESULTS_BACKEND_URL : str = "redis://localhost:6379/2"
    
    # model_config is Keyword.
    model_config = SettingsConfigDict(
    env_file= ".env",
    extra="ignore"
    )

my_config =MySettings()




