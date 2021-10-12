#!/usr/bin/env python
import mariadb
import json
from mariadb.constants import FIELD_TYPE


def load_json(value):
    return json.loads(value)


converter = {**{FIELD_TYPE.JSON: load_json}}

cnx = mariadb.connect(user="root", password="example", host="mysql")
cursor = cnx.cursor()
cursor.execute("create database if not exists test")
cursor.execute("use test")
cursor.execute("create table  if not exists `test_json` (v json)")

v = json.dumps({"a": "b"})
cursor.execute("insert into `test_json` values('%s')" % v)

cursor.execute("select v from `test_json`")
(value,) = cursor.fetchone()
print("without converter:", value, type(value))
cursor.close()
cnx.close()

cnx_con = mariadb.connect(
    user="root", password="example", host="mysql", db="test", converter=converter
)
cursor = cnx_con.cursor()
cursor.execute("insert into `test_json` values('%s')" % v)
cursor.execute("select v from test_json")
(value,) = cursor.fetchone()
print("with converter   :", value, type(value))

cursor.close()
cnx_con.close()
