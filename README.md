# JSON Data Type Representation in Python

Here we will test JSON data type representation for other database like
PostgreSQL/MySQL/MariaDB in Python.

Use docker-compose for test.

```yaml
version: "3.8"

services:
  postgres:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example
  pgjson:
    build: ./pg
    depends_on:
      - postgres
  mysql:
    image: mysql
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: example
  mysqljson:
    build: ./mysql
    depends_on:
      - mysql
  mariajson:
    build: ./mariadb
    depends_on:
      - mysql
```

Start database service(use mariadb connector with MySQL database).

```sh
alias dc=docker-compose
dc up -d mysql postgres

dc run --rm pgjson
dc run --rm mysqljson
dc run --rm mariajson
```

PostgreSQL code:

```python
#!/usr/bin/env python
import psycopg
import json

cnx = psycopg.connect(user="postgres", password="example", host="postgres")
cursor = cnx.cursor()
cursor.execute("create table test_json (v json)")


v = json.dumps({"a": "b"})
cursor.execute("insert into test_json values('%s')" % v)

cursor.execute("select v from test_json")
value, = cursor.fetchone()
print(value, type(value))

cursor.close()
cnx.close()
```

PostgreSQL json type result:

```sh
{'a': 'b'} <class 'dict'>
```

MySQL code:

```python
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
```

MySQL json type:

```sh
{"a": "b"} <class 'str'>
```

MariaDB connector code:

```sh
#!/usr/bin/env python
import mariadb
import json

cnx = mariadb.connect(user="root", password="example", host="mysql")
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
```

MariaDB python connector instead use `bytes`:

```sh
b'{"a": "b"}' <class 'bytes'>
```

For convenient usage, MariaDB connector provide an option `converter`:

```py
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
```

In this example, use a converter function for JSON type, automatically convert
JSON bytes to python dict(or other types) object.

```sh
without converter: b'{"a": "b"}' <class 'bytes'>
with converter   : {'a': 'b'} <class 'dict'>
```

## Summary

PostgreSQL automatically converts json to Python builtin object by default, MySQL official
connector uses `str` type, MariaDB uses `bytes` by default and provides a `converter`
option for a convenient way.

For TDengine, I prefer to use MariaDB-like way to represent JSON data type.
