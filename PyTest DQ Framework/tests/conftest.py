import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager


def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost")
    parser.addoption("--db_port", action="store", default="5432")
    parser.addoption("--db_name", action="store", default="mydatabase")
    parser.addoption("--db_user", action="store", default=None)
    parser.addoption("--db_password", action="store", default=None)


def pytest_configure(config):
    required = ["db_user", "db_password"]

    for opt in required:
        if not config.getoption(f"--{opt}"):
            pytest.fail(f"Missing required option: {opt}")


@pytest.fixture(scope="session")
def db_connection(request):
    host = request.config.getoption("--db_host")
    port = request.config.getoption("--db_port")
    name = request.config.getoption("--db_name")
    user = request.config.getoption("--db_user")
    password = request.config.getoption("--db_password")

    with PostgresConnectorContextManager(
        db_host=host,
        db_port=port,
        db_name=name,
        db_user=user,
        db_password=password
    ) as db:
        yield db