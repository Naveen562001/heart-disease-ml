import mysql.connector

def db():

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",
    database="patient"
    )
  

    
    mycursor = mydb.cursor()
    return mydb
    
    #mycursor.execute("CREATE TABLE customers (age INT,sex VARCHAR(255),ChestPainType VARCHAR(255)),RestingBP INT,Cholesterol INT,")
    #mycursor.execute("SHOW TABLES")
   # print(mycursor)
