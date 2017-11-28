#!/usr/bin/env python2.7

"""
  Insert fake data into woken database
"""

import os
import sys
import fnmatch
import psycopg2
from psycopg2 import sql


DATA_DIR = './data'


def main():
    # Get DB info
    db_host = os.environ.get('DB_HOST', 'db')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'woken')
    db_user = os.environ.get('DB_USER', 'woken')
    db_password = os.environ.get('DB_PASSWORD')
    db_table = os.environ.get('DB_TABLE', 'job_result')

    # Get node
    node = os.environ.get('NODE', 'test_node')

    # Connect to DB
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()
    except psycopg2.Error as ex:
        print "Error while connecting to the database " + str(ex)
        sys.exit(1)

    # Find PFA documents to load
    pfa_files = find_pfa_files(DATA_DIR)

    # Insert document into DB
    job_id_iter = 1
    for pfa_file in pfa_files:
        job_id = str(job_id_iter)  # job_id = str(uuid.uuid1())
        with open(pfa_file, 'r') as f:
            data = f.read()
        sql_template = """
                  INSERT INTO {}
                  (job_id, node, data) VALUES (%s, %s, %s)
                """
        prepared_statement = sql.SQL(sql_template).format(
            sql.Identifier(db_table)
        )
        cur.execute(prepared_statement, [job_id, node, data])
        conn.commit()
        job_id_iter += 1
    conn.close()


def find_pfa_files(folder):
    matches = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, '*.pfa'):
            matches.append(os.path.join(root, filename))
    return matches


if __name__ == '__main__':
    main()
