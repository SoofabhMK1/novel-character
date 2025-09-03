from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import model_validator, PostgresDsn

class Settings(BaseSettings):
    """
    应用程序的配置模型。
    Pydantic V2 会自动从环境变量或 .env 文件中读取这些值。
    """
    # Application Port
    API_PORT: int = 8001

    # PostgreSQL Database Configuration
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # The full database connection URL.
    # This field is assembled automatically from the other DB settings.
    DATABASE_URL: Optional[str] = None

    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        """
        在 Pydantic 完成对其他字段的验证后，动态构建 DATABASE_URL。
        这是 Pydantic V2 的推荐做法。
        """
        if self.DATABASE_URL:
            # 如果 DATABASE_URL 已被显式提供，则直接使用它
            return self

        # 手动构建数据库连接 URL 字符串
        self.DATABASE_URL = (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        # Pydantic 会自动验证这个字符串是否符合 PostgresDsn 的格式
        return self

    class Config:
        # env_file = "../.env"
        pass

# 创建一个全局可用的配置实例
settings = Settings()