from utils.db_config import fetch_one_dict, fetch_all_dict


def load_test_data(test_id, table="TESTCASEMAIN"):
    table_name = table.upper()

    table_config = {
        "TESTCASEMAIN": "TEST_CASE_ID",
        "TESTACCOUNT": "ID",
        "TESTCASEDATA": "DATA_KEY_SEQ",
        "GRID_TESTCASEDATA": "DATA_KEY",
    }

    if table_name not in table_config:
        raise ValueError(f"허용되지 않은 테이블명: {table}")

    id_column = table_config[table_name]

    # TESTCASEDATA: 해당 DATA_KEY_SEQ의 모든 행을 읽어 {DATA_KEY: DATA} 맵으로 변환
    if table_name == "TESTCASEDATA":
        query = f"""
            SELECT DATA_KEY, DATA
            FROM {table_name}
            WHERE {id_column} = :test_id
        """
        rows = fetch_all_dict("test_db", query, {"test_id": test_id})

        if not rows:
            raise LookupError(f"[❌] {table_name}에서 {id_column}={test_id} 데이터가 없습니다.")

        # fetch_all_dict가 소문자 키(data_key, data)를 반환하므로 이를 매핑
        return {row["data_key"]: row["data"] for row in rows}

    # 일반 단일 행 테이블 (TESTCASEMAIN, TESTACCOUNT 등)
    else:
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE {id_column} = :test_id
        """
        data = fetch_one_dict("test_db", query, {"test_id": test_id})

        if data is None:
            raise LookupError(f"[❌] {table_name}에서 {id_column}={test_id} 데이터가 없습니다.")

        return data