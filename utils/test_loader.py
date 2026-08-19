from utils.db_config import fetch_one_dict

# def load_test_data(test_id, table="pilot_data"):
#     allowed_tables = {"pilot_data", "pilot_pf_data"}
#     assert table in allowed_tables, f"허용되지 않은 테이블명: {table}"

#     data = fetch_one_dict("test_db", f"SELECT * FROM {table} WHERE test_id = %s", (test_id,))
#     assert data is not None, f"[❌] test_id={test_id}에 해당하는 테스트 데이터가 없습니다."
#     return data

def load_test_data(test_id, table="pilot_data"):
    table_name = table.upper()

    table_config = {
        "PILOT_DATA": "TEST_ID",
        "PILOT_PF_DATA": "TEST_ID",
        "TEST_ADD_RULE": "ID",
        "TEST_LOGIN": "ID",
    }

    if table_name not in table_config:
        raise ValueError(
            f"허용되지 않은 테이블명: {table}"
        )

    id_column = table_config[table_name]

    query = f"""
        SELECT *
        FROM {table_name}
        WHERE {id_column} = :test_id
    """

    data = fetch_one_dict(
        "test_db",
        query,
        {"test_id": test_id}
    )

    if data is None:
        raise LookupError(
            f"[❌] {table_name}에서 "
            f"{id_column}={test_id}에 해당하는 "
            "테스트 데이터가 없습니다."
        )

    return data