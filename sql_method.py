import sqlite3 as sql
import zrk_info as log

# Методы по работе в БД для цирка с конями
conn = sql.connect("Zirk.db")


def create_table(name, columns: dict):
    cursor = conn.cursor()
    sSQL = 'create table {} ('.format(name)
    for k, v in columns.items():
        sSQL = sSQL + k + ' ' + v
        if k == list(columns.keys())[-1]:
            sSQL = sSQL + ')'
        else:
            sSQL = sSQL + ','
    try:
        cursor.execute(sSQL)
        log.ok_print('table {} successfully created'.format(name))
    except Exception as e:
        log.err_print('Error while creating table {}'.format(name) + ' ' + str(e))


def drop_table(name):
    cursor = conn.cursor()
    sSQL = 'drop table {}'.format(name)
    try:
        cursor.execute(sSQL)
        log.ok_print('table {} dropped successfully'.format(name))
    except Exception as e:
        log.err_print("Can't drop table {}".format(name) + ': ' + str(e))


def getquery(sSQL):
    cursor = conn.cursor()
    log.ok_print('SQL: '+sSQL)
    try:
        cursor.execute(sSQL)
        log.ok_print('  rows selected: ' + str(len(list(cursor))))
    except Exception as e:
        log.err_print('SQL ERROR: ' + '\n' + sSQL + '\n' + str(e))
    return cursor


def insert(table, column: list):
    cursor = conn.cursor()
    sSQL = 'insert into {} values ('.format(table)
    for i, v in enumerate(column):
        if type(v) is int or type(v) is float:
            vv = str(v)
        else:
            vv = "'" + str(v) + "'"
        sSQL = sSQL + vv
        if i == len(column) - 1:
            sSQL = sSQL + ')'
        else:
            sSQL = sSQL + ','
    log.ok_print(sSQL)
    try:
        cursor.execute(sSQL)
        log.ok_print('1 row inserted into {}'.format(table))
    except Exception as e:
        log.err_print('Ошибка при Insert в таблицу {}: '.format(table) + str(e))


def getwhere(column: dict):
    sSQL = 'where 1=1 ' + '\n'
    for k, v in column.items():
        if type(v) is int or type(v) is float:
            vv = str(v)
        else:
            vv = "'" + str(v) + "'"
        sSQL = sSQL + 'and ' + k + ' = ' + vv + '\n'
    return sSQL


def isPrimary(table, column: dict):  # Проверяет, есть ли уже в таблице записи с такими значениями
    sSQL = 'select 1 from {} '.format(table) + getwhere(column)
    cursor = getquery(sSQL)
    if cursor.fetchone() is None:
        return True
    else:
        return False