import sqlite3 as sql
import zrk_info as log

# Методы по работе в БД для цирка с конями


class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sql.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cursor = self.conn.cursor()


    def create_table(self, name, columns: dict):
        sSQL = 'create table {} ('.format(name)
        for k, v in columns.items():
            sSQL = sSQL + k + ' ' + v
            if k == list(columns.keys())[-1]:
                sSQL = sSQL + ')'
            else:
                sSQL = sSQL + ','
        try:
            self.cursor.execute(sSQL)
            log.ok_print('table {} successfully created'.format(name))
        except Exception as e:
            log.err_print('Error while creating table {}'.format(name) + ' ' + str(e))


    def drop_table(self, name):
        sSQL = 'drop table {}'.format(name)
        try:
            self.cursor.execute(sSQL)
            log.ok_print('table {} dropped successfully'.format(name))
        except Exception as e:
            log.err_print("Can't drop table {}".format(name) + ': ' + str(e))

    def getquery(self, sSQL):
        log.ok_print('SQL: ' + sSQL)
        try:
            self.cursor.execute(sSQL)
            log.ok_print('  rows selected: ' + str(len(list(self.cursor))))
        except Exception as e:
            log.err_print('SQL ERROR: ' + '\n' + sSQL + '\n' + str(e))
        return self.cursor


    def __del__(self):
        self.conn.close()





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


def commit():
    conn.commit()

def isPrimary(table, column: dict):  # Проверяет, есть ли уже в таблице записи с такими значениями
    sSQL = 'select 1 from {} '.format(table) + getwhere(column)
    ds = getquery(sSQL)
    if len(ds) is None:
        print('ret true')
        return True
    else:
        print('ret false')
        return False