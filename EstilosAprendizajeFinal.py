import argparse
import base64
import os
import pandas as pn
import numpy as np
from matplotlib import pyplot as ptl
import matplotlib.backends.backend_pdf as mpdf


def read_excel(file_url, fileO_url):
    directory = fileO_url
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    xlp = pn.read_excel(file_url)  # se carga el archivo de excel a un pandas

    xlp = xlp.rename(
        columns={x: y for x, y in zip(xlp.columns, range(0, len(xlp.columns)))})  # se substituyen las cabeceras

    # se remplazan las respuestas a) y b), los datos del alumno van de la pos 0 a 4
    xlp = xlp.replace(to_replace=r'(^a\).*)',
                      value=-1,
                      regex=True)

    xlp = xlp.replace(to_replace=r'(^b\).*)',
                      value=1,
                      regex=True)
    # se crea el data set de resultados
    data_result = pn.DataFrame({'NAME': xlp.loc[:, 2], 'EMAIL': xlp.loc[:, 1], 'TIMESTAMP': xlp.loc[:, 0],
                                'AGE': xlp.loc[:, 3], 'TEACHER': xlp.loc[:, 6], 'SCHOOL': xlp.loc[:, 4],
                                'SEMESTER': xlp.loc[:, 5]})
    # se ordenan los valores
    data_result = data_result.sort_values(by=['TEACHER', 'TIMESTAMP'], ascending=False)

    # se eliminan las columnas innecesarias
    xlp = xlp.drop(xlp.columns[[0, 1, 2, 3, 4, 5, 6]], axis=1)

    xlp = xlp.rename(
        columns={x: y for x, y in zip(xlp.columns, range(0, len(xlp.columns)))})  # se substituyen las cabeceras

    # se asigan las nuevas columnas vacias
    data_result['AR'], data_result['SI'], data_result['VV'], data_result['SG'] = [np.nan, np.nan, np.nan, np.nan]

    # se calculan los estilos

    data_result['AR'] = xlp.loc[:, [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]].sum(axis=1)
    data_result['SI'] = xlp.loc[:, [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41]].sum(axis=1)
    data_result['VV'] = xlp.loc[:, [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42]].sum(axis=1)
    data_result['SG'] = xlp.loc[:, [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43]].sum(axis=1)

    # se crea el archivo de uso profesional
    data_result.to_csv(directory+'/'+'Resultados_Completos_Uso_Cientifico.txt', sep='\t', index=False)
    # se codifican los nombres con un hash y se guardan por separado en pares
    data_keys = pn.DataFrame({'KEY': np.nan, 'NAME': data_result.loc[:, 'NAME']})
    data_result['NAME'] = data_result['NAME'].apply(hash)
    data_result['NAME'] = data_result['NAME'].apply(lambda b: str(base64.b64encode(str(b).encode()), "utf-8"))
    data_result = data_result.drop(['EMAIL'],axis=1)
    data_keys['KEY'] = data_result.loc[:, 'NAME']
    data_result.to_csv(directory+'/'+'Resultados_Completos_sin_nombres.txt', sep='\t', index=False)
    data_keys.to_csv(directory+'/'+'Llaves_con_nombres.txt', sep='\t', index=False)


    # print para todas las columnas
    with pn.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data_result)
        print(xlp)

    headers = list(['Activo', 'Sensorial', 'Visual', 'Secuencial'])
    headers2 = list(['Reflexivo', 'Intuitivo', 'Verbal', 'Global'])
    headers_val = range(0, 4)
    pdf = mpdf.PdfPages(directory+'/'+'Graficas_Resultados_sin_nombres.pdf')
    for index in range(0, data_result.shape[0]):
        fig, ax1 = ptl.subplots()
        ptl.yticks(range(-11, 12))
        ptl.ylim(-11, 11)
        ptl.title("Alumno: " + data_result.iloc[index, 0]
                  + "\n Escuela :" + data_result.iloc[index, 4] + " " + "Profesor: " + data_result.iloc[index, 3]
                  + "\n Edad :" + str(data_result.iloc[index, 2]) + " " + "Semestre: " + str(
            data_result.iloc[index, 5]))
        ax1.set_xlabel("Estilo de aprendizaje")
        ax1.set_ylabel("Nivel de Estilo de aprendizaje")
        ax1.tick_params(axis='x')
        ax1.set_xticks(headers_val)
        ax1.set_xticklabels(headers, fontdict=None, minor=False)
        ax2 = ax1.twiny()  # instantiate a second axes that shares the same x-axis
        # we already handled the x-label with ax1
        ax2.set_xticks(headers_val)
        ax2.set_xticklabels(headers2, fontdict=None, minor=False)
        ax2.tick_params(axis='x', top=True)
        fig.tight_layout()  # otherwise the right y-label is slightly
        results_val = list(data_result.iloc[index, 6:])
        # print(results_val)
        ptl.stem(headers_val, results_val, use_line_collection=True)
        pdf.savefig(fig)
    pdf.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Nombre del archivo a tratar")
    parser.add_argument("-o", "--fileO", help="Nombre del archivo de salida")
    args = parser.parse_args()
    if args.file and args.fileO:
        print("Archivo seleccionado: " + args.file)
        print("Archivo salida: " + args.fileO)
        read_excel(args.file, args.fileO)
    else:
        print("No se selecciono ningun archivo")


if __name__ == '__main__':
    main()
