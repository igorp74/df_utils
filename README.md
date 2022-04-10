# df_utils
Set of Data Engineering functions which I use a lot in ETL data processing.

It all started with print(df).. then print(df.values.tolist()).. then prettify with tabulate...
After some time and work, I noticed which parts of code I use the most and in every script, thus I made functions.
Fast forward.. after some amount of functions this is a logical step to Python module on PyPI (soon).

I use them as a local module

```python
import sys
sys.path.append(r"/home/igorp/Documents/CODE")
from df_utils import db, du, fi
```

I separate them in 3 different files: 
* ### **db** - for database connectors [wiki](https://github.com/igorp74/df_utils/wiki#db---for-database-connectors)
  * ***mssqlsrv***(sqlserver, database, **kwargs)
  * ***oracle***(hostname, database, **kwargs)
  * ***postgresql***(hostname, database, **kwargs)
* ### **du** - as dataframe utils
  * ***df_2_mssqlsrv***(df, engine_name, schema_name, table_name, ifexist)
  * ***df_2_sqlite***(df, db_path, table_name)
  * ***get_xlsx_data***(file, sheet)
  * ***df_merged_headers***(cl, delimiter)
  * ***get_xlsx***(fn, **kwargs)
  * ***from_excel_ordinal***(ordinal, _epoch0=datetime(1899, 12, 31))
  * ***df_append_2_xlsx***(df, file_name, sheet_name)
  * ***df_2_xlsx***(df, fn, sn, ac=1, m=0, s=0, sr=0)
  * ***print_df***(df, **kwargs)
  * ***df_dtypes***(df, mode)
  * ***split_df***(df, lines = 1000)
  * ***df_unique***(df, col, id=0)
  * ***clean_df***(res, fillna='')
* ### **fi** - as file and list helpers
  * ***remove_sublist***(main_list, unwanted_list)
  * ***check_sublist***(main_list, sub_list, exception=0)
  * ***list_2_pickle***(src_list, fn)
  * ***pickle_2_list***(fn)
  * ***list_slice***(list, chunks)
  * ***replace_many***(text, dic)
  * ***fuzzy_compare_lists***(source_list, match_list, limit_level, fast=0)
  * ***list_2_str***(source_list)
  * ***num_2_str***(data)
  * ***new_folder***(folder, mode=0)
  * ***get_file_list***(path, extension, mode=0)
  * ***split_by_size***(path, file_list, size)
  * ***cp_multi_2_one***(file_list, dst_path)

### 💡 Example 1 - Read xlsx
Let say I want to read an xlsx (MS Excel) file and print the content of a worksheet.

```python
import sys
sys.path.append('/home/igorp/Documents/CODE/GitHub') #place your path to the df_utils folder
from df_utils import du

from pathlib import Path

fn = Path(r'/home/igorp/Documents/CODE/MISC/Python/Proba.xlsx') # Place your path to the source xlsx file

# Now, just read xlsx
df = du.get_xlsx_data(fn, 'Milka')

# print raw DataFrame
du.print_df(df, vt=2, e=0)

# print cleaned DataFrame
res = du.clean_df(df)
du.print_df(res, vt=3)
```

### Source data:
![screenshot_20220405-231144](https://user-images.githubusercontent.com/17882375/161851292-3b150ef1-f5bd-4777-83e5-7d0e0aed2146.png)

### Result:
Notice that first dataframe is printed as is, without cleaning, then for comparison, there is another print with cleaned dataframe.

![screenshot_20220405-231858](https://user-images.githubusercontent.com/17882375/161851313-5fb66668-13f5-4cdd-b1e3-09da510b76d6.png)

### 💡 Example 2 - Connect to databases
In this example, I am going to connect to 2 databases; one local and one remote (Heroku).
I will query and collect some data from tables in both databases and left join them together to final result.

![screenshot_20220410-131902](https://user-images.githubusercontent.com/17882375/162615872-71bcdf4f-6fa9-4a4d-86de-e911a1cbf9cd.png)

### Code analysis

```python
# 🧰 My toolbox
import sys
sys.path.append(r"/home/igorp/Documents/CODE/GitHub")
from df_utils import db, du, up

import pandas as pd
from timeit import default_timer as timer
start = timer()

import sqlite3
# 🔑 My password vault...
conn = sqlite3.connect('/home/igorp/Documents/CODE/Vault/secure_box.sqlite')
```
Above code is header and declaration of modules I need in this script. Notice that I use SQLite local database for storing my passwords, so they cannot be visible in my scripts (like this one).

```python
# Local database (PostgreSQL)
host_name = '127.0.0.1'
database  = 'data'
user_name = 'root'
password  = up.get_password(conn, 1)

# Heroku database (PostgreSQL)
host_name2 = "ec2-52-208-254-158.eu-west-1.compute.amazonaws.com"
database2  = "da2g6qll5cjhkd"
user_name2 = "qkrfbcuatvnhha"
password2  = up.get_password(conn, 2)

engine = db.postgresql(host_name, database,
                     a_username = user_name,
                     a_password = password
                     )

engine2 = db.postgresql(host_name2, database2,
                     a_username = user_name2,
                     a_password = password2
                     )

ex= ''
```
Connection strings to both local and remote database and engine creation for both of them.

```python
try:
    df  = pd.read_sql("select id as professorid, first_name, last_name from dbo.professor_csv", con=engine)
    du.print_df(df, c=0, d=0, vt=2, e=0)

    df2 = pd.read_sql("select * from dbo.course_csv", con=engine2)
    du.print_df(df2, c=0, d=0, vt=2, e=0)
except Exception as ex:
    print(ex)
```
Here I am trying to run queries on each database and collect the results into the DataFrames.
Notice that I turned off columns (c=0), dtypes (d=0) and exit (e=0) 
in du.print_df(df, c=0, d=0, vt=2, e=0). I only left values tabular (vt=2).

```python
df_join = pd.merge(df2,df, how='left', on='professorid', indicator=True)
du.print_df(df_join, c=0, d=0, vt=2, e=0)
```
Left join between 2 dataframes. This is equivalent for left joining tables in SQL, as it is usual in pandas DataFrame environment. Indicator is turned ON (True), so I have got additional column in result DataFrame "_merge" with indicator do I have the joined data in **both** tables or just **left_only**

```python
proc_time = round(timer() - start,2)
print(f'\n⚡⚡⚡ ⏱ Done in: {proc_time} s ⚡⚡⚡')
```
This is processing time counter.
