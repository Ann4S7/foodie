import psycopg2


class DatabaseContextManager:

    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                           host=self.host, port=self.port)

        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type:
            print(exc_type, exc_value, exc_tb)
