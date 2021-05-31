from typing import Dict, Iterable

from .type import type_mapping
from .database import Database


class Table:
    def __init__(self, db: Database, name: str, schema: Dict[str, type] = {}) -> None:
        self.db = db

        self.name = name
        self.schema = schema

    def fetch_rows(self):
        return self.db.query_all(f"SELECT * FROM {self.name}")

    def fetch_column(self, column_name):
        result = self.db.query_all(f"SELECT {column_name} FROM {self.name}")
        if not result:
            return []
        return [i[0] for i in result]

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

    def delete(self, conditions: str) -> None:
        self.db.execute(f"DELETE FROM {self.name} WHERE {conditions};")
