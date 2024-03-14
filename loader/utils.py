import requests

def get_all_catalogs():
    url_get_catalogs = f"https://taldau.stat.gov.kz/ru/Search/GetCatalogNodes"
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
    url_get_leaf = f"https://taldau.stat.gov.kz/ru/Search/getSearchPageGridData"
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
    url_get_periods = f"https://taldau.stat.gov.kz/ru/Search/GetPeriodNodes"
    response = requests.get(url_get_periods)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "error_code": response.status_code}
