import os

from time import strftime #Для (Time)
import random

# + Просмотор предметов.            ls_item(user_id)
# + Просмотор пользователей.        ls_user(user_id)
# + Информация о пользователе.      user_info(user_id,user_id_rec)
# ? - Информация о предмете.        item_info(user_id,item_id)
# + Редактирование пользователя.    user_edit(user_id,user_id_rec, user_name, email, password, avatar, active, group_id)
# - Редактирование пользователя (Подгруппы).
# + Редактирование предмета.        item_edit(user_id, item_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id)
# + Создание пользователя.          user_add(user_id, user_name, email, password, avatar, active, group_id)
# + Создание предмета.              add_item(user_id, user_id_2, name, status, icon, comments, inventory_id)
# ! - Удоление пользователя.
# + Удоление предмета.              rm_item(user_id,item_id)
# - Создание груп.
# + Просмотор груп.                 ls_group(user_id)





import secrets

IP = "127.0.0.1"

# BEGIN mariadb
import mariadb
import sys
pool = mariadb.ConnectionPool(user="recording_spark",password="",host=IP,port=3306,pool_name="web-app",pool_size=1)
try:
    bd = pool.get_connection()
except mariadb.PoolError as e:
    print(f"Error opening connection from pool: {e}")

sql = bd.cursor() ## TODO SAS
# BEGIN bd CREATE
sql.execute("""
    CREATE TABLE IF NOT EXISTS recording_spark.group (
    group_id INT NOT NULL AUTO_INCREMENT,
    name TEXT,
    rights INT(12) NOT NULL,
    PRIMARY KEY (group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS recording_spark.user (
    user_id INT(24) NOT NULL AUTO_INCREMENT,
    user_name TEXT NOT NULL,
    email TEXT,
    password TEXT,
    avatar tinyint(1) NOT NULL DEFAULT 0,
    active tinyint(1) NOT NULL DEFAULT 0,
    group_id INT NOT NULL,
    PRIMARY KEY (user_id),
    KEY user_FK (group_id),
    CONSTRAINT user_FK FOREIGN KEY (group_id) REFERENCES recording_spark.group (group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

""")

sql.execute("""
    CREATE TABLE IF NOT EXISTS recording_spark.item (
    item_id INT(24) NOT NULL AUTO_INCREMENT,
    item_name TEXT NOT NULL,
    status TEXT,
    user_id_1 INT(24) NOT NULL,
    user_id_2 INT(24) NOT NULL,
    icon TEXT DEFAULT NULL,
    comments TEXT,
    inventory_id bigint,
    PRIMARY KEY (item_id),
    KEY item_FK (user_id_1),
    KEY item_FK_1 (user_id_2),
    CONSTRAINT item_FK FOREIGN KEY (user_id_1) REFERENCES recording_spark.user (user_id),
    CONSTRAINT item_FK_1 FOREIGN KEY (user_id_2) REFERENCES recording_spark.user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS recording_spark.ownership_over_group (
    group_id INT NOT NULL,
    user_id INT(24) NOT NULL,
    KEY group_id (group_id),
    KEY user_id (user_id),
    CONSTRAINT ownership_over_group_ibfk_1 FOREIGN KEY (group_id) REFERENCES  recording_spark.group (group_id),
    CONSTRAINT ownership_over_group_ibfk_2 FOREIGN KEY (user_id) REFERENCES   recording_spark.user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

""")
# END

#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.user (user_id INT, user_name TEXT, email TEXT, password TEXT, avatar TEXT, active BOOL, group_id INT)")
#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.group (group_id INT, name TEXT, user_id INT, permission BIGINT)") # group 1 - отправитель, 2 - user, 3 - admin
#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.item (item_id INT NOT NULL AUTO_INCREMENT, item_name TEXT, status TEXT, user_id_1 INT, user_id_2 INT, png_id_name TEXT, comments TEXT, inventory_id BIGINT, PRIMARY KEY (item_id))")


#sql.execute("""
#CREATE TABLE IF NOT EXISTS recording_spark.ownership_over_group (
#group_id INT NOT NULL, user_id INT NOT NULL,
#FOREIGN KEY (group_id) REFERENCES recording_spark.group(group_id),
#FOREIGN KEY (user_id) REFERENCES recording_spark.user(user_id))

#""")

#sql.execute("ALTER TABLE recording_spark.user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci") # Смена кодировки!
#sql.execute("ALTER TABLE recording_spark.group CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci") # Смена кодировки!
#sql.execute("ALTER TABLE recording_spark.item CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci") # Смена кодировки!


#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.user_group (id INT NOT NULL AUTO_INCREMENT, group_id INT, PRIMARY KEY (id))")
#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.user_group_2 (id INT NOT NULL AUTO_INCREMENT, user_id INT, FOREIGN KEY (id) REFERENCES recording_spark.user_group(id))")

#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.user_group (group_id INT NOT NULL AUTO_INCREMENT, user_id INT NOT NULL AUTO_INCREMENT, FOREIGN KEY (group_id, user_id) REFERENCES recording_spark.group(group_id, user_id))")


#sql.execute("CREATE TABLE IF NOT EXISTS recording_spark.user_group_2 (id INT NOT NULL AUTO_INCREMENT, user_id INT, FOREIGN KEY (id) REFERENCES recording_spark.user(user_id))")

# (SELECT group_id FROM recording_spark.user_group WHERE recording_spark.user_group.user_id = ?)
user_id = 2

# SELECT group_id FROM recording_spark.group WHERE recording_spark.user_group.user_id = ?) <= group_id

# SELECT MAX(group_id) FROM recording_spark.group WHERE recording_spark.group.item = 5 AND group_id IN (SELECT group_id FROM recording_spark.user_group WHERE recording_spark.user_group.user_id = ?)

#DECLARE SSS INT(11);




