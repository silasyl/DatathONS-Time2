import os
import re
import pandas as pd
from datetime import timedelta


# Função leitura dos dados
def read_wind_data(dir_name='Datathons_pem_vento', usina=None):
    """
    Função que faz leitura de todos os arquivos de dados de ventos e retorna um dataframe contendo todos os dados.
    Presume-se que os dados de vento são em intervalos de meia hora.
    A pasta precisa ter apenas arquivos de vento, formato txt.
    Os arquivos precisam ter nome UX_Ven_Prev.txt e UX_Ven_Verif.txt, onde X é o número da usina,
    conforme os dados repassados para nós.

    Args:
        dir_name (str, optional): string com o nome do diretório onde os dados estão
        usina (str, or None): string no formato UX, onde X é o número da usina.
            Aceita None para fazer a leitura de todos os dados no diretório.

    Returns:
        df: pandas dataframe contendo as informações dos arquivos lidos.
            Cada coluna é o nome do arquivo lido e os index das linha são timestamps, ordenados.
    """
    path = os.path.join(os.getcwd(), dir_name)
    df = pd.DataFrame()
    for root, dirs, files in os.walk(path):
        for file in files:
            if usina:
                if re.search(usina + '_Ven_Prev.txt', file) or re.search(usina + '_Ven_Verif.txt', file):
                    file_path = os.path.join(root, file)
                    df_temp = pd.read_csv(file_path, header=None, sep=';')
                    df_temp[0] = pd.to_datetime(df_temp[0], format='%Y%m%d')
                    df_temp.set_index(0, drop=True, inplace=True)
                    init_date = df_temp.index[0]
                    last_date = df_temp.index[-1] + timedelta(days=1) - timedelta(minutes=30)
                    df_temp = df_temp.stack(dropna=False)
                    df_temp.index = pd.date_range(init_date, last_date, freq='30T')
                    df = pd.concat([df, pd.DataFrame(df_temp, columns=[file])], axis=1)
            else:
                file_path = os.path.join(root, file)
                df_temp = pd.read_csv(file_path, header=None, sep=';')
                df_temp[0] = pd.to_datetime(df_temp[0], format='%Y%m%d')
                df_temp.set_index(0, drop=True, inplace=True)
                init_date = df_temp.index[0]
                last_date = df_temp.index[-1] + timedelta(days=1) - timedelta(minutes=30)
                df_temp = df_temp.stack(dropna=False)
                df_temp.index = pd.date_range(init_date, last_date, freq='30T')
                df = pd.concat([df, pd.DataFrame(df_temp, columns=[file])], axis=1)
    df = df.reindex(sorted(df.columns), axis=1)
    return df