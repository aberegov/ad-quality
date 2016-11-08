import psycopg2


class SQLCommander:
    connection = None

    def __init__(self, user, password, host, database):
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    def __del__(self):
        self.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute(self, sql, params, processor, max_rows=-1):
        if self.connection is None:
            raise Exception("Connection is closed")

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        row_num = 0

        try:
            for rec in cursor:
                row_num += 1
                if max_rows != -1 and row_num > max_rows:
                    break
                processor(rec)
        finally:
            cursor.close()