# Есть пользователи.
# Есть админестраторы.
# У польователей есть группы, а у админестраторов их нет.
# У каждого есть группа и она может быть только 1.
# У также у каждого есть спиок груп которые может польователь метья и упровлять.
# У Обычных польователей неттаких груп, а у администраторов они есть.
"""
SELECT user_id FROM recording_spark.ownership_over_group WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE recording_spark.ownership_over_group.user_id = ? AND recording_spark.ownership_over_group.group_id >=
(SELECT MAX(group_id) FROM recording_spark.group WHERE recording_spark.group.item = 5 AND group_id IN (SELECT group_id FROM recording_spark.ownership_over_group WHERE recording_spark.ownership_over_group.user_id = ?)))
"""

# SELECT item_id FROM recording_spark.item WHERE user_id_1 OR user_id_2
#sql.execute(
"""SELECT recording_spark.item.item_id, recording_spark.item.item_name, recording_spark.item.status, recording_spark.item.user_id_1, SAS.user_name, recording_spark.item.user_id_2, SUS.user_name, recording_spark.item.png_id_name, recording_spark.item.comments, recording_spark.item.inventory_id
    FROM recording_spark.item
    JOIN recording_spark.user SAS
    ON recording_spark.item.user_id_1 = SAS.user_id

    JOIN recording_spark.user SUS
    ON recording_spark.item.user_id_2 = SUS.user_id

    WHERE recording_spark.item.user_id_1 = ?
    OR recording_spark.item.user_id_2 = ?
    OR recording_spark.item.user_id_2 IN

(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)

)

"""
#,(user_id,user_id,user_id,))
#A = sql.fetchone()
#while A != None:
#    print(A)
#    A = sql.fetchone()





# CONSTRAINT recording_spark.user PRIMARY KEY (user_id)
# product_no integer PRIMARY KEY,
"""
( website_id INT(11) NOT NULL AUTO_INCREMENT,
  website_name VARCHAR(25) NOT NULL,
  server_name VARCHAR(20),
  creation_date DATE,
  CONSTRAINT websites_pk PRIMARY KEY (website_id)

"""
# END

# BEGIN redis
import redis
from datetime import timedelta
r = redis.StrictRedis(
    host=IP,
    port=6379,
    password='',
    charset="utf-8",
    decode_responses=True,
    db = 1
)
# END
# BEGIN L
# Пользователь может быть в нескольких группах.
# ID levol Это уровень групы
# Если ID levol администратора меньше ID levol пользователя, то всё ок.
# Если ID levol администратора равен ID levol пользователя, то прова уразаны в двое (Не досупны функции "Редактировать/Удолять/Создовать").
# Админестрарор может создать или выдать пользователю только те групы, в которых сам состоит.
# Только люди с ID levol 0 имеют право изменять emeil или пароль другим членам.

# Люжи с ID levol 0 имеют обсолютные прова.


# Доступ на чтение <= (user_id[ID levol] <= ID levol пользователей предмета)

# ID levol
"""
r.rpush(f"recording_spark:user_group:{4344}", 4)
r.rpush(f"recording_spark:user_group:{4344}", 2)
r.rpush(f"recording_spark:user_group:{34545}", 4)
r.rpush(f"recording_spark:user_group:{23324}", 4)
"""



[1,2,3,4,5]
#- - + - -
#- - + + +

#    +
#    + + + + + + +
user_id = 1
#sql.execute(
"""SELECT recording_spark.item.item_id, recording_spark.item.item_name, recording_spark.item.status, recording_spark.item.user_id_1, SAS.user_name, recording_spark.item.user_id_2, SUS.user_name, recording_spark.item.png_id_name, recording_spark.item.comments, recording_spark.item.inventory_id
    FROM recording_spark.item
    JOIN recording_spark.user SAS
    ON recording_spark.item.user_id_1 = SAS.user_id

    JOIN recording_spark.user SUS
    ON recording_spark.item.user_id_2 = SUS.user_id

    WHERE recording_spark.item.user_id_1 = ?
    OR recording_spark.item.user_id_2 = ?
    OR recording_spark.item.user_id_2
    IN (SELECT recording_spark.user_group.user_id FROM recording_spark.group WHERE group_id
    IN (SELECT group_id FROM recording_spark.group WHERE group_id IN (SELECT group_id FROM recording_spark.group WHERE recording_spark.user_group.user_id = ?) <= group_id
    IN (SELECT MAX(group_id) FROM recording_spark.group WHERE recording_spark.group.item = 5 AND group_id
    IN (SELECT group_id FROM recording_spark.user_group WHERE recording_spark.user_group.user_id = ?))))
    """
#, (user_id, user_id, user_id, user_id))

#A = sql.fetchone()
#while A != None:
#    print(A)
#    A = sql.fetchone()

# Пользователи
# # Сам (Читать, Редактировать)
# # Своя група (Читать, Редактировать/Удолять/Создовать)
# # Остольное (Читать, Редактировать/Удолять/Создовать)

# Предметы
# # Своё (Читать, Редактировать/Удолять/Создовать)
# # Своя група (Читать, Редактировать/Удолять/Создовать)
# # Остольное (Читать, Редактировать/Удолять/Создовать)
"""
0000000000000001 - Предметы - Своё - Читать
0000000001000000 - Пользователи - Своё - Читать
0000000100000000 - Пользователи - Своя група - Читать
1000000000000000 - ID levol - 8

1000000101000001 - 33089


000001
000010
000100
001000
010000
100000
"""

"""
IDL - ID levol

 11111111
    IDL    user   item
|10000000|100000|100000|
     1000 000101 000001 - 33089
   1000
    8




111111111111
000101000001
000101000001

1000000101000001


33089-4095

8191 -
"""

# END


"""
    IDL    user   item
|10000000|100000|100000|
     1000 000101 000001 - 33089
  1100100 000001 000001 - 409665
   1010   001111 001111 - 41935
   1000   011111 111111 - 34815

          000101 000101 - 325
          000001 000001 - 65
          001111 001111 - 975
          011111 111111 - 2047



"""
# 111111111111
# 100



