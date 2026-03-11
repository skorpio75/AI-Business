"""Apply latest Alembic migrations for local development."""

from alembic import command
from alembic.config import Config


if __name__ == "__main__":
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")
    print("database_migrated")
