"""Application settings and environment configuration."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
	"""Pydantic settings for application configuration."""

	APP_ENV: str = "local"
	POSTGRES_DB: str
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	PGHOST: str
	PGPORT: int
	LOG_LEVEL: str | None = None

	# SMTP / Email settings (MailHog defaults)
	SMTP_HOST: str = "localhost"
	SMTP_PORT: int = 1025
	SMTP_FROM: str = "david.serban@endava.com"
	SMTP_TLS: bool = False
	SMTP_USERNAME: str | None = None
	SMTP_PASSWORD: str | None = None

	# JWT / Auth settings
	JWT_SECRET_KEY: str = "dev-change-me"  # Replace in production
	JWT_ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
	REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

	@property
	def DATABASE_URL(self) -> str:
		"""Build the SQLAlchemy database URL from settings."""
		return (
			f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
			f"@{self.PGHOST}:{self.PGPORT}/{self.POSTGRES_DB}"
		)

	class Config:
		env_file = Path(__file__).resolve().parent.parent / ".env" 
		extra = "ignore"


settings = Settings()
