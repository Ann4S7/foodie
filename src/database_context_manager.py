import psycopg2
from psycopg2 import extensions
import traceback
import logging


class DatabaseContextManager:

    def __init__(self, database: str, user: str, password: str, host: str, port: int) -> None:
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self) -> extensions.cursor:
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                           host=self.host, port=self.port)

        logging.info(f"Connected to the database: {self.database}.",
                     extra={"extra_parameters": {
                         "database": self.database, "user": self.user, "host": self.host, "port": self.port
                     }})

        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type: type[Exception], exc_value: Exception, exc_tb: traceback) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        logging.info(f"Disconnected from the database: {self.database}.")

        if exc_type:
            print(exc_type, exc_value, exc_tb)
