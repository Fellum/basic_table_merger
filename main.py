import pandas as pd
import sys
from os import walk


def main(basename, lookname):

    f = []
    for (dirpath, dirnames, filenames) in walk(lookname):
        f.extend(filenames)

    x1 = pd.ExcelFile(basename)
    dfb = x1.parse(x1.sheet_names[0])
    dfb.columns = ["Фамилия", "Имя", "Отчество", "КЕК"]
    res = None
    for file in f:

        x2 = pd.ExcelFile(lookname + "/" + file)
        dft = x2.parse(x2.sheet_names[0])
        dft = dft.iloc[2:, 1:4]

        df_obj = dft.select_dtypes(['object'])
        dft[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        dft.columns = ["Фамилия", "Имя", "Отчество"]
        tmp = pd.merge(dft, dfb, "inner")
        res = pd.concat([res, tmp])
    res.to_excel("res.xlsx", index=False, header=False)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: path_to_base path_to_folder")