# 1000001

#10000

# # Своё (Читать, Редактировать/Удолять/Создовать)
# # Своя група (Читать, Редактировать/Удолять/Создовать)
# # Остольное (Читать, Редактировать/Удолять/Создовать)

# 000001 - 1
# 000100 - 4
# 010000 - 16

# SELECT 65 & 16, 65 & 4, 65 & 1
#user_id = 1
#sql.execute(

"""

SELECT

@a:=(SELECT rights FROM recording_spark.group WHERE group_id = (SELECT group_id FROM recording_spark.user WHERE user_id = ?)),
IF (1=1,@a,0)

"""
#,(user_id, ))


#A = sql.fetchone()
#while A != None:
#    print(A)
#    A = sql.fetchone()
print("@@@@@@@@@@@@@@@@@@@")
#sql.execute(

"""

SELECT item_id, item_name, @a & 4, @q FROM recording_spark.item WHERE
user_id_1 = ?
OR user_id_2 = ?
OR @a & 4 = 4
AND user_id_2 IN


(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?) AND

@a:=(SELECT rights FROM recording_spark.group WHERE group_id
IN (SELECT group_id FROM recording_spark.user WHERE user_id = ?))

)


"""
#,(user_id,user_id,user_id,user_id))


#A = sql.fetchone()
#while A != None:
#    print(A)
#    A = sql.fetchone()


"""
SELECT rights & 1, rights >> 2 & 1, rights >> 4 & 1 FROM recording_spark.group WHERE group_id =
(SELECT group_id FROM recording_spark.user WHERE user_id = ?)
"""
# IF (? = 0, rights & 1, IF (? = 1, rights >> 1 & 1, IF (? = 2, rights >> 6 & 1,rights >> 7 & 1))),
def permissions(u_id,L): # 0 - item_r,1 - item_w ,2 - user_r , 3 - user_w
    sql.execute("""
SELECT
IF (? = 0, rights & 1,      IF (? = 1, rights >> 1 & 1, IF (? = 2, rights >> 6 & 1,rights >> 7 & 1))),
IF (? = 0, rights >> 2 & 1, IF (? = 1, rights >> 3 & 1, IF (? = 2, rights >> 8 & 1,rights >> 9 & 1))),
IF (? = 0, rights >> 4 & 1, IF (? = 1, rights >> 5 & 1, IF (? = 2, rights >> 10 & 1,rights >> 11 & 1)))

FROM recording_spark.group WHERE group_id =
(SELECT group_id FROM recording_spark.user WHERE user_id = ?)
    """, (L ,L ,L ,L ,L ,L ,L ,L ,L ,u_id))
    A = sql.fetchone()
    if A == None:
        return None
    else:
        #print(A)
        return(A)
def permissions_item_r(u_id):
    return(permissions(u_id,0))
def permissions_item_w(u_id):
    return(permissions(u_id,1))
def permissions_user_r(u_id):
    return(permissions(u_id,2))
def permissions_user_w(u_id):
    return(permissions(u_id,3))

#print(permissions_item_r(1))
#print(permissions_item_w(1))
#print(permissions_user_r(1))
#print(permissions_user_w(1))

admin = 0
meneger = 34815
sender = 41935
user = 409665
# BEGIN Redis
#
# Используем 2 токена, тороткоживучий 30 мин.
# И долгоживучий 30 дней (12ч. если пользовотель попросил его не запоминать.)
# Если пользователь хочет прдить свой токен то он получит не только ноый короткий токен,
# но и новый доинный, предыдуший будет немедленно удолён.
#
# BEGIN token

def update_short_token(user_id, live_token):
    TTL = r.pttl(f"recording_spark:{user_id}:{live_token}:PC-INFO") / 1000
    #print(int(L))
    if TTL > 31*60:
        rm_short_token(user_id, live_token)
        list_A = r.lrange(f"recording_spark:{user_id}:{live_token}:PC-INFO", 0, -1)
        for key in r.scan_iter(f"recording_spark:{user_id}:{live_token}:*"):
            r.delete(key)
        short_token, live_token = add_live_token(user_id, list_A[0], list_A[1], list_A[2],int(TTL))

        #short_token = add_short_token(user_id, live_token)
        return short_token, live_token
    return None, None

#rm_short_token()

def rm_live_token(user_id, live_token):
    short_token = r.get(f'recording_spark:{user_id}:{live_token}:short_token') ### !!! ИНЕКЦИЯ !!!
    r.delete(f"recording_spark:short_token:{short_token}")
    A = False
    for key in r.scan_iter(f"recording_spark:{user_id}:{live_token}:*"):
        A = True
        r.delete(key)
    return A

def rm_short_token(user_id, live_token):
    short_token = r.get(f'recording_spark:{user_id}:{live_token}:short_token') ### !!! ИНЕКЦИЯ !!!
    r.delete(f"recording_spark:short_token:{short_token}")
    r.delete(f'recording_spark:{user_id}:{live_token}:short_token')

def add_short_token(user_id, live_token):
    short_token = secrets.token_urlsafe(32)
    r.set(f"recording_spark:short_token:{short_token}", user_id, 30*60)
    r.set(f"recording_spark:{user_id}:{live_token}:short_token", short_token, 30*60)
    return short_token


