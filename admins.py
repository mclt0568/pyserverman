from typing import List
import db


def create_table(database: db.Database) -> db.Table:
    table = db.Table(
        database,
        "admins",
        {
            "user_id": str
        }
    )

    table.create()

    return table


def get_admins(table: db.Table) -> List[str]:
    admin_user_ids = []

    admin_rows = table.db.query_all("SELECT user_id FROM admins;")
    for admin_row in admin_rows:
        admin_user_ids.append(admin_row[0])

    return admin_user_ids


def add_admin(table: db.Table, user_id: str) -> None:
    table.insert((user_id,))


def remove_admin(table: db.Table, user_id: str) -> None:
    table.db.execute("DELETE FROM admins WHERE admin_id=?;", (user_id,))
