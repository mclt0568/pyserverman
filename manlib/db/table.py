from typing import Dict, Iterable

from .database import Database
from .type import type_mapping


class Table:
    def __init__(self, db: Database, name: str, schema: Dict[str, type] = None) -> None:
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
        return self.db.query_one(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.name}';") is not None

    def create(self) -> None:
        if not self.exists():
            fields = []

            if self.schema is not None:
                for column_name, column_type in self.schema.items():
                    fields.append(f"{column_name} " + type_mapping[column_type].name)

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