def add_live_token(user_id, ps_info_name, ps_info_ip, ps_info_date,TTL):
    live_token = secrets.token_urlsafe(128)
    #if remember == 1:
    #    TTL = 30*24*60*60
    #elif remember == 0:
    #    TTL = 12*60*60
    #print(ps_info_date)

    r.rpush(f"recording_spark:{str(user_id)}:{live_token}:PC-INFO", ps_info_name, ps_info_ip, str(ps_info_date))
    r.expire(f'recording_spark:{user_id}:{live_token}:PC-INFO', timedelta(seconds=TTL))
    #r.ttl(f"recording_spark:{user_id}:{live_token}:PC-INFO", int(TTL))
    #r.rpushx(f"recording_spark:{user_id}:{live_token}:PC-INFO", int(TTL))
    short_token = add_short_token(user_id, live_token)
    return short_token, live_token




    #r.set(f"recording_spark:{user_id}:{live_token}:PC-INFO", ps_info, 30*24*60*60)
    return live_token

def check_user_live_token(user_id,live_token):
    user_id = r.get(f'recording_spark:{user_id}:{live_token}:PC-INFO') ### !!! ИНЕКЦИЯ !!!
    if user_id == None:
        print("None")
        return None
    else:
        short_token = update_short_token(user_id, live_token)
        #short_token = add_short_token(user_id)
        #r.expire(f'recording_spark:live_token:{live_token}', timedelta(seconds=30*24*60*60))
        return short_token


#add_live_token(1, "40-PC", "192.168.1.40", "25-04-2022",1)

"""
def add_short_token(user_id):
    short_token = secrets.token_urlsafe(32)
    r.set(f"recording_spark:short_token:{short_token}", user_id, 12*60*60)
    return short_token

def add_live_token(user_id):
    live_token = secrets.token_urlsafe(128)
    r.set(f"recording_spark:live_token:{live_token}", user_id, 30*24*60*60)
    return live_token

"""
def check_user_short_token(short_token):
    user_id = r.get(f'recording_spark:short_token:{short_token}') ### !!! ИНЕКЦИЯ !!!
    if user_id == None:
        return None
    else:
        return user_id


def ls_sessions(user_id): # !!! МОГУТ БЫТЬ ПРОБЛЕМЫ !!!
    A = 0
    Q = []
    for key in r.scan_iter(f"recording_spark:{user_id}:*:PC-INFO"):
        print(key)
        short_token = r.lrange(key, 0, -1)
        short_token.append(A)
        Q.append(short_token)
        A = A + 1
    return Q

#print(ls_sessions(1))


def rm_live_token_position(user_id, position): # !!! МОГУТ БЫТЬ ПРОБЛЕМЫ !!!
    A = 0
    for key in r.scan_iter(f"recording_spark:{user_id}:*"):
        if position == A:
            short_token = r.get(f'recording_spark:{user_id}:{key}:short_token') ### !!! ИНЕКЦИЯ !!!
            r.delete(f"recording_spark:short_token:{short_token}")
            for key in r.scan_iter(f"recording_spark:{user_id}:{key}:*"):
                r.delete(key)
        A = A + 1


def full_sessions_kill(user_id):
    for key in r.scan_iter(f"recording_spark:{user_id}:*:short_token"):
        short_token = r.get(key)
        r.delete(f"recording_spark:short_token:{short_token}")
        r.delete(key)
    for key in r.scan_iter(f"recording_spark:{user_id}:*"):
        r.delete(key)

#full_sessions_kill(1)
#print(update_short_token(1, "tAVtQvl-_NmPOXbRoqfPWVtlx5gblZjcjVZmUy6qGa60Dzc7bWqHzj0ybsoyvv1rj5EG-jLc2eEuTR4riEvQy_ggVMLZVx9VDlI_z1fqpWvW6wRQDqxW4upiSLmqseCPHuqJMbNpXqa8l-fIH8Lrb2r73wcCklhFLdqh7lRe9og"))

#add_live_token(1, "80-PC", "192.168.1.64", "26-04-2022",12*60*60)




#r.delete(f"recording_spark:1:*")

"SGSlPpX0m-bWDmgDkaLrtAf9JAjno46Wg01KmEAf0Qs"
"""
def check_user_live_token(live_token):
    user_id = r.get(f'recording_spark:live_token:{live_token}') ### !!! ИНЕКЦИЯ !!!
    if user_id == None:
        print("None")
        return None
    else:
        short_token = add_short_token(user_id)
        r.expire(f'recording_spark:live_token:{live_token}', timedelta(seconds=30*24*60*60))
        return short_token
"""

# END

def add_user_registration(email, password):
    G = int(strftime("%Y")) # Год
    M = int(strftime("%m")) # Месяц
    D = int(strftime("%d")) # День
    ch = int(strftime("%H"))
    m = int(strftime("%M"))
    s = int(strftime("%S"))
    #id = str(D) + str(ch) + str(m) + str(s) + str(random.randint(0, 100000))
    id = f"{D}{ch}{m}{s}{random.randint(0, 100000)}"


    date = f"{G}-{M}-{D}"
    r.set(f"recording_spark:registration:{id}:email", email, 7*24*60*60)
    r.set(f"recording_spark:registration:{id}:password", password, 7*24*60*60)
    r.set(f"recording_spark:registration:{id}:date", date, 7*24*60*60)
    return id




# END
# BEGIN mariadb_SAS

def user_name(user_id):
    sql.execute("SELECT user_name FROM recording_spark.user WHERE user_id = ?", (user_id,))
    A = sql.fetchone()
    if A == None:
        return None
    else:
        return(A[0])


def avatar_png(user_id):
    sql.execute("SELECT avatar FROM recording_spark.user WHERE user_id = ?", (user_id,))
    A = sql.fetchone()
    if A == None:
        return None
    else:
        return(A[0])


def check_user(email, password):
    sql.execute("SELECT user_id, user_name, active FROM recording_spark.user WHERE email = ? AND password = ?", (email, password))
    A = sql.fetchone()
    if A == None:
        return None, None, None
    else:
        print(A[0])
        return(A[0], A[1], A[2])


