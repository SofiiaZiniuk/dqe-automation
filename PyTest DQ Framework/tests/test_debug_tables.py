def test_debug_tables(db_connection):
    df = db_connection.get_data_sql("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    print(df)
    assert not df.empty