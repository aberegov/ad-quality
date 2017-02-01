from com.conversant.common.SQLCommander import SQLCommander
from com.conversant.common.EnvConfig import EnvConfig


class SQLShell:
    command = None

    def __init__(self):
        config = EnvConfig()
        self.command = SQLCommander(
            config.database_login,
            config.database_password,
            config.database_host,
            config.database_database)
        config.clear()

    def iterate(self, sql, params,max_rows=-1):
        return self.command.iterate(sql, params, max_rows)

    def execute(self, sql, params, processor,max_rows=-1):
        self.command.execute(sql, params, processor, max_rows)

    def __del__(self):
        self.close()

    def close(self):
        if self.command is not None:
            self.command.close()
            self.command = None