#def ls_item2(user_id):
#    Q = [[],[],[],[],[]]
#    sql.execute("SELECT item_id, item_name, status, user_id_1, user_id_2 FROM recording_spark.item WHERE user_id_1 = ? OR user_id_2 = ?", (user_id, user_id))
#    A = sql.fetchone()
#    if A == None:
#        return None
#    R = 0
#    while A != None:
#        for a in A:
#            Q[R].append(a)
#        A = sql.fetchone()
#        R = R + 1
    #print(Q[2][1])
#    return Q
# OR LLL.user_id IN (SELECT user_id FROM recording_spark.group WHERE group_id = ?)
"""
    JOIN recording_spark.group LLL
    ON recording_spark.item.user_id_2 = LLL.user_id
"""

def ls_user(user_id):
    A = permissions_user_r(user_id)
    print(A)
    sql.execute("""SELECT recording_spark.user.user_id, recording_spark.user.user_name, recording_spark.user.email, recording_spark.user.avatar, recording_spark.user.active, SAS.group_id, SAS.name, SAS.rights
    FROM recording_spark.user
    JOIN recording_spark.group SAS
    ON recording_spark.user.group_id = SAS.group_id

    WHERE
    IF (? = 1, user_id >= 0,
    IF (? = 1, user_id = ?, NULL) OR
    IF (? = 1,
user_id IN
(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)),
NULL)
    )

    """, (A[2], A[0], user_id, A[1], user_id))
    A = sql.fetchall()
    if A == None:
        return None
    else:
        print(A)
        print(A[0])
        #return(A[0])
        return A


def ls_user__3(user_id):
    A = permissions_user_r(user_id)
    print(A)
    sql.execute("""SELECT user_id, user_name, email, avatar, active, group_id
    FROM recording_spark.user
    WHERE
    IF (? = 1, user_id >= 0,
    IF (? = 1, user_id = ?, NULL) OR
    IF (? = 1,
user_id IN
(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)),
NULL)
    )

    """, (A[2], A[0], user_id, A[1], user_id))
    Q = []
    A = sql.fetchone()
    while A != None:
        print(A)
        Q.append(list(A))
        A = sql.fetchone()
    return Q


#print(ls_user(4))


def ls_item(user_id):
    A = permissions_item_r(user_id)
    #if A[2] == 1:
    sql.execute("""SELECT recording_spark.item.item_id, recording_spark.item.item_name, recording_spark.item.status, recording_spark.item.user_id_1, SAS.user_name, recording_spark.item.user_id_2, SUS.user_name, recording_spark.item.icon, recording_spark.item.comments, recording_spark.item.inventory_id

    FROM recording_spark.item

    JOIN recording_spark.user SAS
    ON recording_spark.item.user_id_1 = SAS.user_id

    JOIN recording_spark.user SUS
    ON recording_spark.item.user_id_2 = SUS.user_id

    WHERE
    IF (? = 1, recording_spark.item.item_id >= 0,


    IF (? = 1,
    recording_spark.item.user_id_1 = ?
    OR recording_spark.item.user_id_2 = ?,
    NULL) OR
    IF (? = 1, recording_spark.item.user_id_2 IN
(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)),
NULL)
)

    """, (A[2], A[0], user_id, user_id, A[1], user_id))
    Q = []
    A = sql.fetchone()
    while A != None:
        #print(A)
        Q.append(list(A))
        A = sql.fetchone()
    return Q



#print(ls_item(3))



#def ls_item(user_id):
    #Q = [[],[],[],[],[],[],[],[],[],[]]
#    sql.execute(
    """SELECT recording_spark.item.item_id, recording_spark.item.item_name, recording_spark.item.status, recording_spark.item.user_id_1, SAS.user_name, recording_spark.item.user_id_2, SUS.user_name, recording_spark.item.png_id_name, recording_spark.item.comments, recording_spark.item.inventory_id
    FROM recording_spark.item
    JOIN recording_spark.user SAS
    ON recording_spark.item.user_id_1 = SAS.user_id

    JOIN recording_spark.user SUS
    ON recording_spark.item.user_id_2 = SUS.user_id

    WHERE recording_spark.item.user_id_1 = ?
    OR recording_spark.item.user_id_2 = ?
    OR recording_spark.item.user_id_2 IN

(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)

)
    """
#    , (user_id, user_id, user_id))
#    A = sql.fetchone()
#    while A != None:
#        print(A)
#        Q.append(A)
    #for a in A:
    #    print(a)
    """
    if A == None:
        return None
    R = 0
    while A != None:
        for a in A:
            print(a)
            if a == None:
                Q[R].append("None")
            else:
                Q[R].append(a)
            R = R + 1
        print("--------------")
        A = sql.fetchone()
        R = 0
    return Q
    """


#bd.commit()
#sql.execute(
"""
    SELECT * FROM recording_spark.user
    WHERE
    ? = user_id
"""
#,(id,))

#A = sql.fetchone()
#print(A)


# 3 зп!
def user_add(user_id:int, user_name:str, email:str, password:str, avatar:bool, active:bool, group_id:int):
    def add(user_name, email, password, avatar, active, group_id):
        print(user_name, email, password, avatar, active, group_id)
        sql.execute("""
            INSERT INTO recording_spark.user
            VALUES
            (NULL, ?, ?, ?, ?, ?, ?)
        """,(user_name, email, password, avatar, active, group_id))
        id = sql.lastrowid
        print(id)
        bd.commit()
        return id
    A = permissions_user_w(user_id)
    print(A)
    if A[2] == 1:
        id = add(user_name, email, password, avatar, active, group_id)
        return id
    elif A[1] == 1:
        sql.execute("""
        SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?
        """,(user_id,))
        Q = []
        A = sql.fetchone()
        while A != None:
            print(A)
            Q.append(A[0])
            A = sql.fetchone()
        print(Q)
        for a in Q:

            if a == group_id:
                id = add(user_name, email, password, avatar, active, group_id)
                bd.commit()
                return id
    else:
        return None


#id = user_add(1, "Фёдор", None, "mnvbijdseahicihsf72e3wh89hfuh34h89f", 0, 1, 3)
#print(id)

