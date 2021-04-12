from typing import Dict, Iterable
from .database import Database
from .type import type_mapping


class Table:
    def __init__(self, db: Database, name: str, schema: Dict[str, type] = {}) -> None:
        self.db = db

        self.name = name
        self.schema = schema

    def exists(self) -> bool:
        return self.db.query_one(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name}';") != None

    def create(self) -> None:
        if not self.exists():
            fields = []
            for name, type in self.schema.items():
                fields.append(f"{name} " + type_mapping[type].name)

            fields_str = ", ".join(fields)
            self.db.execute(f"CREATE TABLE {self.name} ({fields_str});")

    def insert(self, args: Iterable = ()) -> None:
        if args:
            values = []
            for arg in args:
                values.append(f"'{arg}'" if type(arg) == str else f"{args}")

            values_str = ", ".join(values)
            print(f"INSERT INTO {self.name} VALUES ({values_str});")
            self.db.execute(f"INSERT INTO {self.name} VALUES ({values_str});")
