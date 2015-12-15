# coding=utf-8

import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")

cur = conn.cursor()


def add_user(username, password):
    sql = "INSERT INTO USER (username,password) VALUE ('%s','%s')" % (username, password)
    cur.execute(sql)
    conn.commit()


def is_existed(username, password):
    sql = "SELECT * FROM USER WHERE username = '%s' AND password = '%s'" % (username, password)
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True
