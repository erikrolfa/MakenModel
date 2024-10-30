'''These are functions that transfer the scraped data to the database'''
import os
import sys
import sqlite3
import json


# pylint: disable=C0103

data_folder = 'data'

def get_db():
    '''Connects to sqlite database'''
    db_folder = 'var'
    db_filename = 'makenmodel.sqlite3'

    db_filename = os.path.join(db_folder, db_filename)

    database = sqlite3.connect(str(db_filename))

    database.execute("PRAGMA foreign_keys = ON")

    return database

def paints_to_instructions_map():

    filename = 'data/instruction_to_paint.txt'

    connection = get_db()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            pdf_name, paint_list = line.split('\t')

            paint_list = paint_list.replace('{', '')
            paint_list = paint_list.replace('}', '')
            paint_list = paint_list.replace("'", '')
            paint_list = paint_list.split(',')

            cur = connection.execute(
                "SELECT unique_instruction_identifier "
                "FROM instructions "
                "WHERE pdf_name = ?",
                (pdf_name,)
            )
            pdf_identifier = cur.fetchone()[0]

            for paint in paint_list:
                paint = paint.strip()
                if paint == 'set()':
                    continue
                cur = connection.execute(
                    "SELECT unique_paint_identifier "
                    "FROM paints WHERE paint_code = ?",
                    (paint,)
                )
                paint_identifier = cur.fetchone()[0]

                connection.execute(
                    "INSERT OR IGNORE INTO instructions_to_paints (unique_instruction_identifier, unique_paint_identifier) "
                    "VALUES (?, ?)",
                    (pdf_identifier, paint_identifier)
                )

    connection.commit()
    if connection is not None:
        connection.close()

if __name__ == "__main__":
    paints_to_instructions_map()