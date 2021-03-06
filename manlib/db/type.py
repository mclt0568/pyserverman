from enum import Enum


class Type(Enum):
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    REAL = "REAL"


type_mapping = {
    int: Type.INTEGER,
    float: Type.REAL,
    str: Type.TEXT
}

type_mapping_reversed = {
    Type.INTEGER: int,
    Type.REAL: float,
    Type.TEXT: str
}
