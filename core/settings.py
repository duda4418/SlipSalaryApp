"""Application settings and environment configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	"""Pydantic settings for application configuration."""

	APP_ENV: str = "local"
	POSTGRES_DB: str
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	PGHOST: str
	PGPORT: int
	LOG_LEVEL: str | None = None

	@property
	def DATABASE_URL(self) -> str:
		"""Build the SQLAlchemy database URL from settings."""
		return (
			f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
			f"@{self.PGHOST}:{self.PGPORT}/{self.POSTGRES_DB}"
		)

	class Config:
		env_file = ".env"
		extra = "ignore"


settings = Settings()
