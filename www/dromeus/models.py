from .common import db, Field
from pydal.validators import *


# Define the database drivers available
db.define_table(
    "sys_db_drivers",
    Field(
        "driver_name",
        "string",
        length=32,
        required=True,
        unique=True,
        requires=[IS_NOT_EMPTY(), IS_UPPER(), IS_NOT_IN_DB(db, "sys_db_drivers.driver_name")],
    ),
    Field("description", "string"),
    format="%(driver_name)s",
)

db.define_table(
    "sys_connections",
    Field("driver", "reference sys_db_drivers", help="Database Driver"),
    Field(
        "connection_name",
        "string",
        required=True,
        unique=True,
        requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, "sys_connections.connection_name")],
        help="Database Connection Name",
    ),
    Field("hostname", "string", length=64, help="Hostname of Database Server"),
    Field("port", "integer", help="Database Port Number"),
    Field(
        "database",
        "string",
        length=64,
        help="Database Name or Path to SQLite Data File",
    ),
    Field("username", "string", length=32, help="Database Username"),
    Field("password", "password", help="User Password"),
    format="%(connection_name)s",
)


db.define_table('sys_library',
                Field('connection', 'reference sys_connections', help='Connection Name'),
                Field('sql_query', 'string', required=True, unique=True,
                      requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'sys_library.sql_query')]),
                Field('query', 'text', required=True,
                      requires=[IS_NOT_EMPTY()]),
                format='%(sql_query)s'
)

db.commit()
