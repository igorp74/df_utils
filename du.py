"""
## DATAFRAME UTILS
*#A collection of useful functions for optimized and faster work with DataFrame*

---
👔 by Igor Perkovic

🛠 CREATED: 2020-10-13 08:39:29
📆 CHANGED: 2022-04-13 17:50:56

---
⚙ PREREQUISITES:
📘 Libraries: xlsxwriter, pandas, sqlalchemy

"""

import numpy as np
import pandas as pd

from datetime import datetime, timedelta


# Databases
def df_2_mssqlsrv(df, engine_name, schema_name, table_name, ifexist):
    print('Inserting into database...')

    # Optimal chunk-size for SQL Server import
    chunk_size=999//(df.shape[1]+1)

    try:
        df.to_sql(name=table_name, con=engine_name, schema=schema_name, index=False, if_exists=ifexist, chunksize=chunk_size, method='multi')
        print(f'Successfully INSERTED table: {table_name}\n')
    except:
        print(f'INSERT FAILED for {table_name}')

def df_2_sqlite(df, db_path, table_name):
    """
    *#Create a SQLite database file from DataFrame*

    ---
    ### Returns
    → SQLite file (database)

    ---
    ### Arguments:
    - df         (DataFrame)
    - db_path    (Path) Database name with path
    - table_name (str)  Table name

    """
    from sqlalchemy import create_engine

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    sqlite_connection = engine.connect()

    try:
        df.to_sql(table_name, sqlite_connection, if_exists='fail')
        print(f'Successfully created database {db_path} and table {table_name}')
    except:
        print('❌❌❌ Error creating SQLite database !❌❌❌')



# Excel
def get_xlsx_data(file, sheet):
    try:
        print('Getting the data from xlsx to DataFrame')
        df   = pd.read_excel(file, sheet_name = sheet)
        print('Successfully imported!\n')
        return df
    except:
        print('Oh, no! Data Import ERROR!')

def df_merged_headers(cl, delimiter):
    merged_headers = []
    for c in cl:
        tmp = []
        for i in c:
            if ('Unnamed' in str(i)) or ('*' in str(i)) or (i is np.nan) or ('None' in str(i)):
                pass
            else:
                tmp.append(str(i).replace('\n','').strip().upper())
        merged_headers.append(delimiter.join(tmp[0: len(tmp)]))
    return merged_headers

def get_xlsx(fn, **kwargs):
    """
    *#Gets data from one file and multiple worksheets*

    ---
    ### Returns
    → List of DataFrames - one DataFrame from each worksheet

    ---
    ### Arguments:
    fn (Path)            *Existing xlsx file*

    a_sn_list (list)     *List of desired sheet names*
    a_sn_col  (str)      *Column name for column with worksheet names*
    a_header_rows (int)  *Number of rows for handling multiple headers*
    a_delimiter   (str)  *Delimiter for merged header names*
    a_destination (Path) *Path and name of pickle file for saving the data localy*
    """

    # Default values
    #-----------------
    sn = []     # sheet names
    snc = ''
    nr = 0
    delimiter = '-'
    src_headers = 0
    dest_pick = ''

    # Get dynamic argument
    for k,v in kwargs.items():
        # Check all arguments
        # ---------------------------
        # print("%s = %s" % (k, v))

        if k == 'a_sn_list':
            sn  = v
        if k == 'a_sn_col':
            snc  = v
        if k == 'a_header_rows':
            nr = v
        if k == 'a_delimiter':
            delimiter = v
        if k == 'a_destination':
            dest_pick = v

    if nr > 1:
        src_headers = [i for i in range(nr)]

    xlsx = pd.ExcelFile(fn)
    sheets = xlsx.sheet_names
    print(sheets)

    dfs = []
    if sn:
        for ws in sn:
            print('Reading worksheet:',ws)
            print('headers: ', src_headers)
            df = xlsx.parse(ws, header=src_headers)
            if len(snc):
                df[snc] = ws
            if nr > 1:
                cl = df.columns.tolist()
                df.columns = df_merged_headers(cl, delimiter)
            print('Appending in general list...')
            dfs.append(df)

        res = pd.concat(dfs)
        res.columns = res.columns.str.replace('\n', '')

        res.reset_index(drop=True, inplace=True)
        res.dropna(axis=1, how='all', inplace=True)
        res.dropna(axis=0, how='all', inplace=True)


        if len(dest_pick)>1:
            res.to_pickle(dest_pick)
            print('Created:',dest_pick)
        else:
            return res

