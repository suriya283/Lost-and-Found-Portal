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
        cursor.close()
        connection.close()
        return True
    query="insert into users (name,username,password) values (%s,%s,%s)"
    values=name,username,password
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return False
def store_items(user_id,name,description,location,date,img_location,number,status):
    connection=get_db_connection()
    cursor=connection.cursor()
    query="insert into items (user_id, item_name, item_description, location, date, image_location, mobile_number, status) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    values=user_id,name,description,location,date,img_location,number,status
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return True
def get_all_item():
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    query="select * from items order by created_at desc"
    cursor.execute(query)
    datas=cursor.fetchall()
    cursor.close()
    connection.close()
    return datas
def search_items(keyword=None,status=None):
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    query="select * from items where 1=1"
    values=[]
    if keyword:
        query+=""" and (
            item_name like %s
            or item_description like %s
            or location like %s
           )"""
        values.extend([
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ])
    if status:
        query += "and status=%s"
        values.append(status)
    query+="order by created_at desc"
    cursor.execute(query,values)
    datas = cursor.fetchall()
    cursor.close()
    connection.close()
    return datas