import sqlite3
import threading
from typing import Dict, Iterable, Optional

from .table import Table
from .type import Type, type_mapping_reversed


# READ BEFORE USING
# this object is thread-safe it can be used in multiple threads simultaneously
# one and only one object should be used for one database file
class Database:
    def __init__(self, filename: str) -> None:
        self._db_conn = sqlite3.connect(filename, check_same_thread=False)
        self._db_conn_lock = threading.Lock()

        self._tables = {}

        tables_schemas = self.query_all(
            "SELECT name, sql FROM sqlite_master WHERE type='table';")
        if tables_schemas:
            tables_schemas = [(i[0], self.parse_schema(i[1]))
                              for i in tables_schemas]
            for table_name, column_schema in tables_schemas:
                self._tables[table_name] = Table(
                    db=self,
                    name=table_name,
                    schema=column_schema
                )

    def __getitem__(self, key: str):
        return self._tables[key]

    def __iter__(self):
        for key, item in self._tables.items():
            yield key, item

    def __del__(self) -> None:
        self._db_conn.close()

    @staticmethod
    def parse_schema(schema: str = "") -> Dict[str, type]:
        raw_columns = schema.split("(")[-1][:-1]
        columns_schemas = [i.strip().split(" ")
                           for i in raw_columns.split(",")]
        columns_schemas = [(i[0], type_mapping_reversed[Type(i[1])])
                           for i in columns_schemas]
        schemas_dict = {}
        for column_name, column_type in columns_schemas:
            schemas_dict[column_name] = column_type
        return schemas_dict

    # create new cursor and return the new cursor
    def _new_cursor(self) -> sqlite3.Cursor:
        return self._db_conn.cursor()

    # save changes to file
    def save(self) -> None:
        with self._db_conn_lock:
            self._db_conn.commit()

    # execute sql and save
    def execute(self, sql: str, args: Iterable = ()) -> None:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        self.save()

        cursor.close()

    # execute sql, fetch one row and return result
    # return None if no result
    def query_one(self, sql: str, args: Iterable = ()) -> Optional[list]:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchone()

        cursor.close()
        return results

    # execute sql, fetch {wanted_results_count} lines of rows and return results
    # return None if no results
    def query_many(self, wanted_results_count: int, sql: str, args: Iterable = ()) -> Optional[list]:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchmany(wanted_results_count)
        if not results:
            results = None

        cursor.close()
        return results

    # execute sql, fetch all returned rows and return the rows
    # return None if no returned rows
    def query_all(self, sql: str, args: Iterable = ()) -> Optional[list]:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchall()
        if not results:
            results = None

        cursor.close()
        return results

    def get_table_names(self):
        return self._tables.keys()

    def get_table(self, name) -> Table:
        return self[name]

    def init_table(self, name: str, schema: Dict[str, type]) -> None:
        if name in self._tables:
            return
        self._tables[name] = Table(
            db=self,
            name=name,
            schema=schema
        )
        self._tables[name].create()

    def remove_table(self, name: str) -> None:
        if " " in name:
            return
        if name in self._tables:
            self.execute(f"DROP TABLE {name}")
