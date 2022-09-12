"""
## FILES and LISTS
*#A collection of useful functions for work with files and lists*

👔 by Igor Perković

🛠 CREATED: 2020-10-13 08:39:29
📆 CHANGED: 2022-09-07 11:05:42

---
⚙ PREREQUISITES:
📘 Libraries: pandas, rapidfuzz

"""

# List functions
#--------------------------------------------------
def transpose_list(list_in, na=None):
    """
    =============================

    🏷 Transposing a list of list

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - list_in  list
    - na       substitute for the empty positions

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → Transposed list
    """

    # First I need to find maximum length of all sublists
    max_len = max(len(s) for s in list_in)

    # then, in every other sublist with less than max items, append empty symbol
    for i in list_in:
        if len(i) < max_len:
            i.append(na)

    # Finally, prepare the result as a transposed list of lists
    res = [list(i) for i in zip(*list_in)]

    return res


def rotate_list(l,n):
    """
    =============================

    🏷 Rotate a list

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - l  list
    - n  number of positions for rotating to the righ

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → Rotated list
    """

    return [l[(i + n) % len(l)] for i, x in enumerate(l)]


def flatten_list(in_list):
    """
    =============================

    🏷 Flatten any embedded list

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - in_list    list for flattening

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → Flatten list generator object

    # ATTENTION:
    For getting result in another list,
    we need to iterate over generator
    or print object.

    # EXAMPLE:
    res_list = list(flatten(some_list))
    """

    for x in in_list:
        if isinstance(x, list) and not isinstance(x, (str, bytes)):
            yield from flatten_list(x)
        else:
            yield x


def remove_sublist(ml, ul) -> list:
    """
    ==================================================

    🏷 Remove items from main list

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――――――――――――――――――――――――
    - ml (list)  main_list from which I want to remove..
    - ul (list)  unwanted list istems

    🎯 RETURNS
    ―――――――――――――――――――――――――――――――――――――――――――――――――――
    → Reduced main list
    """

    return [x for x in ml if x not in ul]


def check_sublist(main_list, sub_list, exception=0) -> bool:
    """
    =============================

    🏷 Check if list conatins a whole or partial sublist

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - main_list    list in which I try to find..
    - sub_list     ..this sub-list
    - exception=0  with exception of n items. # Default is 0 which means all items of sub-list should be in main list to get True as a result.

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → True or False
    """

    sl = set(sub_list)
    res = [x for x in main_list if x in sl]

    if (len(res) == (len(sub_list) - exception)):
        return True
    else:
        return False


def list_2_pickle(src_list, fn):
    """
    ===============================================

    🏷 Converting and saving list to a pickle file

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - src_list (list)  Source list
    - fn       (Path)  File name

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → Saved file and message
    """

    import pickle

    print(f'Storing list into: 💾 {fn}')
    try:
        f = open(fn,'wb')
        pickle.dump(src_list,f)
        f.close()
        print('\n ✔Successfully saved: 💾',fn)
    except:
        print(f'❌ ERROR saving list into {fn} file.')


def pickle_2_list(fn) -> list:
    """
    ============================================

    🏷 Read serialized list from pickle to list

    📌 ARGUMENTS:
    ――――――――――――――――――――――――――――――――――――――――――――
    - fn (Path) file name

    🎯 RETURNS
    ――――――――――――――――――――――――――――――――――――――――――――
    → list

    """

    import pickle

    res = []
    with (open(fn, 'rb')) as pickle_file:
        while True:
            try:
                res = pickle.load(pickle_file)
            except EOFError:
                break
    print(f'✔ Successfully read {fn} file.')

    return res


def list_slice (list, chunks):
    """
    =================================================================

    🏷 Slice list to smaller and equal pieces (exept the last chunk)

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - list   (list) source list
    - chunks (int)  desired number of items in sublist

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → Nested list of sliced sublist of equal size
    """

    res = [list[x:x+chunks] for x in range(0, len(list), chunks)]
    return res


