# coding=utf-8
# Python 3

"""
🏷️ ENCRYPT/DESCRYPT PASSWORDS
👔 Igor Perković

🚀 Created: 25.4.2018.
📅 Changed: 2022-04-10 12:26:59

⚙️ Prerequisites:
------------------------------
    sqlite3
    pip install cryptography

📃 Description:
--------------------------------------------------------------------------
This script uses cryptography library to create a secure keys and hashes
and stores them into separate tables in a database.

In the second part, Decryption, this scripts reads keys and hashes from
the database and decrypt previously encrypted text.

"""
import urllib
import sqlite3 as sq
from cryptography.fernet import Fernet


# oooooooooooo                                                           .    o8o
# `888'     `8                                                         .o8    `"'
#  888         ooo. .oo.    .ooooo.  oooo d8b oooo    ooo oo.ooooo.  .o888oo oooo   .ooooo.  ooo. .oo.
#  888oooo8    `888P"Y88b  d88' `"Y8 `888""8P  `88.  .8'   888' `88b   888   `888  d88' `88b `888P"Y88b
#  888    "     888   888  888        888       `88..8'    888   888   888    888  888   888  888   888
#  888       o  888   888  888   .o8  888        `888'     888   888   888 .  888  888   888  888   888
# o888ooooood8 o888o o888o `Y8bod8P' d888b        .8'      888bod8P'   "888" o888o `Y8bod8P' o888o o888o
#                                             .o..P'       888
#                                             `Y8P'       o888o
#--------------------------------------------------------------------------------------------------------
#
def new_password(conn, idn, raw_comment, raw_password):
    c = conn.cursor()

    new_key = Fernet.generate_key()
    cipher_suite = Fernet(new_key)
    raw_pass_binary = raw_password.encode('utf-8')
    encrypted_pass = cipher_suite.encrypt(raw_pass_binary)   #required to be bytes

    # Insert comment or description
    c.execute(f"INSERT INTO about(ID, comment, timestamp) VALUES ({idn}, '{raw_comment}', DateTime('now'));")

    # Insert keys
    insert_key = '''INSERT INTO keys(ID, keys) VALUES (?,?);'''
    k = sq.Binary(new_key)
    c.execute(insert_key,(idn,k))

    #insert
    insert_hash = '''INSERT INTO hash(ID, hash) VALUES (?,?);'''
    h = sq.Binary(encrypted_pass)
    c.execute(insert_hash,(idn,h))

    conn.commit()
    c.close()

def del_password(conn, idn):
    c = conn.cursor()

    c.execute(f'DELETE from about WHERE ID = {idn};')
    c.execute(f'DELETE from keys  WHERE ID = {idn};')
    c.execute(f'DELETE from hash  WHERE ID = {idn};')

    conn.commit()
    c.close()


# oooooooooo.                                                           .    o8o
# `888'   `Y8b                                                        .o8    `"'
#  888      888  .ooooo.   .ooooo.  oooo d8b oooo    ooo oo.ooooo.  .o888oo oooo   .ooooo.  ooo. .oo.
#  888      888 d88' `88b d88' `"Y8 `888""8P  `88.  .8'   888' `88b   888   `888  d88' `88b `888P"Y88b
#  888      888 888ooo888 888        888       `88..8'    888   888   888    888  888   888  888   888
#  888     d88' 888    .o 888   .o8  888        `888'     888   888   888 .  888  888   888  888   888
# o888bood8P'   `Y8bod8P' `Y8bod8P' d888b        .8'      888bod8P'   "888" o888o `Y8bod8P' o888o o888o
#                                            .o..P'       888
#                                            `Y8P'       o888o
#-------------------------------------------------------------------------------------------------------

def get_password(conn, in_row):
    c = conn.cursor()

    c.execute(f'''SELECT * FROM keys WHERE ID={in_row} ''')
    key=c.fetchone()[1]

    c.execute(f'''SELECT * FROM hash WHERE ID={in_row} ''')
    hashed_password=c.fetchone()[1]
    c.close()

    # Use the key
    cipher_suite = Fernet(key)
    # Decrypt password encrypted with key
    decrypted_pass = (cipher_suite.decrypt(hashed_password))

    # Check original password
    real_password = str(decrypted_pass,'utf-8')
    return urllib.parse.quote_plus(real_password)

    conn.commit()
    c.close()

