# Módulo em virtual env para o modelo SARIMA

O modelo implementado é o SARIMA(1,1,1)(1,1,1,48).
É preciso ter um diretório, contendo os arquivos de ventos das usinas em txt.
O nome padrão do diretório é Datathons_pem_vento, mas pode ser modificado no código.
É possível modificar no código main.py a Usina a se aplicar o modelo, ou deixar None para todas as usinas no diretório.
Também é possível modificar a variável data_prev para previsão de data explícita, ou deixar None para prever dia atual e 1 dia a frente.

Instalar requirements:
pip install -r requirements.txt 

Rodar o modelo:
python main.py
