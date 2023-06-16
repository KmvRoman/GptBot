from attrs import define, field
from omegaconf import MISSING
from pydantic import PostgresDsn


@define
class Bot:
    token: str = MISSING
    use_redis: bool = MISSING


@define
class Database:
    user: str = MISSING
    password: str = MISSING
    db_name: str = MISSING
    host: str = MISSING

    connection_uri: str = field(default="")

    def __attrs_post_init__(self) -> None:
        sync_connection_url = PostgresDsn.build(
            scheme="postgresql",
            user=self.user,
            password=self.password,
            host=self.host,
            path=f"/{self.db_name or ''}",
        )
        self.connection_uri = sync_connection_url.replace("postgresql", "postgresql+asyncpg")


@define
class OpenAiApi:
    key: str = MISSING
    chat_completion_url: str = MISSING


@define
class Config:
    tg_bot: Bot = Bot()
    database: Database = Database()
    openai: OpenAiApi = OpenAiApi()
