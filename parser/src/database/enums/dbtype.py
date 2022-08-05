from enum import Enum

class DBTYPE(Enum):
    ELASTICSEARCH = "elasticsearch"

def parser_config_field(value: str) -> DBTYPE:
    for k, v in DBTYPE.__members__.items():
        if value == v.value:
            return v
    raise ValueError("Invalid Configuration Database :: " + str(value))
