from database.db import db


def get_permissions_of_role(id: int):
    sql_query = """SELECT tm.name, GROUP_CONCAT(LOWER(tp.name) SEPARATOR ',') as permissions  FROM T_ROLE_PERMISSION trp
LEFT JOIN T_PERMISSION tp ON tp.id  = trp.permission_id
LEFT JOIN T_MODULE tm ON tm.id = tp.module_id
WHERE trp.role_id = :role_id AND tm.state = 'active' AND tp.state = 'active'
GROUP BY tm.name;"""
    res = db.session.execute(sql_query, {"role_id": id})

    json = {}

    for row in res:
        module, permissions = row
        json[module] = permissions.split(',')

    return json


def get_all_modules_permissions():
    sql_query = """SELECT tm.name, GROUP_CONCAT(tp.name SEPARATOR ', ') as permissions from T_MODULE tm 
left join T_PERMISSION tp ON tp.module_id = tm.id
GROUP BY tm.name;"""
    res = db.session.execute(sql_query)

    json = {}

    for row in res:
        module, permissions = row
        json[module] = permissions.split(', ')

    return json


def get_module_permissions(id: int):
    sql_query = """SELECT tm.name, GROUP_CONCAT(tp.name SEPARATOR ', ') as permissions from T_MODULE tm 
left join T_PERMISSION tp ON tp.module_id = tm.id
WHERE tm.id = :m_id
GROUP BY tm.name;"""

    res = db.session.execute(sql_query, {"m_id": id})

    json = {}

    for row in res:
        module, permissions = row
        json[module] = permissions.split(', ')

    return json
