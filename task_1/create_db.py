from db import DatabaseConfig, ConnectionPool

class DatabaseInitializer:
    """Class for initializing the database structure based on an SQL file."""
    def __init__(self, connection_pool, sql_file):
        self.pool = connection_pool
        self.sql_file = sql_file

    def create_tables(self):
        # Get a connection from the pool
        conn = self.pool.get_connection()
        if conn:
            try:
                # Reading SQL commands from the file
                with open(self.sql_file, 'r') as file:
                    sql_script = file.read()
                
                # Using a context manager to ensure that the cursor is properly closed
                with conn.cursor() as cur:
                    cur.execute(sql_script)
                    print("Tables created successfully")
            except Exception as e:
                print(f"Error executing SQL script: {e}")
            finally:
                # Return the connection back to the pool rather than closing it
                self.pool.put_connection(conn)

if __name__ == "__main__":
    config = DatabaseConfig(".env")
    pool = ConnectionPool(config)
    db_initializer = DatabaseInitializer(pool, "create_db.sql")
    db_initializer.create_tables()
    pool.close_all_connections()
