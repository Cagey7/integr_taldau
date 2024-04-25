from django.db import connection

def select_index_data(index_table_name, dics_table_name, dates=None):
    if dates is not None:
        query =  f"SELECT value, date_taldau, date_periods.name FROM {index_table_name} JOIN date_periods ON date_period_id = id"
    else:
        query = f"SELECT value, date_taldau, date_period.name FROM {index_table_name} WHERE date_period_id IN({dates})"
    
    print(query)
    # Testing purposes
    print(index_table_name)
    print(dics_table_name)
    print(len(dics_table_name))

    with connection.cursor() as cursor:
        cursor.execute(query)
    # fetchall() returns a List of Tuples, so most likely value is index_data[n][0], date_taldau is [n][1], date_periods.name is [n][2]
        index_data = cursor.fetchall()
    # For every d_dic execute query 
        dics_data = []
        for dic in dics_table_name:
            cursor.execute(f"SELECT * FROM {dic}")    
            dics_data.append({dic: cursor.fetchall()})
    # Testing purposes
        print(type(index_data))
        print(type(dics_data))
    return index_data, dics_data