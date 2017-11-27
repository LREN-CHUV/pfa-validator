#!/usr/bin/env python2.7

"""
  Insert fake data into woken database
"""

import os


def main():
    db_host = os.environ.get('DB_HOST', 'db')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'woken')
    db_user = os.environ.get('DB_USER', 'woken')
    db_password = os.environ.get('DB_PASSWORD')
    db_table = os.environ.get('DB_TABLE', 'job_result')
    db_column = os.environ.get('DB_COLUMN', 'data')

    # TODO: insert JSON documents from data folder into DB


if __name__ == '__main__':
    main()
