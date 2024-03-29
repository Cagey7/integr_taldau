import requests
import re

taldau_url = "https://taldau.stat.gov.kz/ru"

def get_all_catalogs():
    url_get_catalogs = f"{taldau_url}/Search/GetCatalogNodes"
    response = requests.get(url_get_catalogs)
    if response.status_code == 200:
        catalogs = response.json()
    else:
        return {"status": "error", "error_code": response.status_code}

    catalogs_list = []
    for row in catalogs:
        catalogs_data = get_node_chapter_data(row)
        catalogs_list += catalogs_data
    
    return catalogs_list


def get_node_chapter_data(data, parent_id=None):
    category_data = []
    if isinstance(data, dict):
        if "id" in data and "text" in data:
            category_data.append((data["id"], data["text"], parent_id))
        parent_id = data.get("id", parent_id)
        for value in data.values():
            category_data.extend(get_node_chapter_data(value, parent_id))
    elif isinstance(data, list):
        for item in data:
            category_data.extend(get_node_chapter_data(item, parent_id))
    return category_data


def get_all_indices(chapter_ids, period_ids):
    url_get_leaf = f"{taldau_url}/Search/getSearchPageGridData"
    payload = {
        "pid": -1,
        "tree": chapter_ids,
        "periods": period_ids,
        "page": 1,
        "start": 0,
        "limit": 100000,
    }
    response = requests.post(url_get_leaf, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def get_all_periods():
    url_get_periods = f"{taldau_url}/Search/GetPeriodNodes"
    response = requests.get(url_get_periods)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def get_index_attributes(index_id):
    url_get_name = f"{taldau_url}/Api/GetIndexAttributes?indexId={index_id}"     
    response = requests.get(url_get_name)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def get_index_periods(index_id):
    url_get_period = f"{taldau_url}/Api/GetPeriodList?indexId={index_id}"
    response = requests.get(url_get_period)
    if response.status_code == 200:
        return response.json()
    else: 
        return {"status": "error", "error_code": response.status_code}


def get_index_segment(index_id, period_id):
    url_get_segment = f"{taldau_url}/Api/GetSegmentList?indexId={index_id}&periodId={period_id}"
    response = requests.get(url_get_segment)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def convert_to_list(input_str):
    try:
        splitter = re.findall(r"[\+\,\/]", input_str)[0]
        try:
            return [int(num.strip()) for num in input_str.split(splitter)]
        except:
            return [num.strip() for num in input_str.split(splitter)]
    except:
        try:
            return [int(input_str)]
        except:
            return [input_str]


def create_dic_table(cursor, dic_id):
    create_dic = f"""
    CREATE TABLE IF NOT EXISTS dics_data.d_{dic_id} (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    );
    """
    cursor.execute(create_dic)


def create_index_table(cursor, index_id, period_id, dic_ids):
    periods_data_table = ""
    rows_data_table = ""
    fk_data_table = ""
    if period_id == 7 or period_id == 12 or period_id == 16:
        periods_data_table += "year INTEGER,"
    elif period_id == 5 or period_id == 9:
        periods_data_table += "year INTEGER, quarter INTEGER,"
    elif period_id == 6 or period_id == 10:
        periods_data_table += "year INTEGER, half_year INTEGER,"
    elif period_id == 4 or period_id == 8:
        periods_data_table += "year INTEGER, month INTEGER,"
    
    for dic_id in dic_ids:
        rows_data_table += f"d_{dic_id}_id INTEGER,"
        fk_data_table += f"FOREIGN KEY (d_{dic_id}_id) REFERENCES dics_data.d_{dic_id}(id),"
    
    index_table_name = f"index_data.i_{index_id}_p_{period_id}_d_{'_'.join(map(str, dic_ids))}"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {index_table_name} (
        value NUMERIC,
        date_taldau DATE,
        created DATE,
        date_period_id INTEGER,
        {periods_data_table}
        {rows_data_table}
        {fk_data_table}
        FOREIGN KEY (date_period_id) REFERENCES date_periods(id)
    );
    """
    cursor.execute(create_table_query)


def get_index_dates(index_id, period_id, term_ids, dic_ids):
    url_get_dates = f"""
        {taldau_url}/Api/GetIndexPeriods?p_measure_id=1
        &p_index_id={index_id}
        &p_period_id={period_id}
        &p_terms={term_ids}
        &p_term_id=741880&p_dicIds={dic_ids}
    """
    response = requests.get(url_get_dates)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def get_index_data(index_id, period_id, dic_ids, date_ids):
    url_get_periods = f"{taldau_url}/Api/GetIndexData/{index_id}?period={period_id}&dics={dic_ids}&dateIds={date_ids}"
    response = requests.get(url_get_periods)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}


def insert_term(cur, dic_id, term_id, term_name):
    get_term = "SELECT * FROM dics_data.d_{} WHERE id = %s;".format(dic_id)
    cur.execute(get_term, (term_id,))
    check_term = cur.fetchone()
    if not check_term:
        insert_term_query = """
        INSERT INTO dics_data.d_{} (id, name)
        VALUES (%s, %s);
        """.format(dic_id)
        data_for_term = (term_id, term_name)
        cur.execute(insert_term_query, data_for_term)


def get_period_values(period_id, taldau_date):
    if period_id == 7 or period_id == 12 or period_id == 16:
        return [taldau_date.year]
    elif period_id == 5 or period_id == 9:
        if taldau_date.month == 3:
            quarter = 1
        elif taldau_date.month == 6:
            quarter = 2
        elif taldau_date.month == 9:
            quarter = 3
        elif taldau_date.month == 12:
            quarter = 4
        return [taldau_date.year, quarter]
    elif period_id == 6 or period_id == 10:
        if taldau_date.month == 6:
            half_year = 1
        if taldau_date.month == 12:
            half_year = 2
        return [taldau_date.year, half_year]
    elif period_id == 4 or period_id == 8:
        return [taldau_date.year, taldau_date.month]
    else:
        return []


def insert_index_data(cur, index_id, period_id, dic_ids, data):
    index_table_name = f"index_data.i_{index_id}_p_{period_id}_d_{'_'.join(map(str, dic_ids))}"
    insert_dics_list = ""
    index_name_period = ""
    for i, dic in enumerate(dic_ids):
        if i == len(dic_ids) - 1:
            insert_dics_list += f"d_{dic}_id"
        else:
            insert_dics_list += f"d_{dic}_id,"
    
    insert_num_values = ",".join(["%s"] * len(data))

    if period_id == 7 or period_id == 12 or period_id == 16:
        index_name_period += "year,"
    elif period_id == 5 or period_id == 9:
        index_name_period += "year, quarter,"
    elif period_id == 6 or period_id == 10:
        index_name_period += "year, half_year,"
    elif period_id == 4 or period_id == 8:
        index_name_period += "year, month,"



    insert_data = """
    INSERT INTO {} (value, date_taldau, created, date_period_id, {} {})
    VALUES ({});
    """.format(index_table_name, index_name_period, insert_dics_list, insert_num_values)
    cur.execute(insert_data, data)
