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

    def iterate(self, sql, params, max_rows=-1):
        if self.connection is None:
            raise Exception("Connection is closed")

        cursor = self.connection.cursor()
        cursor.execute(sql, params)

        return SQLCommanderIterator(cursor, max_rows)

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
                ret = processor(rec)
                if ret is not None and not ret:
                    break
        finally:
            cursor.close()


class SQLCommanderIterator:
    def __init__(self,  cursor, max_rows = -1):
        self.row_num = 0
        self.cursor = cursor
        self.max_rows = max_rows

    def __iter__(self):
        try:
            for rec in self.cursor:
                self.row_num += 1
                if self.max_rows != -1 and self.row_num > self.max_rows:
                    break

                yield rec
        finally:
            self.cursor.close()