def from_excel_ordinal(ordinal, _epoch0=datetime(1899, 12, 31)):
    # Convert Excel date shown as serial number into a date string
    if ordinal >= 60:
        ordinal -= 1  # Excel leap year bug, 1900 is not a leap year!
    return (_epoch0 + timedelta(days=ordinal)).replace(microsecond=0)

def df_append_2_xlsx(df, file_name, sheet_name):
    """
    *#Appends data from DataFrame to a new worksheet in existing file.*

    ### Prerequisites:
    pip install openpyxl

    ---
    ### Returns
    → File list

    ---
    ### Arguments:
    df         (DataFrame) *your data*
    file_name  (Path)      *Existing xlsx file*
    sheet_name (str)       *Sheet Name for a new data*
    """

    from openpyxl import load_workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.styles import Font,PatternFill

    try:
        wb = load_workbook(file_name)
        writer = pd.ExcelWriter(file_name, engine='openpyxl')
        writer.book = wb
        new_sheet = wb.create_sheet(title=sheet_name)

        # Freeze 1st row
        for r in dataframe_to_rows(df, index=False, header=True):
            new_sheet.append(r)
        new_sheet.freeze_panes = 'A2'

        # Header row style
        fg_style = Font(color='00FFD966', bold=True)
        bg_style = PatternFill("solid", start_color="000d0d0d")

        for y in range(1, new_sheet.max_column+1):
            new_sheet.cell(row=1, column=y).font = fg_style
            new_sheet.cell(row=1, column=y).fill = bg_style

        writer.save()
        print(f'✔ Successfully append sheet: {sheet_name}\n   to file: {file_name}')
    except:
        print(f'❌❌❌ Cannot open or write to file: {file_name}.\nIs it open ?')

