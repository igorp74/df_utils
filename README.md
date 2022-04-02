# df_utils
Set of pandas DataFrame functions which I use a lot in ETL data processing.

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
![screenshot_20220402-112943](https://user-images.githubusercontent.com/17882375/161377127-ff1ec00e-0f1a-43bf-ae09-7cebca5bcf11.png)


### Result:
Notice that first dataframe is printed as is, without cleaning, then for comparison, there is another print with cleaned dataframe.
![screenshot_20220402-112908](https://user-images.githubusercontent.com/17882375/161377122-f00161f0-8ab7-4a45-b561-90675d815760.png)