# Удолить могут только отпровители или те кто имеет власть над отпровителями.

# 3-4 зп!
def item_edit_2(user_id, item_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id):
    A = permissions_item_w(user_id)
    print(A)
    sql.execute("""SELECT IF
                (? IN
                (SELECT user_id FROM recording_spark.user WHERE group_id IN
                (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
                , 1,0), IF
                (? IN
                (SELECT user_id FROM recording_spark.user WHERE group_id IN
                (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
                , 1,0)

                """,(user_id_1,user_id, user_id_2,user_id))
    Al = sql.fetchone()
    print(Al)
    if Al[0] == 1 or user_id_1 == user_id or user_id_1 == -1 and Al[1] == 1 or user_id_2 == user_id or user_id_2 == -1:
        sql.execute("""SELECT IF  (
            (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?) IN
            (SELECT user_id FROM recording_spark.user WHERE group_id IN
            (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
            , 1,0

            )

        """,(item_id,user_id,))
        Am = sql.fetchone()
        print(Am)
        if Am[0] == 1:
            sql.execute("""UPDATE recording_spark.item
    SET
    item_name= IF (? = 'None', item_name, ?),
    status = IF (? = 'None', status, ?),
    user_id_1 = IF (? = -1, user_id_1, ?),
    user_id_2 = IF (? = -1, user_id_2, ?),
    icon = IF (? = 'None', icon, ?),
    comments = IF (? = 'None', comments, ?),
    inventory_id = IF (? = 'None', inventory_id, ?)

    WHERE item_id = ?


            """,(name,name,status,status,user_id_1,user_id_1,user_id_2,user_id_2,icon,icon,comments,comments,inventory_id,inventory_id,item_id))






item_id = 3
user_id = 23
user_id_1 = 1
user_id_2 = -1
#A = permissions_user_w(user_id)
#print(f'uw{A}')
#Al = permissions_user_r(user_id)
#print(f'ur{Al}')
#A = permissions_item_r(user_id)
#print(f'ir{A}')
#A = permissions_item_w(user_id)
#print(f'iw{A}')
# 2 зп!
def item_edit(user_id, item_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id):
    print(user_id, item_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id)
    Al = permissions_user_r(user_id)
    print(f'ur{Al}')
    A = permissions_item_w(user_id)
    print(f'iw{A}')
    sql.execute("""UPDATE recording_spark.item
    SET
    item_name= IF (? IS NULL, item_name, ?),
    status = IF (? IS NULL, status, ?),
    user_id_1 = IF (? IS NULL, user_id_1, ?),
    user_id_2 = IF (? IS NULL, user_id_2, ?),
    icon = IF (? IS NULL, icon, IF (? = '-1', NULL, ?)),
    comments = IF (? IS NULL, comments, ?),
    inventory_id = IF (? IS NULL, inventory_id, IF (? = -1, NULL, ?))

    WHERE item_id =

    IF (1 =

    IF (? = 1, 1,
    IF (? = 1 AND (? = (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?)), 1,
    IF (? = 1 AND
    (
    (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?) IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))), 1, 0

    )
    )
    ) AND

    IF (? = 1, 1,

    IF (? IS NULL, 1,
    IF (? = 1 AND ? = ?, 1,
    IF (? = 1 AND
    (? IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))),1,0)

    )

    )

    AND
    IF (? IS NULL, 1,
    IF (? = 1 AND ? = ?, 1,
    IF (? = 1 AND
    (? IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))),1,0)

    )
    )

    )


    , ?, NULL)


    """,(name,name,status,status,user_id_1,user_id_1,user_id_2,user_id_2,icon,icon,icon,comments,comments,inventory_id,inventory_id,inventory_id,
        A[2],  A[0],user_id,item_id,  A[1],item_id,user_id,
        Al[2],
        user_id_1,  Al[0],user_id_1,user_id,  Al[1],user_id_1,user_id,
        user_id_2,  Al[0],user_id_2,user_id,  Al[1],user_id_2,user_id,
        item_id
        ))
    #Al = sql.fetchone()
    id = sql.rowcount
    print(id)
    bd.commit()
    return int(id)


#item_edit(1, 32, None, None, None, None, -1, None, None)

#item_edit(user_id, item_id, user_id_1, user_id_2, "None", "None", -1, "None", 465)


def item_edit_3(user_id, item_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id):
    A = permissions_item_w(user_id)
    print(A)
    sql.execute("""UPDATE recording_spark.item
    SET
    item_name= IF (? IS NULL, item_name, ?),
    status = IF (? IS NULL, status, ?),
    user_id_1 = IF (? IS NULL, user_id_1, ?),
    user_id_2 = IF (? IS NULL, user_id_2, ?),
    icon = IF (? IS NULL, icon, ?),
    comments = IF (? IS NULL, comments, ?),
    inventory_id = IF (? IS NULL, inventory_id, ?)

    WHERE

    IF (? =
    (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?)
    AND ? = 1, item_id = ?,
    IF (? = 1, item_id = ?,
    IF (? = 1,

    IF
    ((SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?) IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
    ,


    ,NULL))))


    , NULL)))





            """,(name,name,status,status,user_id_1,user_id_1,user_id_2,user_id_2,icon,icon,comments,comments,inventory_id,inventory_id,item_id))
    id = sql.rowcount
    print(id)

#item_edit(1, 3, -1, -1, "SAS", "None", 0, "None", -1)

"""
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)

SELECT user_id_1 FROM recording_spark.item WHERE ? = item_id

SELECT
        IF (? = ?, (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?),

        IF (? = 1, (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?),
        IF (? = 1 AND (

        ? IN

        (SELECT user_id FROM uid WHERE group_id IN
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))),
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)
        , NULL)))


"""


