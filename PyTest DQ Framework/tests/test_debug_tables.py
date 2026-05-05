def test_debug_tables(db_connection):
    df = db_connection.get_data_sql("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type='BASE TABLE'
    """)

    print(df)
    assert not df.empty