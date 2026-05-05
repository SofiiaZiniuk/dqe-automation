import pytest
import os
from src.connectors.file_system.parquet_reader import ParquetReader
from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager


def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost")
    parser.addoption("--db_port", action="store", default="5432")
    parser.addoption("--db_name", action="store", default="mydatabase")
    parser.addoption("--db_user", action="store", default=None)
    parser.addoption("--db_password", action="store", default=None)


def pytest_configure(config):
    required_envs = ["DB_USER", "DB_PASSWORD"]

    for env in required_envs:
        if not os.getenv(env):
            pytest.fail(f"Missing required env var: {env}")

@pytest.fixture(scope='session')
def db_connection():
    with PostgresConnectorContextManager(
        db_host=os.getenv("DB_HOST"),
        db_port=os.getenv("DB_PORT"),
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_password=os.getenv("DB_PASSWORD")
    ) as db:
        yield db


@pytest.fixture(scope="session")
def parquet_reader():
    return ParquetReader()

@pytest.fixture(scope="session")
def data_quality_library():
    return DataQualityLibrary