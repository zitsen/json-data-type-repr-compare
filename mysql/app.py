#!/usr/bin/env python
import mysql.connector
import json

cnx = mysql.connector.connect(user="root", password="example", host="mysql")
cursor = cnx.cursor()
cursor.execute("create database if not exists test")
cursor.execute("use test")
cursor.execute("create table  if not exists `test_json` (v json)")

v = json.dumps({"a": "b"})
cursor.execute("insert into `test_json` values('%s')" % v)

cursor.execute("select v from `test_json`")
(value,) = cursor.fetchone()
print(value, type(value))

cursor.close()
cnx.close()
