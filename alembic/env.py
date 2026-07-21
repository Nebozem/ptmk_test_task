import asyncio
from logging.config import fileConfig

from alembic import context

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.database.database import Base
from app.core.config import settings


# Alembic Config object
config = context.config


# Берём URL базы из настроек приложения
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace(
        "postgresql+asyncpg",
        "postgresql+asyncpg"
    )
)


# Настройка логирования Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Метаданные моделей для autogenerate
target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


asyncio.run(run_migrations_online())