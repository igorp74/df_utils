"""
## DATAFRAME UTILS
*#A collection of useful functions for work with database connectors*

👔 by Igor Perković

🛠 CREATED: 2020-10-13 08:39:29
📆 CHANGED: 2022-04-10 00:26:38

---
⚙ PREREQUISITES:
📘 Libraries: cx_Oracle, pyodbc, sqlalchemy

"""


def mssqlsrv(hostname, database, **kwargs):
    """
    #*MicroSoft SQL Server connection engine for Python.*

    ---
    ### Arguments:
    **Mandatory**
    - hostname:     Host IP or Name. Non-default port number goes after coma.
    - database:     Database name

    **Optional** (defaults are in bold)
    - a_mode:       **engine** | conn
    - a_autocommit:   True | **False**

    - a_username:   If left, use Windows auth.
    - a_password:
    """


    # Default values
    #-----------------
    mode      = 'engine'
    ac        = False
    username  = ''
    password  = ''
    c         = ''

    # Get dynamic argument
    for k,v in kwargs.items():
        # Check all arguments
        # ---------------------------
        #print("%s = %s" % (k, v))

        #------------------------
        if k == 'a_mode':
            mode = v
        if k == 'a_autocommit':
            ac = v
        if k == 'a_username':
            username = v
        if k == 'a_password':
            password = v

    #-------------------------------------------------------------------------------------
    conn_string_base = "DRIVER={SQL Server};SERVER=" + hostname + ";DATABASE=" + database
    #-------------------------------------------------------------------------------------
    if  (len(username)>0) & (len(password)>0):
        conn_string = conn_string_base+";UID="+username+";PWD="+password
    else:
        conn_string = conn_string_base+";Trusted_Connection=Yes;"

    try:
        print('📢 CONNECTING TO:')
        print('   Hostname   :', hostname)
        print('   Database   :', database)

        if mode == 'conn':
            import pyodbc

            # SQL Server Database Connection
            result = pyodbc.connect(conn_string, autocommit=ac)

            print('   Mode       : CONNECTION')
            print('   Autocommit : {ac}')

            c = result.cursor()

        if mode == 'engine':
            from sqlalchemy import create_engine
            import urllib.parse

            # SQLAlchemy

            params = urllib.parse.quote(conn_string)
            result  = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

            print('   Mode       : ENGINE')

            conn = result.raw_connection()
            c = conn.cursor()

        c.execute('SELECT @@version')
        res = c.fetchall()
        print('✅ ',res[0][0])

        return result

    except Exception as ex:
        print('----------------------------------------------------------------')
        print('❌ DB Connection ERROR ❌\n  ',ex)

def oracle(hostname, database, **kwargs):
    """
    #*Oracle connection engine for Python.*

    ---
    ### Arguments:
    **Mandatory**
    - hostname: Host IP or Name. Non-default port number goes after coma.
    - database: Database name

    **Optional** (defaults are in bold)
    - a_mode:       **engine** | conn
    - a_autocommit:   True | **False**

    - a_username:
    - a_password:
    """


    # Default values
    #-----------------
    mode      = 'engine'
    username  = ''
    password  = ''
    db_port   = '1521'

    # Get dynamic argument
    for k,v in kwargs.items():
        # Check all arguments
        # ---------------------------
        #print("%s = %s" % (k, v))

        #------------------------
        if k == 'a_mode':
            mode = v
        if k == 'a_port':
            db_port = v
        if k == 'a_username':
            username = v
        if k == 'a_password':
            password = v

    try:
        print('📢 Connecting to:', hostname, database)
        print('----------------------------------------------------------------')

        if mode == 'conn':
            import cx_Oracle

            # Connetcion string to Oracle database
            # ------------------------------------------------------------------------------------
            conn = cx_Oracle.connect(username, password, hostname+'/'+database, encoding="UTF-8")
            # ------------------------------------------------------------------------------------

            cur = conn.cursor()
            cur.execute ('SELECT * FROM v$version')
            result = cur.fetchone()
            cur.close()

            print('📢 DB Connection SUCCESS on:', database)
            print('----------------------------------------------------------------------------\n')
            print(result[0])

            return conn

        if mode == 'engine':
            from sqlalchemy import create_engine

            oracle_connection_string = 'oracle+cx_oracle://{usr}:{pwd}@{host}:{port}/{db}'

            engine = create_engine(
                oracle_connection_string.format(
                    usr  = username,
                    pwd  = password,
                    host = hostname,
                    port = db_port,
                    db   = database
                )
            )
            return engine
    except:
            print('DB Connection ERROR\n')

def postgresql(hostname, database, **kwargs):
    import psycopg2 as pg

    # Default values
    #-----------------
    mode      = 'engine'
    username  = ''
    password  = ''
    c         = ''

    # Get dynamic argument
    for k,v in kwargs.items():
        # Check all arguments
        # ---------------------------
        #print("%s = %s" % (k, v))

        #------------------------
        if k == 'a_mode':
            mode = v
        if k == 'a_username':
            username = v
        if k == 'a_password':
            password = v

    try:
        print('📢 CONNECTING TO:')
        print('   Hostname :', hostname)
        print('   Database :', database)

        if mode == 'conn':
            #  Define database connection
            result = pg.connect(f'host={hostname} dbname={database} user={username} password={password}')

            # Checking database connection
            #-----------------------------------------------------
            c = result.cursor()
            print('   Mode     : CONNECTION')

        if mode == 'engine':
            from sqlalchemy import create_engine

            result = create_engine(f"postgresql+psycopg2://{username}:{password}@{hostname}/{database}")
            print('   Mode     : ENGINE')

            conn = result.raw_connection()
            c = conn.cursor()

        c.execute("select version()")
        data = c.fetchone()

        #from tabulate import tabulate
        #table = [['Hostname',hostname],['Database',database],['Mode','ENGINE']]
        #print(tabulate(table, tablefmt='psql'))

        print(f'✅ {data[0]}\n')

        return result

    except Exception as ex:
        print('----------------------------------------------------------------')
        print('❌ DB Connection ERROR ❌\n  ',ex)

def exec_query(conn, query_list):
    c = conn.cursor()
    for q in query_list:
        c.execute(q)
        conn.commit()
    c.close()