def permission(u_id,user_id):
    A = permissions_user_r(u_id)
    print(A)
    sql.execute("""SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id =
        IF (? = ? AND ? = 1, ?,
        IF (? = 1, ?,
        IF (? = 1 AND

    ? IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)), ?, NULL)))

        """,(u_id, user_id,A[0],user_id,A[2],user_id, A[1], user_id, u_id, user_id))
    id = sql.fetchall()
    #id = sql.rowcount
    print(id)
    sql.execute("""SELECT group_id FROM recording_spark.user WHERE user_id =
        IF (? = ? AND ? = 1, ?,
        IF (? = 1, ?,
        IF (? = 1 AND

    ? IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)), ?, NULL)))

        """,(u_id, user_id,A[0],user_id,A[2],user_id, A[1], user_id, u_id, user_id))
    permission_int = sql.fetchall()

    return id, permission_int

# permission(3,1)

# 2 зп!
def item_rm(user_id,item_id):
    A = permissions_item_w(user_id)
    sql.execute("""DELETE FROM recording_spark.item WHERE item_id =

        IF (? = (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?)
        AND
        (? = 1), ?,

        IF (? = 1, ?,
        IF (? = 1 AND (

        ? IN

        (SELECT item_id FROM recording_spark.item WHERE user_id_1

        IN
        (SELECT user_id FROM recording_spark.user WHERE group_id IN
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)))), ?, NULL)))




        """,(user_id,item_id,A[0],item_id, A[2],item_id, A[1],item_id,user_id, item_id))
    #id = sql.fetchone()
    id = sql.rowcount
    print(id)
    return id

#item_rm(5,2)
#sql.execute(
    """
    DELETE recording_spark.user, recording_spark.ownership_over_group
        FROM recording_spark.ownership_over_group
        INNER JOIN recording_spark.user

        WHERE

        recording_spark.ownership_over_group.user_id = 23 AND
        recording_spark.user.user_id = 23




    """
    #)
#id = sql.rowcount
#print(id)
def user_rm(user_id,user_id_rm):
    A = permissions_user_w(user_id)
    sql.execute("""DELETE
        recording_spark.user, recording_spark.ownership_over_group FROM
        recording_spark.user
        INNER JOIN recording_spark.user uid
        INNER JOIN recording_spark.ownership_over_group

        WHERE
        IF (? = ?, user_id = NULL,

        IF (? = 1, user_id = ?,
        IF (? = 1 AND (

        ? IN

        (SELECT user_id FROM uid WHERE group_id IN
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))), user_id = ?, user_id = NULL)))

        """,(user_id, user_id_rm,A[0],user_id_rm, A[2],user_id_rm, user_id,user_id_rm))
    #id = sql.fetchone()
    id = sql.rowcount
    print(id)
    return id
#item_rm(5,2)
#user_rm(1,23)

############################################### + !!! ПЕРЕДАЛАТЬ !!!
def item_rm_2(user_id,item_id):
    A = permissions_item_w(user_id)
    print(A)
    if A[2] != 1:
        sql.execute("DELETE FROM recording_spark.item WHERE ? = item_id",(item_id,))
        bd.commit()
        return 1
    if A[0] != 1:
        print("AAA")
        return 0
    sql.execute("SELECT user_id_1 FROM recording_spark.item WHERE ? = item_id",(item_id,))
    Al = sql.fetchone()
    if len(Al) != 0:
        if user_id == Al[0]:
            sql.execute("DELETE FROM recording_spark.item WHERE ? = item_id",(item_id,))
            bd.commit()
            return 1
        elif A[1] != 1:
            sql.execute("""SELECT IF
                (? IN
                (SELECT user_id FROM recording_spark.user WHERE group_id IN
                (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
                , 1,0)
                """,(Al[0],user_id,))
            Al = sql.fetchone()
            if Al == 1:
                sql.execute("DELETE FROM recording_spark.item WHERE ? = item_id",(item_id,))
                bd.commit()
                return 1
            else:
                print("SSS")
                return 0


    else:
        print("Нет такого!")
        return 0

# 4 зп!
def add_item(user_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id):
    print(user_id, user_id_1, user_id_2, name, status, icon, comments, inventory_id)
    Al = permissions_user_r(user_id)
    print(f'ur{Al}')
    A = permissions_item_w(user_id)
    print(f'iw{A}')
    sql.execute("""SELECT

    (SELECT
    IF (1 =

    IF (
    IF ((? = ?) AND (? = ?), 1,0) = 0,
    IF (? = 1,1,
    IF (? = 1,



    IF (1 =

    IF (? = -1, 1, IF (
    ?
    IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)) OR ? = ?,
    1, 0
    )
    )

    AND

    IF (? = -1, 1, IF (
    ?
    IN
    (SELECT user_id FROM recording_spark.user WHERE group_id IN
    (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)) OR ? = ?,
    1, 0
    )

    ),1,0),0)),1)



    ,

    IF (? = 1, 1,
    IF (? = 1, 1,
    IF (? = 1,

    1,0))),0))


    """,(user_id_1, user_id, user_id_2, user_id,Al[2],Al[1],user_id_1, user_id_1, user_id,user_id_1,user_id, user_id_2, user_id_2, user_id,user_id_2,user_id, A[0],A[2], A[1]))
    id = sql.fetchone()
    if id[0] == 1:

        print("Ура!!!")
        sql.execute("""
                INSERT INTO recording_spark.item
                VALUES
                (NULL, ?, ?, ?, ?, ?, ?, ?)
        """,(name, status, user_id_1, user_id_2, icon, comments, inventory_id))
        id = sql.lastrowid
        print(id)
        bd.commit()
        return id
    #id = sql.rowcount
    print(id)
    #bd.commit()
    return id


#add_item(1, 5, 2, "SAS", "SUS", 0, "SGS", 3333)

