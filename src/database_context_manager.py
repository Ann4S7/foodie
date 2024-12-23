import logging
import traceback

import psycopg2
from psycopg2 import extensions


class DatabaseContextManager:
    """The class has instance methods that allow to connect and work with the database."""

    def __init__(
        self, database: str, user: str, password: str, host: str, port: int
    ) -> None:
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def __enter__(self) -> extensions.cursor:
        """Connect to the database.
        Create the cursor object that allows Python code
        to execute PostgreSQL command in a database session.

        Returns: an object of the cursor class (this class is contained in the psycopg2 library).

        """
        self.connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

        logging.info(
            "Connected to the database.",
            extra={
                "extra_parameters": {
                    "database": self.database,
                    "user": self.user,
                    "host": self.host,
                    "port": self.port,
                }
            },
        )

        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(
        self, exc_type: type[Exception], exc_value: Exception, exc_tb: traceback
    ) -> None:
        """Disconnect from the database.
        Close the current cursor and free the associated resources.
        Close the connection."""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        logging.info("Disconnected from the database.")

        if exc_type:
            print(exc_type, exc_value, exc_tb)
