import argparse
import pandas as pn
import numpy as np


def read_excel(file_url):
    xl = pn.read_excel(file_url)
    del xl['Unnamed: 3']
    del xl['Marca temporal']


    xl = xl.replace(to_replace=r'(^a\).*)',
                    value='1',
                    regex=True)

    xl = xl.replace(to_replace=r'(^b\).*)',
                    value='-1',
                    regex=True)

    print(xl.columns.values.tolist())

    print(xl)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Nombre del archivo")
    args = parser.parse_args()
    if args.file:
        print("Archivo seleccionado: " + args.file)
        read_excel(args.file)
    else:
        print("No se selecciono ningun archivo")


if __name__ == '__main__':
    main()
