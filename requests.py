from db import DatabaseConfig, ConnectionPool


class TaskManager:
    """Class for managing tasks in the database."""

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def execute_sql(self, sql, params=None, is_fetch=False):
        """Execute a SQL command with optional parameters and fetching."""
        conn = self.connection_pool.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if is_fetch:
                    return cur.fetchall()
                else:
                    conn.commit()
        except Exception as e:
            print(f"An error occurred while executing SQL: {e}")
        finally:
            self.connection_pool.put_connection(conn)

    def perform_queries(self, queries):
        """Perform a list of queries on the database."""
        for query, params, is_fetch in queries:
            result = self.execute_sql(query, params, is_fetch)
            if result:
                for row in result:
                    print(row)
            print("---------------------------")  # Separator for query results


if __name__ == "__main__":
    config = DatabaseConfig(".env")
    pool = ConnectionPool(config)
    task_manager = TaskManager(pool)

    queries = [
        # Get all tasks for a specific user
        (
            "SELECT * FROM tasks WHERE user_id = %s",
            (1,),
            True,
        ),  # Replace 1 with the actual user_id
        # Select tasks with a specific status, e.g., 'new'
        (
            "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s)",
            ("new",),
            True,
        ),
        # Update the status of a specific task to 'in progress'
        (
            "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s",
            ("in progress", 1),
            False,
        ),  # Replace 1 with the actual task_id
        # Get list of users who have no tasks
        ("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)", None, True),
        # Add a new task for a specific user
        (
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)",
            ("New Task", "Task Description", "new", 1),
            False,
        ),  # Replace 'new' and 1 with the actual status and user_id
        # Get all tasks that are not completed
        (
            "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = %s)",
            ("completed",),
            True,
        ),
        # Delete a specific task
        (
            "DELETE FROM tasks WHERE id = %s",
            (1,),
            False,
        ),  # Replace 1 with the actual task_id
        # Find users with a specific email domain
        (
            "SELECT * FROM users WHERE email LIKE %s",
            ("%@example.com",),
            True,
        ),  # Replace example.com with the actual domain
        # Update a user's name
        (
            "UPDATE users SET fullname = %s WHERE id = %s",
            ("New Name", 1),
            False,
        ),  # Replace 'New Name' and 1 with the actual name and user_id
        # Get count of tasks for each status
        (
            "SELECT status.name, COUNT(tasks.id) FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name",
            None,
            True,
        ),
        # Get tasks assigned to users with a certain email domain
        (
            "SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s",
            ("%@example.com",),
            True,
        ),  # Replace example.com with the actual domain
        # Get list of tasks that have no description
        (
            "SELECT * FROM tasks WHERE description IS NULL OR description = ''",
            None,
            True,
        ),
        # Select users and their tasks which are 'in progress'
        (
            "SELECT users.*, tasks.* FROM users INNER JOIN tasks ON users.id = tasks.user_id WHERE tasks.status_id = (SELECT id FROM status WHERE name = %s)",
            ("in progress",),
            True,
        ),
        # Get users and the count of their tasks
        (
            "SELECT users.id, users.fullname, COUNT(tasks.id) AS task_count FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id",
            None,
            True,
        ),
    ]

    task_manager.perform_queries(queries)
    pool.close_all_connections()  # Close all connections when done
