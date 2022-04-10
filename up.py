import sqlite3 as db
from cryptography.fernet import Fernet

def get_password(db_path, in_row):

    conn = db.connect(db_path)
    c = conn.cursor()

    c.execute(f'''SELECT * FROM keys WHERE rowid={in_row} ''')
    key=c.fetchone()[0]

    c.execute(f'''SELECT * FROM hash WHERE rowid={in_row} ''')
    hashed_password=c.fetchone()[0]

    # Use the key
    cipher_suite = Fernet(key)
    # Decrypt password encrypted with key
    decrypted_pass = (cipher_suite.decrypt(hashed_password))

    # Check original password
    real_password = str(decrypted_pass,'utf-8')
    return real_password
