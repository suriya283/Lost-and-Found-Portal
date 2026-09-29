import mysql.connector
from mysql.connector import cursor


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9043148891",
        database="lost_and_found"
    )

def check_admin(username):
    connection = get_db_connection()
    cursor =connection.cursor(dictionary=True)
    cursor.execute("select * from admin where username=%s",(username,))
    datas=cursor.fetchone()
    cursor.close()
    connection.close()
    return datas

def check_db(username):
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from users where username=%s",(username,))
    datas=cursor.fetchone()
    cursor.close()
    connection.close()
    return datas

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
def store_items(user_id,name,description,verification_description,location,date,number,status,img_location=None):
    connection=get_db_connection()
    cursor=connection.cursor()
    query="insert into items (user_id, item_name, item_description, verfication_description,location, date, image_location, mobile_number, status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=user_id,name,description,verification_description,location,date,img_location,number,status
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
def store_proof(id,proof,user_id):
    connection=get_db_connection()
    cursor=connection.cursor()
    query="insert into claims (item_id,claimant_id,proof_description,status) values (%s,%s,%s,%s)"
    values=id,user_id,proof,"pending"
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return True
def store_founder(user_id,item_id,number,location,description):
    connection=get_db_connection()
    cursor=connection.cursor()
    query="insert into founders (item_id, founder_id, mobile_number, location, proof_description, status) values (%s,%s,%s,%s,%s,%s)"
    values=item_id,user_id,number,location,description,"reported"
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    return True
def admin_display():
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()
    total_users=users['total_users']
    cursor.execute("SELECT * FROM items")
    items=cursor.fetchall()
    cursor.execute("select * from items i join founders f on i.id=f.item_id")
    found_datas=cursor.fetchall()
    cursor.execute("select * from items i join claims c on i.id=c.item_id")
    claims_datas=cursor.fetchall()
    cursor.close()
    connection.close()
    return total_users,items