# 3 зп!
# Работает, НЕ ТРОГОЙ!!! но мне пох)))
def add_item_3(user_id, user_id_2, name, status, icon, comments, inventory_id):
    A = permissions_item_w(user_id)
    print(A)
    if A[0] == 1 or A[1] == 1 or A[2] == 1:
        sql.execute("""
            SELECT IF
                (? IN
                (SELECT user_id FROM recording_spark.user WHERE group_id IN
                (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?))
                , 1,0)
        """,(user_id_2,user_id))
        Al = sql.fetchone()
        if Al[0] == 1:
            sql.execute("""
                INSERT INTO recording_spark.item
                VALUES
                (NULL, ?, ?, ?, ?, ?, ?, ?)
            """,(name, status, user_id, user_id_2, icon, comments, inventory_id))
            id = sql.lastrowid
            print(id)
            bd.commit()
            return id
        return 0

#id = add_item(1, 23, "Морковь", "В пути", 0, "2кг.", 784538673428743)
#print(id)

# 2 зп!
def user_edit(user_id,user_id_rec, user_name, email, password, avatar, active, group_id):
    A = permissions_user_w(user_id)
    print(user_id)
    print(A)
    print(user_id,user_id_rec, user_name, email, password, avatar, active, group_id)
    sql.execute("""UPDATE recording_spark.user
    SET
    user_name = IF (? IS NULL, user_name, ?),
    email = IF (? IS NULL, email, ?),
    password = IF (? IS NULL, password, ?),
    avatar = IF (? IS NULL, avatar, ?),
    active = IF (? IS NULL, active, ?),
    group_id = IF (? IS NULL, group_id, ?)

    WHERE
    IF (? = ? AND ? = 1, recording_spark.user.user_id = ?,
    IF (? = 1, recording_spark.user.user_id = ?,
    IF (? = 1,

? = user_id and user_id IN
(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)), NULL)))

    """, (user_name, user_name, email, email, password, password, avatar, avatar, active, active, group_id, group_id, user_id, user_id_rec, A[0], user_id, A[2], user_id_rec, A[1]  , user_id_rec, user_id))
    bd.commit()
    id = sql.rowcount
    print(id)
    if (id == 1 and active == 0) or (id == 1 and password != None):
        full_sessions_kill(user_id_rec)
    return id
    #A = sql.fetchone()
    #if A == None:
        #return None
    #else:
        #print(A)


#sql.execute("SELECT IF (? IS NULL, 1, 0)", (None,))
#print(sql.fetchone())

#user_edit(1,5, None, "GGG", None,None,None,None)

# 2 зп!
def user_info(user_id,user_id_rec):
    A = permissions_user_r(user_id)
    print(A)
    sql.execute("""SELECT recording_spark.user.user_name, recording_spark.user.email, recording_spark.user.avatar, recording_spark.user.active, SAS.group_id, SAS.rights
    FROM recording_spark.user
    JOIN recording_spark.group SAS
    ON recording_spark.user.group_id = SAS.group_id

    WHERE
    IF (? = ? AND ? = 1, recording_spark.user.user_id = ?,
    IF (? = 1, recording_spark.user.user_id = ?,
    IF (? = 1,

? = user_id and user_id IN
(SELECT user_id FROM recording_spark.user WHERE group_id IN
(SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)), NULL)))

    """, (int(user_id),int(user_id_rec), A[0],int(user_id), A[2],int(user_id_rec), A[1]  ,int(user_id_rec),int(user_id)))
    A = sql.fetchone()
    if A == None:
        return None
    else:
        print(A)
        print(A[0])
        #return(A[0])
        return A

def ls_group(user_id):
    A = permissions_user_r(user_id)
    if A[2] == 1:
        sql.execute("SELECT * FROM recording_spark.group")
        group_list = sql.fetchall()
    else:
        sql.execute("""SELECT * FROM recording_spark.group WHERE group_id
            IN
            (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)


            """, (user_id, user_id))
        group_list = sql.fetchall()
    return group_list



def item_info(user_id,item_id):
    A = permissions_item_r(user_id)
    sql.execute("""SELECT * FROM recording_spark.item
        WHERE item_id =

        IF (? = (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?)
        AND
        (? = 1), ?,

        IF (? = 1, ?,
        IF (? = 1 AND (

        ? IN

        (SELECT item_id FROM recording_spark.item WHERE user_id_1

        IN
        (SELECT user_id FROM recording_spark.user WHERE group_id IN
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)))), ?, NULL)))




        """,(user_id,item_id,A[0],item_id, A[2],item_id, A[1],item_id,user_id, item_id))
    group_list = sql.fetchone()
    return group_list

def item_w_test(user_id,item_id):
    A = permissions_item_w(user_id)
    sql.execute("""SELECT

        IF (? = (SELECT user_id_1 FROM recording_spark.item WHERE item_id = ?)
        AND
        (? = 1), 1,

        IF (? = 1, 1,
        IF (? = 1 AND (

        ? IN

        (SELECT item_id FROM recording_spark.item WHERE user_id_1

        IN
        (SELECT user_id FROM recording_spark.user WHERE group_id IN
        (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?)))), 1, 0)))




        """,(user_id,item_id,A[0], A[2], A[1],item_id,user_id))
    group_list = sql.fetchone()
    print(group_list[0])
    return int(group_list[0])

#print(item_info(1,20))
#print(item_w_test(1,100))


"""SELECT * FROM recording_spark.group WHERE group_id
            IN
            (SELECT group_id FROM recording_spark.ownership_over_group WHERE user_id = ?) OR group_id =
            (SELECT group_id FROM recording_spark.user WHERE user_id = ?)


            """

#print(ls_group(2))


#user_info(2,4)



#print(ls_item(5))

#print(permissions_item_w(3))


# END


#sql.execute("INSERT INTO recording_spark.group VALUES (4, 'user', 34545, 409665)")
#sql.execute("INSERT INTO recording_spark.group VALUES (4, 'user', 455435, 409665)")
#bd.commit()
#print(ls_item(1))






#ls_item(455435)






