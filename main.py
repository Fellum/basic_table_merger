import pandas as pd
import sys
from os import walk


def preprocess_table(table):
    if "Фамилия" not in table.columns or "Имя" not in table.columns or "Отчество" not in table.columns:
        print("Didnt found separated name fields, loking for ФИО field")
        if "ФИО" not in table.columns:
            print("Didnt found ФИО column, exit")
            exit(0)
        tmp = table.ФИО.str.split(expand=True)
        tmp.columns = ["Фамилия", "Имя", "Отчество", "tmp"]
        tmp[["tmp"]] = tmp[["tmp"]].fillna('')
        tmp[["Отчество"]] = tmp[["Отчество"]].fillna('')
        tmp["Отчество"] = tmp[['Отчество', 'tmp']].apply(lambda x: ' '.join(x), axis=1)
        table[["Фамилия", "Имя", "Отчество"]] = tmp[["Фамилия", "Имя", "Отчество"]]
    table["Отчество"] = table["Отчество"].fillna('')
    table["Отчество"] = table['Отчество'].str.strip()
    table["Фамилия"] = table["Фамилия"].str.strip()
    table["Имя"] = table["Имя"].str.strip()


def main(basename, lookname):

    f = []
    for (dirpath, dirnames, filenames) in walk(lookname):
        f.extend(filenames)

    x1 = pd.ExcelFile(basename)
    dfb = x1.parse(x1.sheet_names[0])
    preprocess_table(dfb)
    if "Номер счета" not in dfb.columns:
        print("Didnt found Номер счета column, exit")
        exit(0)

    dfb = dfb[["Фамилия", "Имя", "Отчество", "Номер счета"]]
    print(dfb)
    res = None
    for file in f:

        x2 = pd.ExcelFile(lookname + "/" + file)
        dft = x2.parse(x2.sheet_names[0])

        preprocess_table(dft)
        dft = dft[["Фамилия", "Имя", "Отчество"]]
        print(lookname + "/" + file)
        print(dft)
        tmp = pd.merge(dft, dfb, "inner", on=["Фамилия", "Имя", "Отчество"])
        res = pd.concat([res, tmp])
    res.to_excel("res.xlsx", index=False, header=False)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: path_to_base path_to_folder")