def df_2_xlsx(df, fn, sn, **kwargs):
    """
    *#Saves Dataframe(s) to worksheet(s) in Excel xlsx file.*

    ---
    ### Returns:
    → Single xlsx file with worksheet(s) from dataframe data

    ---
    ### Arguments:
    - df             (DataFrame)
    - fn             (Path(str))  File Name[s]
    - sn             (str)        Sheet Name[s]
    - a_tc           (hex color)  tab color
    - a_tab_colors   (hex color)  list of tab colors for every sheet
    - a_ac           (int)        0 = Off,    1 = On    (Auto-resize column)
    - a_style        (int)        0 = Header, 1 = Table
    - a_table_style  (str)        Name of Excel table style
    - a_multi        (int)        0 = Single, 1 = Multi (if a_mode=1, dataframes and worksheets in arguments need to be in a list form)
    - a_properties   (dict)       custom file properties
    - a_index        (boolean)    Print with index True or False
    """

    #-----------------
    # Default values
    #-----------------
    tc  = '#e6e6e6'
    if 'list' in str(type(df)):
        tcl = [tc]*len(df)
    ac  = 1
    m   = 0
    s   = 0
    ind = False
    ts  = 'Table Style Medium 2'
    wsp = {
            'author':   'IgorP',
            'company':  'Private',
            'category': 'Report',
          }

    # Get dynamic argument
    for k,v in kwargs.items():
        if k == 'a_tc':
            tc = v
        if k == 'a_tab_colors':
            tcl = v
        if k == 'a_ac':
            ac = v
        if k == 'a_style':
            s = v
        if k == 'a_table_style':
            ts = v
        if k == 'a_multi':
            m = v
        if k == 'a_properties':
            wsp = v
        if k == 'a_index':
            ind = v

    import xlsxwriter
    import pandas as pd

    def get_col_widths(dataframe):
        idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

    writer = pd.ExcelWriter(fn, engine='xlsxwriter')

    # Declare Excel Workbook
    workbook  = writer.book

    # Workbook properties
    workbook.set_properties(wsp)

    format_dict = {
        'bold'       : True,
        'text_wrap'  : True,
        'valign'     : 'middle',
        'font_color' : '#ffdf3c',
        'fg_color'   : '#232323',
        'border'     : 1
        }


    if m==0:
        if 'DataFrame' in str(type(df)):

            # Create worksheet Data with data from dataframe
            df.to_excel(writer, sheet_name=sn, index=ind)

            # Cosmetic - auto-fit columns
            #-----------------------------------------------
            ws = writer.sheets[sn]

            if ac:
                for i, width in enumerate(get_col_widths(df)):
                    ws.set_column(i-1, i-1, width+2)

            # Style
            #------------------------------------
            if s:
                # Table style format
                #--------------------
                cols = []
                for c in (df.columns.values):
                    cols.append({'header': c})

                ws.add_table(0, 0, len(df.index), len(df.columns)-1, {'columns': cols, 'style': ts})

            else:
                # Header formatting (option instead of Table Style)
                # -------------------------------------------------
                header_format = workbook.add_format(format_dict)

                for col_num, value in enumerate(df.columns.values):
                    ws.write(0, col_num, value, header_format)

            # Color the tabs
            ws.set_tab_color(tc)
            # Freeze 1st row
            ws.freeze_panes(1, 0)
            # Worksheet zoom level
            ws.set_zoom(80)

        else:
            print('This is not a single dataframe for process.')
            print('Exiting...')
            exit()
    else:
        if 'list' in str(type(df)):
            if len(df) == len(sn):
                for d,s, tagc in zip(df, sn, tcl):

                    # Skip empty worksheets
                    if d.empty:
                        pass
                    else:
                        d.to_excel(writer, sheet_name=s, index=False)

                        ws = writer.sheets[s]
                        for i, width in enumerate(get_col_widths(d)):
                            ws.set_column(i-1, i-1, width+2)

                        if s:
                            # Table style format
                            #--------------------
                            cols = []
                            for c in (d.columns.values):
                                cols.append({'header': c})

                            ws.add_table(0, 0, len(d.index), len(d.columns)-1, {'columns': cols, 'style': ts})

                        else:
                            # Header formatting (option instead of Table Style)
                            # -------------------------------------------------
                            header_format = workbook.add_format(format_dict)

                            for col_num, value in enumerate(d.columns.values):
                                ws.write(0, col_num, value, header_format)

                    # Color the tabs
                    ws.set_tab_color(tagc)
                    # Freeze 1st row
                    ws.freeze_panes(1, 0)
                    # Worksheet zoom level
                    ws.set_zoom(80)

            else:
                print('List of DataFrames | WorkSheets are not of the same size.')
                print('Exiting...')
                exit()
        else:
            print('This is not a list of dataframes!')
            print('Exiting...')
            exit()
    try:
        writer.save()
        print('\n ✔Successfully saved: 💾',fn)
    except xlsxwriter.exceptions.FileCreateError:
        print('\n\nERROR!!!\nCannot write in opened file.\nCLOSE THE FILE, PLEASE!\n')

