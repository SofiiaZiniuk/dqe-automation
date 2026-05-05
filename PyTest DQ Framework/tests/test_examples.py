import pytest


@pytest.fixture(scope='module')
def source_data(db_connection):
    source_query = """
    SELECT * FROM example_table
    """
    return db_connection.get_data_sql(source_query)


@pytest.fixture(scope='module')
def target_data(parquet_reader):
    target_path = 'data/example.parquet'
    return parquet_reader.read_parquet(target_path)


@pytest.mark.example
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.example
def test_check_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)