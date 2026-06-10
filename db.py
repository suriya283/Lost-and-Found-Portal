import mysql.connector
from mysql.connector import cursor


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9043148891",
        database="lost_and_found"
    )

def check_db(username):
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from users where username=%s",(username,))
    datas=cursor.fetchone()
    cursor.close()
    connection.close()
    if datas:
        return datas
    else:
        return
def store_user(username,name,password):
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("select * from users where username=%s",(username,))
    datas=cursor.fetchone()
    if datas:
        return True
    query="insert into users (name,username,password) values (%s,%s,%s)"
    values=name,username,password
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return False

def store_lost_item(item_name, description, location, date_lost, user_id, mobile_number):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "insert into lost_items (item_name, description, location, date_lost, user_id, mobile_number) values (%s,%s,%s,%s,%s,%s)"
        values = (item_name, description, location, date_lost, user_id, mobile_number)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        return False

def store_found_item(item_name, description, location, date_found, user_id, mobile_number):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "insert into found_items (item_name, description, location, date_found, user_id, mobile_number) values (%s,%s,%s,%s,%s,%s)"
        values = (item_name, description, location, date_found, user_id, mobile_number)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        return False

def get_lost_items():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from lost_items order by date_lost desc")
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items
    except:
        return []

def get_found_items():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from found_items order by date_found desc")
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items
    except:
        return []
