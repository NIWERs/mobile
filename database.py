import mysql.connector as mysql



def registration(name, pw, email, status):
    host = 'db4free.net'
    user = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4' )

    cursor = connection.cursor()
    new_user = f"INSERT INTO `users`(password, email) VALUES ('{pw}', '{email}');"
    cursor.execute(new_user)
    connection.commit()

    new_user = f"INSERT INTO `des_users`(name, status, email) VALUES ('{name}', '{status}', '{email}');"
    cursor.execute(new_user)
    connection.commit()

    connection.close()


def check_user_pw(email):
    if (email == '') or (email == 'Email'):
        return ''

    host = 'db4free.net'
    user = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4')

    cursor = connection.cursor()
    user = f"SELECT `password` FROM `users` WHERE `email`='{email}'"
    cursor.execute(user)
    result = cursor.fetchone()

    connection.close()

    return result[0] if result else ''


def get_user_data(email):
    if (email == '') or (email == 'Email'):
        return ''

    host = 'db4free.net'
    user = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4')

    cursor = connection.cursor()
    user = f"SELECT `status`, `name` FROM `des_users` WHERE `email`='{email}'"
    cursor.execute(user)
    result = cursor.fetchone()

    connection.close()
    return result


def all_users():
    host = 'db4free.net'
    user = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4')
  
    cursor = connection.cursor()
    user = f"SELECT * FROM `des_users`"
    cursor.execute(user)
    result = cursor.fetchall()

    connection.close()
    return result


def get_ip(ip, name, update, connect):
    host = 'db4free.net'
    user_ip = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user_ip,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4')
    if connect:
        cursor = connection.cursor()
        user_ip = f"SELECT `ip` FROM `des_users` WHERE `name`='{name}'"
        cursor.execute(user_ip)
        result = cursor.fetchone()
        return result
    else:
        cursor = connection.cursor()
        ip_user = f"UPDATE `des_users` SET ip = '{ip}' WHERE name = '{name}';"
        cursor.execute(ip_user)
        connection.commit()

    connection.close()

def new_project(name, link, proj, connect=False):
    host = 'db4free.net'
    user_ip = 'niwer6'
    password = 'mrNIWER200512'

    print("Connection...")

    connection = mysql.connect(host=host,
                                 port=3306,
                                 user=user_ip,
                                 password=password,
                                 database='kivy_proj',
                                 charset='utf8mb4')
    if connect:
        cursor = connection.cursor()
        result = {}
        user = f"SELECT `project` FROM `des_users` WHERE `name`='{name}'"
        cursor.execute(user)
        result['project'] = cursor.fetchone()[0]

        user = f"SELECT `project_link` FROM `des_users` WHERE `name`='{name}'"
        cursor.execute(user)
        result['project_link'] = cursor.fetchone()[0]
        return result
    else:
        cursor = connection.cursor()
        ip_user = f"UPDATE `des_users` SET project = '{proj}' WHERE name = '{name}';"
        cursor.execute(ip_user)
        connection.commit()

        ip_user = f"UPDATE `des_users` SET project_link = '{link}' WHERE name = '{name}';"
        cursor.execute(ip_user)
        connection.commit()

    connection.close()
    
