from db import DatabaseConfig, ConnectionPool
from faker import Faker
import random

class DatabaseFiller:
    def __init__(self, connection_pool):
        self.pool = connection_pool
        self.fake = Faker()

    def fill_users(self, n=10):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cur:
                for _ in range(n):
                    fullname = self.fake.name()
                    email = self.fake.email()
                    cur.execute(
                        "INSERT INTO users (fullname, email) VALUES (%s, %s)",
                        (fullname, email),
                    )
                conn.commit()  # Commit transactions
                print(f"Inserted {n} fake users.")
        finally:
            self.pool.put_connection(conn)

    def fill_tasks(self, n=20):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users")
                user_ids = [row[0] for row in cur.fetchall()]

                for _ in range(n):
                    title = self.fake.sentence(nb_words=6)
                    description = self.fake.paragraph(nb_sentences=3)
                    status_id = random.randint(1, 3)
                    user_id = random.choice(user_ids)
                    cur.execute(
                        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                        (title, description, status_id, user_id),
                    )
                conn.commit()  # Commit transactions
                print(f"Inserted {n} fake tasks.")
        finally:
            self.pool.put_connection(conn)

if __name__ == "__main__":
    config = DatabaseConfig(".env")
    pool = ConnectionPool(config)
    filler = DatabaseFiller(pool)
    filler.fill_users(10)  # Insert 10 fake users
    filler.fill_tasks(20)  # Insert 20 fake tasks
    pool.close_all_connections()  # Close all connections when completely done
