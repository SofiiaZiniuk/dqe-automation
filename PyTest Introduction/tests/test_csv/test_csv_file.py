import pytest
import re


def test_file_not_empty(csv_data):
    assert csv_data.empty == False, "CSV file is empty"

@pytest.mark.validate_csv
def test_validate_schema(csv_data, validate_schema):
    validate_schema(list(csv_data.columns), ['id', 'name', 'age', 'email', 'is_active'])

@pytest.mark.xfail(reason="This test is expected to fail due to duplicate rows in the CSV file")
@pytest.mark.validate_csv
def test_duplicates(csv_data):
    assert not csv_data.duplicated().any(), "CSV file contains duplicate rows"

@pytest.mark.skip(reason="This test should be skipped due to homework requirements")
@pytest.mark.validate_csv
def test_age_column_valid(csv_data):
    assert csv_data['age'].apply(lambda x: isinstance(x, int) and 0 <= x <= 100).all(), "Age column contains invalid values"

@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    assert csv_data['email'].apply(lambda x: re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', x) is not None).all(), "Email column contains invalid email addresses"

@pytest.mark.parametrize("id, is_active", [(1, False), (2, True)])
def test_active_players(id, is_active, csv_data):
    actual = csv_data[csv_data['id'] == id]['is_active'].iloc[0]
    assert actual == is_active, f"Expected is_active to be {is_active} for id={id}"


def test_active_player(csv_data):
    assert csv_data[csv_data['id'] == 2]['is_active'].iloc[0], "Expected is_active to be True for the second player"

