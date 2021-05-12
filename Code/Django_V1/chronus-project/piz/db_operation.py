# -*- coding: utf-8 -*-


# !pip install psycopg2

import psycopg2


def connect_db():
    conn = None
    try:
        # connect to the PostgreSQL server
        # todo: using config file
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="MasterProject")

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


def close_connect(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')


def insert_data_info(user_id, data_id, data_path, conn):
    if conn is None:
        conn = connect_db()
    cur = conn.cursor()
    try:
        sql = """INSERT INTO data_info(user_id,data_id,data_path)
             VALUES(%s,%s,%s);"""
        cur.execute(sql, (user_id, data_id, data_path,))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        close_connect(conn)


def insert_model_info(model_id, version, project_type, model_path, model_type, is_default, conn):
    if conn is None:
        conn = connect_db()
    cur = conn.cursor()
    try:
        sql = """INSERT INTO model_info(model_id, version, project_type, model_path, model_type,is_default)
             VALUES(%s,%s,%s,%s,%s,%s);"""
        cur.execute(sql, (model_id, version, project_type, model_path, model_type, is_default,))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        close_connect(conn)


def get_user_dataID_list(conn, user_id):
    # check the how many data for one user
    if conn is None:
        conn = connect_db()
    cur = conn.cursor()
    try:
        sql = """SELECT * FROM data_info WHERE user_id = (%s);"""
        cur.execute(sql, (user_id,))
        data_id_records = cur.fetchall()
        # for data_id in data_id_records:
        #     print(data_id)
        conn.commit()
        cur.close()
        # return len(data_id_records) + 1
        return data_id_records

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_connect(conn)


# test
# insert_data_info("21321", "21321_20201118_0001", "/user_path/21321/20201118_0001.csv", None)

# print(get_user_dataID_list(None, "21321"))

#insert_model_info('20201118_model', 'DL_1.0', 'ECG', '/model_path/ECG/20201118_DL_1.0.h5', "DL", True, None)
