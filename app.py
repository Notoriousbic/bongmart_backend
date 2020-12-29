import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

def generateToken():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(56))
    return result_str
print (generateToken())

@app.route('/api/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        conn = None
        cursor = None
        product = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            product = cursor.fetchall()
        except Exception as error:
            print("Something went wrong: ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(product != None):
                return Response(json.dumps(product, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
#############################################################################################################            
    elif request.method == 'POST':
        conn = None
        cursor = None
        item_name = request.json.get("name")
        item_description = request.json.get("description")
        item_price = request.json.get("price")
        item_image = request.json.get("image")
        item_salescode = request.json.get("SalesCode")
        item_qty = request.json.get("quantity")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product(name, price, description, picture_http, SalesCode, Qty) VALUES (?,?,?,?,?,?)", [item_name, item_price, item_description, item_image, item_salescode, item_qty])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("New Item Inserted!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
################################################################################################################                  
@app.route('/api/user', methods=['GET'])
def see_customers():
    if request.method == 'GET':
        conn = None
        cursor = None
        customers = None
        try:
                conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user")
                customers = cursor.fetchall()
                print(customers)
        except Exception as error:
                print("Something went wrong: ")
                print(error)
        finally:
                if(cursor != None):
                    cursor.close()
                if(conn != None):
                    conn.rollback()
                    conn.close()
                if(product != None):
                    return Response(json.dumps(customers, default=str), mimetype="application/json", status=200)
                else:
                    return Response("Something went wrong!", mimetype="text/html", status=500)
###############################################################################################################            
@app.route('/api/admin', methods=['POST'])
def login_endpoint():
    
    if request.method == 'POST':
        conn = None
        cursor = None
        username = request.json.get("username")
        password = request.json.get("password")
        loginToken = generateToken()
        rows = None
        admin= None
        user_id = None
        
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute ("SELECT id, username FROM admin WHERE username=? AND password=?", [username, password])
            admin = cursor.fetchall()
            print(admin)
            cursor.execute("INSERT INTO user_session(logintoken, user_id) VALUES (?,?)", [loginToken, admin[0][0]])
            conn.commit()
            rows = cursor.rowcount                                                                                          
        except Exception as error:
            print("Sorry you're F'ed.  Internal error and I'm too lazy to log further. HA.")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response (json.dumps(admin, default=str), mimetype="application/json", status="210")
            else:
                return Response("Look's like you F'd up! POST ERROR", mimetype="text/html", status=510)
################################################################################################################
@app.route('/api/purchase', methods=['POST','GET'])
def purchase_endpoint():
    if request.method == 'POST':
        conn = None
        cursor = None
        first_name = request.json.get("first_name")
        middle_name = request.json.get("middle_name")
        last_name = request.json.get("last_name")
        email = request.json.get("email")
        phone_number = request.json.get("phone_number")
        postal_code = request.json.get("postal_code")
        address = request.json.get("address")
        is_eighteen = request.json.get("is_eighteen")
        

        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO purchase(first_name, middle_name, last_name, email, postal_code, phone_number, address, is_eighteen) VALUES (?,?,?,?,?,?,?,?)", [first_name, middle_name, last_name, email, postal_code, phone_number, address, is_eighteen])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("New Purchase Inserted!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
            
    elif request.method == 'GET':
        conn = None
        cursor = None
        customers = None
        try:
                conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM purchase")
                customers = cursor.fetchall()
                print(customers)
        except Exception as error:
                print("Something went wrong: ")
                print(error)
        finally:
                if(cursor != None):
                    cursor.close()
                if(conn != None):
                    conn.rollback()
                    conn.close()
                if(product != None):
                    return Response(json.dumps(customers, default=str), mimetype="application/json", status=200)
                else:
                    return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'DELETE':
        conn = None
        user_id = None
        customers = None
        try:
                conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("DELETE  FROM purchase")
                customers = cursor.fetchall()
                print(customers)
        except Exception as error:
                print("Something went wrong: ")
                print(error)
        finally:
                if(cursor != None):
                    cursor.close()
                if(conn != None):
                    conn.rollback()
                    conn.close()
                if(product != None):
                    return Response(json.dumps(customers, default=str), mimetype="application/json", status=200)
                else:
                    return Response("Something went wrong!", mimetype="text/html", status=500)