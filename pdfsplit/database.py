import sqlite3
from pathlib import Path
import os

import pdfsplit as psp


def load_sql(cmd):
    loc = Path(os.path.realpath(__file__)).parent / cmd
    with open(loc, "r") as f:
        sql_file = f.read()
    if ";" in sql_file:
        yield from sql_file.split(";")
    else:
        yield sql_file


def create_empty_db(db_loc: str) -> None:
    con = sqlite3.connect(db_loc)

    sql_commands = load_sql("sql/schema.sql")
    for cmd in sql_commands:
        con.execute(cmd)

    con.commit()
    con.close()


def populate_db(db_loc: str, uri: str, pages, tags):
    con = sqlite3.connect(db_loc)
    # insert data into db
    con.execute("INSERT or REPLACE into pdfs VALUES(?)", (uri,))
    con.commit()
    for pnum, image in pages:
        page_tags = tags.get(int(pnum), None)
        if page_tags is None:
            continue
        con.execute("INSERT or REPLACE into pages VALUES(?,?,?)", (uri, pnum, image))
        con.executemany(
            "INSERT or REPLACE into pagetags VALUES(?,?,?)",
            ((tag, uri, pnum) for tag in page_tags),
        )
        con.commit()

    con.close()
