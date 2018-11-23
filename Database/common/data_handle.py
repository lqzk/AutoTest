from AppAuto.common.json_handle import JsonHandle

import os
#p="common\\path_handle.py"即从项目一级目录开始
PATH=lambda P:os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),P))
database_config_path=PATH("data\\database_config.ini")


class DataHandle:
    def obtain_connect_parm(self):
        database_config_info = {}
        suffix_config_file = os.path.splitext(database_config_path)[1]
        if suffix_config_file == ".ini":
            import configparser
            database_config = configparser.ConfigParser()
            database_config.read(database_config_path, encoding="utf-8")
            database_config_info["host"] = database_config.get("connect", "host")
            database_config_info["port"] = database_config.get("connect", "port")
            database_config_info["user"] = database_config.get("connect", "user")
            database_config_info["passwd"] = eval(database_config.get("connect", "passwd"))
            database_config_info["db"] = database_config.get("connect", "db")
            database_config_info["charset"] = database_config.get("connect", "charset")

        elif suffix_config_file == ".json":
            database_config_info = JsonHandle(database_config_path).jData

        return database_config_info
        
