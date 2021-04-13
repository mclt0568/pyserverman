import sqlite3
import threading
from typing import Any, Iterable


# READ BEFORE USING
# this object is thread-safe it can be used in multiple threads simultaneously
# one and only one object should be used for one database file
class Database:
    def __init__(self, filename: str) -> None:
        self._db_conn = sqlite3.connect(filename, check_same_thread=False)
        self._db_conn_lock = threading.Lock()

    def __del__(self) -> None:
        self._db_conn.close()

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
    def query_one(self, sql: str, args: Iterable = ()) -> Any:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchone()

        cursor.close()
        return results

    # execute sql, fetch {wanted_results_count} lines of rows and return results
    # return None if no results
    def query_many(self, wanted_results_count: int, sql: str, args: Iterable = ()) -> Any:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchmany(wanted_results_count)
        if results == []:
            results = None

        cursor.close()
        return results

    # execute sql, fetch all returned rows and return the rows
    # return None if no returned rows
    def query_all(self, sql: str, args: Iterable = ()) -> Any:
        cursor = self._new_cursor()
        cursor.execute(sql, args)

        results = cursor.fetchall()
        if results == []:
            results = None

        cursor.close()
        return results
