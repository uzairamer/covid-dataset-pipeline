import psycopg2

try:

    conn = psycopg2.connect(
        host="db",
        database="dev",
        user="dev",
        password="kP/]^hGb}_F:`>a_GE(H>Zb+LJ^/t;aQcQU86d$\*2"
    )
    conn.set_session(autocommit=True)
    cursor = conn.cursor()
    from ingestions.covid.database_queries import DatabaseQuery
    cursor.execute(DatabaseQuery.create_covid_record_table())

    
    cursor.executemany(DatabaseQuery.insert_covid_record(), vendors_list)
    print(cursor.execute('SELECT * from vendors;'))

except Exception as e:
    print(e)
finally:
    if conn is not None:
        conn.close()

