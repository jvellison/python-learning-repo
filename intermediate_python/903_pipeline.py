import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

from utils import clean_903_table
from datetime import datetime

# Check everything is working
# print('Code working') #can do before start code to check everything is working

# Session variables (change per session)
filepath = "/workspaces/python-learning-repo/intermediate_python/data/903_database.db"
collection_year = 2014
collection_end = datetime(collection_year, 3, 31)

engine_903 = create_engine(f"sqlite+pysqlite:////{filepath}") #neater, easier to read

#new_string = "sqlite+pysqlite:" + filepath #same as above

connection = engine_903.connect()

inspection = inspect(engine_903)
table_names = inspection.get_table_names()

# Uncomment to check connection to database
# print(table_names)

metadata_903 = MetaData()

# #Dictionary example
# dict_1 = {"key 1":1,
#           "key 2":2}

dfs = {}
for table in table_names:
    # print(table)    
    current_table = Table(table, metadata_903, autoload_with = engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table) # give everything from table
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Uncomment to check reading data frames
# print(dfs.keys())
# print(dfs['header']) # print the table called 'header'

# clean_903_table()

for key, df in dfs.items():
    # print(key,df)
    dfs[key] = clean_903_table(df, collection_end)

print(dfs['header'])