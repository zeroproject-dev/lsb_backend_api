from database.db import db


def get_user_with_permissions(id: int):
    sql_query = """SELECT tm.name, GROUP_CONCAT(tp.name SEPARATOR ',') as
permissions  FROM T_ROLE_PERMISSION trp
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
