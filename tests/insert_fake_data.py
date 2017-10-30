"""
  Insert fake data into woken database
"""

import os
import sys
import psycopg2
from psycopg2 import sql

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'woken')
DB_USER = os.environ.get('DB_USER', 'woken')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_TABLE = os.environ.get('DB_TABLE', 'job_result')
DB_COLUMN = os.environ.get('DB_COLUMN', 'data')
