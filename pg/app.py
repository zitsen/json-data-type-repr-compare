#!/usr/bin/env python
import psycopg
import json


cnx = psycopg.connect(user="postgres", password="example", host="postgres")
cursor = cnx.cursor()
cursor.execute("create table test_json (v json)")

v = json.dumps({"a": "b"})
cursor.execute("insert into test_json values('%s')" % v)

cursor.execute("select v from test_json")
(value,) = cursor.fetchone()
print(value, type(value))

cursor.close()
cnx.close()
