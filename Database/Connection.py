import pymysql 

def connection():
    conn = pymysql.connect(
        host="b8hsjnif8xkeguyz21hq-mysql.services.clever-cloud.com",
        port=3306,
        user="uazzuq7v4dfruk2g",
        password="w6aAlwovlXtfP5q05ZhD",
        db="b8hsjnif8xkeguyz21hq"
    )
    print("Database is Connected!")
    return conn