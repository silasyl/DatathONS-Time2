from datetime import date, timedelta, datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import re
from scripts.wrapper import timer
from scripts.read import read_wind_data


def sarima_model(df, usina, data_prev=date.today().strftime('%Y-%m-%d')):
    """
    Aplica o modelo SARIMA (1,1,1)(1,1,1,48) no dataframe de entrada.
    Usa os 30 dias anteriores à data de previsão e faz previsão dos próximos 2 dias.

    Args:
        df (dataframe): dataframe contendo os dados de vento previstos e verificados para uma usina
        data_prev (string ou date, optional): data de previsão do modelo. O formato deve ser YYYY-MM-DD
            O modelo irá fazer a previsão para a data informada e o próximo dia.
            O valor padrão é a data atual, para previsão da data atual e próximo dia.
        usina (string): nome da usina, para salvar o arquivo de saída.
    Returns:
        dataframe: dataframe contendo os viés previstos
    """
    df.columns = ['verif', 'prev']
    df.loc[:, 'vies'] = df['verif'] - df['prev']
    df.loc[:, 'vies'].fillna(df['vies'].median(), inplace=True)

    if type(data_prev) == type(date.today()):
        data_prev = data_prev.strftime('%Y-%m-%d')

    data_init = (datetime.strptime(data_prev, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
    data_fim = (datetime.strptime(data_prev, '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d')
    train = df[(df.index >= data_init) & (df.index < data_prev)][['vies']]

    #print(train)

    model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,48))
    model = model.fit(disp=False)

    forecast = model.predict(start=data_prev, end=data_fim, dynamic=True)
    forecast.to_csv(f'vies_{usina}')
    return None


def apply_model(df, data_prev, usina=None):
    """
    Se o dataframe tiver 2 colunas, iremos aplicar o modelo sarima apenas aos dados do df (uma usina).
    Se o dataframe tiver mais de 2 colunas, iremos aplicar o modelo a todas as usinas.
    Args:
        df (dataframe): dataframe contendo os dados de vento previstos e verificados
        data_prev (string ou date): data de previsão do modelo. O formato deve ser YYYY-MM-DD
        usina (str, or None): string no formato UX, onde X é o número da usina.
            Aceita None para fazer a leitura de todos os dados no diretório.
    Returns:
        dataframe: dataframe contendo os viés previstos
    """
    if df.shape[1] == 2:
        print(f'Modelando a usina {usina} ...')
        sarima_model(df, usina, data_prev)
    else:
        for i in range(0, df.shape[1], 2):
            usina = re.search("(U[0-9]+)_", data.columns[0])[1]
            print(f'Modelando a usina {usina} ...')
            sarima_model(df.iloc[:, [i, i+1]], usina, data_prev)
    return None


@timer
def read_apply_model(dir_name, usina, data_prev):
    df = read_wind_data(dir_name=dir_name, usina=usina)
    apply_model(df, usina=usina, data_prev=data_prev)
    print('Terminou')
    return None