def replace_many(text, dic):
    """
    ==================================================================

    🏷 Multiple replacement in given text from replacement dictionary

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - text (str)        Text which will be changed
    - dic  (dictionary) Replace dictionary

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → New text
    """

    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def fuzzy_compare_lists(source_list, match_list, limit_level, fast=0):
    """
    =============================

    🏷 Compare 2 lists using RapidFuzz library with Levenstein algorithm.

    ⚙ Prerequisites:
    pip install rapidfuzz pandas

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - source_list (list[str])   Items that we will comapre
    - match_list  (list[str])   ...with items from this list
    - limit_level (int)         and use n best scores
    - fast        (int)         scorer is fuzz.QRatio

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → DataFrame
    """


    import pandas as pd
    from rapidfuzz import process, fuzz

    acc = [] #accumulator
    scorer_part = fuzz.WRatio

    if fast:
        scorer_part = fuzz.QRatio

    for e,i in enumerate(source_list):
        print(f'\nOriginal item: {i} | {e}/{len(source_list)}  {str(round(e/len(source_list)*100,2))}%)')
        print('----------------------------------------------------------')

        row = []
        row.append(i)

        res = process.extract(i, match_list, scorer=scorer_part, limit=limit_level)

        for e in range(limit_level):
            row.append(res[e][0])
            row.append(round(res[e][1],2))
            print(str(round(res[e][1],2)), '% |', res[e][0])

        acc.append(row)

    rc = ['Original']
    dc = []
    for r in range(limit_level):
        dc.append(f'Match {r+1}')
        dc.append(f'Score {r+1} [%]')

    final_cols = rc + dc
    report = pd.DataFrame(acc, columns=final_cols)

    return report



# File functions
#----------------------------------------------------------------

def new_folder(folder, mode=0):
    """
    ===========================

    🏷 Creates a new folder

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――――――――――――――――――
    - folder (Path)
    - mode   (int)  0 = Silent, 1 = With messages

    🎯 RETURNS
    ―――――――――――――――――――――――――――――――――――――――――――――
    → New folder
    """

    try:
        folder.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        if mode:
            print("Folder is already there")
        else:
            pass
    else:
        if mode:
            print("Folder was created")
        else:
            pass


def get_file_list(path, extension, mode=0):
    """
    =============================

    🏷 Gets the file list from given path.

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    path      (Path) Windows path to the source files
    extension (str)  File extension (.doc, .xlsx, ...) with wildcards
    mode      (int)  0 = full path
                     1 = File names only

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → File list
    """

    file_list  = []

    for f in path.glob(f'{extension}'):
        if mode == 1:
            file_list.append(f.name)
        else:
            file_list.append(f)

    return file_list


def split_by_size(path, file_list, size):
    """
    =============================

    🏷 Split file list into smaller lists of wanted overall size.

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - path      (Path)
    - file_list (list[str])
    - size      (int)       Desired size

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → a list with splitted sublists
    """

    from pathlib import Path
    # Accumulator
    acc = 0

    chunk_list = []
    global_list = []

    for f in file_list:
        fp = Path(path / f)
        file_size = fp.stat().st_size
        file_size_MB = round(file_size/1024/1024,2)
        acc = acc + file_size_MB
        print('Size:',file_size_MB,'MB', '📦', round(acc,2),'MB', '💾', fp.name)

        if acc < size:
            chunk_list.append(f)
            print('✔ Collecting more...')
        else:
            print('❌ Stop collecting ❌')
            chunk_list.append(f) # Get last element after full list
            global_list.append(chunk_list) # Add to global list
            # Reset chunk accumulator and list
            acc = 0
            chunk_list=[]

    return global_list


def cp_multi_2_one(file_list, dst_path):
    """
    =============================

    🏷 Copy files from many different folders to one destination folder.

    📌 ARGUMENTS:
    ―――――――――――――――――――――――――――――
    - file_list (list[str])
    - dst_path  (Path)      Destination path

    🎯 RETURNS
    ―――――――――――――――――――――――――――――
    → All files in one folder
    """

    import shutil
    from shutil import SameFileError
    from pathlib import Path

    cn = 0
    err = []
    print('⚙⚙⚙ Copying in process ⚙⚙⚙')
    for f in file_list:
        src = Path(f)

        try:
            shutil.copy(src, dst_path)
            print('🎯 Not existing file...', f)
            cn = cn + 1
        except SameFileError:
            print("➡ Skipping...Existing file", f)
            err.append(f)
        except:
            print("❌❌❌ Unknown error ❌❌❌", f)
            err.append(f)

    print('⚡⚡⚡  Copying is DONE!  ⚡⚡⚡')
    print(f'\n{cn} files successfully copied!')

    print(f'\n{str(len(err))} These files are not copied:')
    for e in err:
        print(e)
