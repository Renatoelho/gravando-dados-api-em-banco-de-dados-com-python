#!/home/ubuntu/python/api-enderecos-python/.venv/bin/python3

import requests
import pandas as pd 
from sqlalchemy import create_engine


# Acessando API para obter informações de endereço para os CEPs listados abaixo.

lista_ceps = ['01153000', '20050000','70714020']
lista_enderecos = []

for cep in lista_ceps:

    url = 'https://viacep.com.br/ws/{}/json/'.format(cep)

    try:
        req = requests.get(url, timeout=3)

        if req.status_code == 200:

            # API acessada com sucesso!
            endereco = req.json()
            lista_enderecos.append([endereco['cep'], 
                                    endereco['logradouro'], 
                                    endereco['bairro'], 
                                    endereco['localidade'], 
                                    endereco['uf']])

        else:
            print('Ocorreu o seguinte erro no acesso da API: {}'.format(req.raise_for_status()))

    except Exception as erro: 
        print('Ocorreu o seguinte erro na execução do código: {}'.format(erro))

# Transformando a lista de endereços em um DataFrame

df_enderecos = pd.DataFrame(lista_enderecos, columns=['cep','logradouro','bairro','localidade','uf'])

# Preparando a conexão e gravando em uma tabela no banco de dados.

db_connection = 'mysql+pymysql://user:password@host:port/database'

db_connection = create_engine(db_connection)

df_enderecos.to_sql(con=db_connection, name='enderecos', if_exists='append', index=False)
