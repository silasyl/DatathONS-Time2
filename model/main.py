from scripts.model import read_apply_model


if __name__ == '__main__':
    # dir_name é o nome do diretório onde os dados de vento se encontram
    # usina é a string da usina a ser analisada. Pode ser None para todas as usinas no diretório

    usina = 'U1'
    read_apply_model(dir_name='Datathons_pem_vento',
                     usina=usina,
                     data_prev='2020-12-01')