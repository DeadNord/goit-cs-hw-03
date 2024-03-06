# database.py
import psycopg2
from psycopg2 import pool
from dotenv import dotenv_values

class DatabaseConfig:
    """Class to handle the database configurations."""
    def __init__(self, config_file):
        self.config = dotenv_values(config_file)

    def get_db_params(self):
        return {
            'dbname': self.config.get("DB_NAME"),
            'user': self.config.get("DB_USER"),
            'password': self.config.get("DB_PASSWORD"),
            'host': self.config.get("DB_HOST"),
            'port': self.config.get("DB_PORT")
        }

class ConnectionPool:
    """Class to manage a pool of database connections."""
    def __init__(self, db_config):
        params = db_config.get_db_params()
        self.pool = pool.SimpleConnectionPool(
            1, 20, **params
        )

    def get_connection(self):
        return self.pool.getconn()

    def put_connection(self, conn):
        self.pool.putconn(conn)

    def close_all_connections(self):
        self.pool.closeall()
        print("All database connections closed.")
