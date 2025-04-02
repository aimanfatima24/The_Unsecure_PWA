#import sqlite3 as sql
#import time
#import random




#def retrieveUsers(username, password):
 #   con = sql.connect("database_files/database.db")
  #  cur = con.cursor()
   # cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    #if cur.fetchone():
     #   return True
   # else:
    #    return False
     #   with open("visitor_log.txt", "r") as file:
      #      number = int(file.read().strip())
       #     number += 1
        #with open("visitor_log.txt", "w") as file:
         #   file.write(str(number))
        # #Simulate response time of heavy app for testing purposes
       # time.sleep(random.randint(80, 90) / 1000)
        #if cur.fetchone() == None:
         #   con.close()
          #  return False
       # else:
        #    con.close()
         #   return True
















def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Secure parameterized query
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone() is None:
        con.close()
        return False

    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    
    # Plain text log of visitor count as requested by Unsecure PWA management
    with open("visitor_log.txt", "r") as file:
        number = int(file.read().strip())
        number += 1
    with open("visitor_log.txt", "w") as file:
        file.write(str(number))

    # Simulate response time of heavy app for testing purposes
    time.sleep(random.randint(80, 90) / 1000)
    
    if cur.fetchone() is None:
        con.close()
        return False
    else:
        con.close()
        return True
    
    def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True
        

import sqlite3 as sql
import time
import random
import bcrypt  # Import bcrypt to hash passwords


def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(hashed_password, password):
    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def insertUser(username, password, DoB):
    hashed_password = hash_password(password)  # Hash the password
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth) VALUES (?, ?, ?)",
        (username, hashed_password, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Secure parameterized query
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user is None:
        con.close()
        return False

    # Check the stored hashed password
    stored_hashed_password = user[1]  # Assuming password is the second column
    if check_password(stored_hashed_password, password):
        # Log visitor count
        with open("visitor_log.txt", "r", encoding="utf-8") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w", encoding="utf-8") as file:
            file.write(str(number))

        # Simulate response time for testing purposes
        time.sleep(random.randint(80, 90) / 1000)

        con.close()
        return True
    else:
        con.close()
        return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
