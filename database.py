import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "bnb_user",
    password = "1111",
    database = "bnb_db",
)

def save(query, data):
    cur = db.cursor(buffered=True)
    
    cur.execute(query, data)
    
    db.commit()
    cur.close()

    return True


def get(query, data):
    cur = db.cursor(buffered=True, dictionary=True)

    cur.execute(query, data)
    
    return cur.fetchall()
