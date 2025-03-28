import sqlite3 as sq

data_base = sq.connect("user.db")
cur = data_base.cursor()

cur.executescript("""
BEGIN;
CREATE TABLE
IF NOT EXISTS
User(id INTEGER PRIMARY KEY, login TEXT, password TEXT, fio TEXT, role TEXT);
CREATE TABLE
IF NOT EXISTS
Request(id INTEGER PRIMARY KEY, date DATE, equipment TEXT, defect TEXT, description, client TEXT);
COMMIT;
""")
data_base.commit()

def get_from_db(
        fields, 
        table, 
        where = ""
    ):
    """
    fields - ["","",]
    table - User
    where = login = "{var}"
    
    """
    fields = ",".join(fields)
    log_in_values = cur.execute(f"""
    SELECT {fields}
    FROM {table}
    WHERE {where}    
    """)
    return log_in_values.fetchall()

def insert_value(login, password, fio):
    cur.execute(f"""
    INSERT INTO User(login, password, fio) 
    VALUES("{login}", "{password}", "{fio}")
    """)
    data_base.commit()

def send_request(date, equipment, defect, description, client):
    cur.execute(f"""
    INSERT INTO Request(Date, equipment, defect, description, client)
    VALUES('{date}','{equipment}','{defect}','{description}','{client}')
    """)
    data_base.commit()

def check_and_get_user(login):
    user = cur.execute(f'SELECT id from User WHERE login="{login}"').fetchone()
    if user:
        return user[0]
    else:
        return None

def search_user_for_login(login, password):
    user = cur.execute(f'SELECT id from User WHERE login="{login}" AND password="{password}"').fetchone()
    if user:
        return user[0]
    else:
        return None
    
def search_user_for_fio(login, password, fio):
    print(login, password, fio)
    fio = "qq"
    user = cur.execute(f'SELECT * from User WHERE login="{login}" AND password="{password}" AND fio="{fio}"').fetchone()
    print(4, user)
    print(fio)
    
    user = cur.execute(f'SELECT * from User WHERE fio="{fio}"').fetchone()
    print(3, user)
    
    user = cur.execute(f'SELECT * from User WHERE login="{login}"').fetchone()
    print(2, user)
    
    user = cur.execute(f'SELECT * from User WHERE password="{password}"').fetchone()
    print(1,user)
    if user:
        return user[3]
    else:
        return None


def check_log_in():
    log_in_values = cur.execute(f"""
    SELECT login, password
    FROM User
    """).fetchall()
    print(log_in_values)

def request_from_db(client):
    request_data = cur.execute(f'SELECT * FROM Request WHERE client = "{client}"').fetchall()
    return request_data

def update_values(req_id, equipment, defect, description):
    cur.execute(f"""
    UPDATE Request SET equipment = "{equipment}", defect="{defect}", description="{description}" WHERE id = {req_id}
    """)
    data_base.commit()
    q = cur.execute(f"""SELECT * from Request WHERE id = "{req_id}" 
                """).fetchall()
    print(q)

