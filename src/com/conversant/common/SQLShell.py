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

    def execute(self, sql, params, processor):
        self.command.execute(sql, params, processor)

    def __del__(self):
        self.close()

    def close(self):
        if self.command is not None:
            self.command.close()
            self.command = None
