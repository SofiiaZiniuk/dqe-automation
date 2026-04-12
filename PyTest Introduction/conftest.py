import pytest
import pandas as pd
import csv

# Fixture to read the CSV file by parameterized fixture
# Or we can do it using fixture that returns function that uses path_to_file as a parameter as I did for the next one
@pytest.fixture(scope='session', params=['src/data/data.csv'])
def csv_data(request):
    path_to_file = request.param
    df = pd.read_csv(path_to_file)
    return df

# Fixture to validate the schema of the file
@pytest.fixture(scope='session')
def validate_schema():
    def validate(actual_schema, expected_schema):
        assert list(actual_schema) == expected_schema, f"Expected schema: {expected_schema}, but got: {list(actual_schema)}"
    return validate

# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.own_markers:
            continue  # Skip already marked tests
        else:
            item.add_marker(pytest.mark.validate_csv)
