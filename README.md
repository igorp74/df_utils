# df_utils
Set of Data Engineering functions which I use a lot in ETL data processing.
I separate them in 3 different files: 
* **db** - for database connectors
* **du** - as dataframe utils
* **fi** - as file and list helpers

It all started with print(df).. then print(df.values.tolist).. then prettify with tabulate...
After some time and work, I noticed which parts of code I use the most and in every script, thus I made functions.
Fast forward.. after some amount of functions this is a logical step to Python module on PyPI (soon).

I use them as a local module

```python
import sys
sys.path.append(r"/home/igorp/Documents/CODE")
from df_utils import db, du, fi
```

### Example
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
res = du.clean_df(df, fillna='///')
du.print_df(res, vt=3)
```

### Source data:
file:///home/igorp/Pictures/Screenshots/screenshot_20220405-231144.png

### Result:
Notice that first dataframe is printed as is, without cleaning, then for comparison, there is another print with cleaned dataframe.
file:///home/igorp/Pictures/Screenshots/screenshot_20220405-231858.png
