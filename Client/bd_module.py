import sqlite3
import os
put = os.path.dirname(os.path.realpath(__file__)) + "/" #Путь- (part-1)

bd = sqlite3.connect(put + "content/user.db")
sql = bd.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS server (
    server_id INTEGER NOT NULL,
    server_name TEXT NOT NULL,
    adres TEXT NOT NULL,
    port INT(12) NOT NULL,
    ssl INT(1) NOT NULL,
    PRIMARY KEY (server_id AUTOINCREMENT)
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS user (
    id INTEGER,
    name TEXT,
    server_id INT,
    email TEXT,
    live_token TEXT,
    short_token TEXT,
    target INT(1),
    CONSTRAINT user_FK FOREIGN KEY (server_id) REFERENCES server (server_id)
)""")

def ls_server():
    sql.execute("SELECT * FROM server")
    server_list = sql.fetchall()
    return server_list

def ls_server_id(server_id):
    sql.execute("SELECT * FROM server WHERE server_id = ?", (server_id,))
    server_list = sql.fetchone()
    return server_list

def add_server(name, adres, port, ssl):
    sql.execute("""
        INSERT INTO server (server_name ,adres ,port,ssl)
        VALUES
        (?, ?, ?, ?)
    """, (name, adres, port, ssl))
    bd.commit()
    sql.execute("SELECT last_insert_rowid()")
    a = sql.fetchone()
    print(a)
    return a[0]

def add(id, name, server_id, email, live_token, short_token):
    sql.execute("""
        INSERT INTO user
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
    """, (id, name, server_id, email, live_token, short_token, 1))
    bd.commit()

def add_2(id, name, server, port, ssl, email, live_token, short_token):
    sql.execute("""
        INSERT INTO user
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
    """, (id, name, server, email, live_token, short_token, 1))
    bd.commit()


def ls():
    sql.execute("SELECT * FROM user")
    user_list = sql.fetchall()
    return user_list
def ls_user():
    sql.execute("SELECT id, name, target FROM user")
    user_list = sql.fetchall()
    return user_list

def ls_token(id):
    sql.execute("SELECT live_token, short_token FROM user WHERE id = ?", (id,))
    user_list = sql.fetchone()
    return user_list

def ls_user_target(id):
    #print(id)
    sql.execute("SELECT * FROM user LIMIT ?", (id+1,))
    user_list = sql.fetchall()
    return user_list[len(user_list)-1]

def token_update(id, live_token, short_token, server_id):
    sql.execute("UPDATE user SET live_token = ?, short_token = ? WHERE id = ? AND server_id = ?", (live_token, short_token, id, server_id))
    bd.commit()

def add_2(id, name, server, email, live_token, short_token):
    sql.execute("""
        INSERT INTO user
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
    """, (id, name, server, email, live_token, short_token, 1))
    bd.commit()

def rm(id, server_id):
    sql.execute("DELETE FROM user WHERE id = ? AND server_id = ?", (id,server_id))
    bd.commit()

def rm_server(server_id):
    sql.execute("DELETE FROM server WHERE server_id = ?", (server_id,))
    bd.commit()


def user_id_check(user_id, server_id):
    sql.execute("SELECT id, live_token, server_id FROM user WHERE id = ? AND server_id = ?", (user_id,server_id))
    user_list = sql.fetchone()
    #print(f"AAA - {user_list}")
    return user_list

def target(id, server_id):
    sql.execute("UPDATE user SET target = 0")
    sql.execute("UPDATE user SET target = 1 WHERE id = ? AND server_id = ?", (id,server_id))
    bd.commit()

def ls_user_on_server(server_id):
    sql.execute("SELECT id, name, target FROM user WHERE server_id = ?", (server_id))
    user_list = sql.fetchall()
    return user_list