def print_df(df, **kwargs):
    """
    Prints a DataFrame.

    ---
    ### Returns:
    → DataFrame information and values

    ---
    ### Arguments:

    🏁 FLAGS:  1 = ON, 0 = OFF

    ---

    df Dataframe         DataFrame
    d  DTypes            int
    dt DTypes tabular    int
    c  Columns           int
    v  Values            int
    vt Values tabular    int
    e  Exit after print  int

    """
    #-----------------
    # Default values
    #-----------------
    a_d  = 1
    a_dt = 0
    a_c  = 1
    a_v  = 1
    a_vt = 0
    a_e  = 1

    # Get dynamic argument
    for k,v in kwargs.items():

        if k == 'd':
            a_d  = v
        if k == 'dt':
            a_dt  = v
        if k == 'c':
            a_c  = v
        if k == 'v':
            a_v  = v
        if k == 'vt':
            a_vt  = v
        if k == 'e':
            a_e  = v

        if a_d==1 and a_dt==1:
            a_d  = 0

        if a_v==1 and a_vt>=1:
            a_v = 0


    print('\n📌 DATAFRAME INFO | Rows:', df.shape[0], 'Columns:', df.shape[1])

    if a_c:
        print('🟢 Columns:',df.columns.tolist(),'\n')

    if a_d:
        print (df.dtypes,'\n')

    if a_dt:
        from tabulate import tabulate

        acc = []
        dtypes  = df.dtypes.tolist()
        columns = df.columns.tolist()

        for c,d in zip(columns, dtypes):
            acc.append([c,d])

        dfd = pd.DataFrame(acc, columns=['Column', 'Dtype'])

        print(tabulate(dfd,headers=dfd.columns,  tablefmt='psql',showindex=False),'\n')

    if a_vt:
        from tabulate import tabulate
        if a_vt == 1:
            print(tabulate(df,headers=df.columns.tolist(),  tablefmt='simple',showindex=False),'\n')
        elif a_vt == 2:
            print(tabulate(df,headers=df.columns.tolist(),  tablefmt='psql',showindex=False),'\n')
        elif a_vt == 3:
            print(tabulate(df,headers=df.columns.tolist(), tablefmt='fancy_grid',showindex=False),'\n')

    if a_v:
        print('\n')
        for v in df.values.tolist():
            print(v)
    if a_e:
        exit()

def df_dtypes(df, mode):
    """
    *#Prints particular DataFrame typ4es*

    ---
    ### Returns
    → Text data

    ---
    ### Arguments:
    - df    (DataFrame)
    - mode  (int)
    ```
       0 = print
       1 = NUM column list
       2 = DAT column list
       3 = TXT column list
       4 = ALL columns list
    ```

    """

    tmp = []
    txt = []
    num = []
    dat = []

    dtypes  = df.dtypes.tolist()
    columns = df.columns.tolist()

    if mode == 0:
        for c,d in zip(columns, dtypes):
            print(d,'\t',c)
        exit()


    elif mode == 1:
        for c,d in zip(columns, dtypes):
            if d in ['float64', 'int64', 'int32']:
                print(d,'\t',c)
                num.append(c)
        return num

    elif mode == 2:
        for c,d in zip(columns, dtypes):
            if d in ['datetime64[ns]']:
                print(d,'\t',c)
                dat.append(c)
        return dat

    elif mode == 3:
        for c,d in zip(columns, dtypes):
            if d == 'O':
                print(d,'\t',c)
                txt.append(c)
        return txt

    else:
        for c,d in zip(columns, dtypes):
            tmp.append([c,d])
        return tmp

def split_df(df, lines = 1000):
    split_list = []
    num_chunks = len(df) // lines + 1
    for i in range(num_chunks):
        split_list.append(df[i*lines:(i+1)*lines])
    return split_list

def df_unique(df, col, id=0):
    res = df.loc[:,col].drop_duplicates()
    res.reset_index(drop=True, inplace=True)
    if id:
        res['ID'] = res.index
    return res

def clean_df(res, fillna=''):
    # Remove empty rows and columns
    res.dropna(how='all', axis=0, inplace=True)
    res.dropna(how='all', axis=1, inplace=True)

    # Strip leading and trailing spaces in column names
    res.columns = res.columns.str.strip()
    # Ensure unique column names
    res.columns = [x[1] if x[1] not in res.columns[:x[0]] else f"{x[1]}_{list(res.columns[:x[0]]).count(x[1])}" for x in enumerate(res.columns)]

    # Strip leading and trailing spaces in all columns
    res = res.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # Fillna
    if len(fillna):
        res.fillna(fillna,inplace=True)
    # Remove duplicates
    res = res.drop_duplicates()
    # Reindex
    res.reset_index(drop=True, inplace=True)

    return res
