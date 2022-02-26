# Gravando os dados de uma API em um banco de dados com Python

Em outro repositório meu aqui no *GitHub* eu ensinei como acessar uma API de endereços com o *Python*, agora vou ensinar como gravar esses dados obtidos via API em um banco de dados utilizando o *Python*. Para entender melhor o contexto desta aplicação proposta aqui, sugiro acessar o repositório onde ensino como acessar uma API com auxílio do *Python*: [Consumindo uma API de endereços com Python](https://github.com/Renatoelho/consumindo-api-enderecos-python).

Com o código que utilizamos para acessar a API e pegar todas as informações de endereço, obtivemos uma lista com informações que vamos carregar em uma tabela no banco de dados *MySQL*. As bibliotecas que utilizaremos para essa atividade vão ser o **pandas** com objetivo de fazer uma pequena organização da lista, e com **sqlalchemy** que é uma biblioteca de [*ORM*](https://pt.wikipedia.org/wiki/Mapeamento_objeto-relacional) que facilita a integração do Python com os mais variados bancos de dados existentes.

Como parte do código já está pronto, vamos focar em dois passos fundamentais que são: utilizar o *pandas* para transformar a lista em um *DataFrame* e como  carregar esse *DataFrame* no banco de dados.

## 1º Passo - Transformar a lista de endereços em um DataFrame e atribuir um nome para cada atributo dessa lista.

```Python
# Transformando a lista de endereços em um DataFrame

df_enderecos = pd.DataFrame(lista_enderecos, columns=['cep','logradouro','bairro','localidade','uf'])
```

## 2º Passo - Pegar esse DataFrame e gravar em uma tabela no banco de dados.

```Python
# Preparando a conexão e gravando em uma tabela no banco de dados.

db_connection = 'mysql+pymysql://user:password@host:port/database'
db_connection = create_engine(db_connection)
df_enderecos.to_sql(con=db_connection, name='enderecos', if_exists='append', index=False)
```

## Os dados gravados no banco de dados ficam da seguinte forma:

![Imagem dos dados da API Gravados no Banco](https://drive.google.com/uc?export=view&id=1FtKaaoCYp8ADx9PdhcaeaCKgoCxVsIUw)

## Código completo da aplicação

```Python
#!/usr/bin/python3

import requests
import pandas as pd
from sqlalchemy import create_engine


lista_ceps: list = ['01153000', '20050000', '70714020']
lista_enderecos: list = []

for cep in lista_ceps:
    url: str = 'https://viacep.com.br/ws/{}/json/'.format(cep)

    try:
        req = requests.get(url, timeout=3)
        if req.status_code == 200:
            # API acessada com sucesso!
            endereco = req.json()
            lista_enderecos.append(
                            [
                                endereco['cep'],
                                endereco['logradouro'],
                                endereco['complemento'],
                                endereco['bairro'],
                                endereco['localidade'],
                                endereco['uf']
                            ]
                )

        else:
            erro = req.raise_for_status()
            print(f'Ocorreu o seguinte erro no acesso da API: {erro}')

    except Exception as erro:
        print(f'Ocorreu o seguinte erro na execução do código: {erro}')

for item in lista_enderecos:
    print(item)

# Transformando a lista de endereços em um DataFrame

df_enderecos = pd.DataFrame(
                lista_enderecos,
                columns=[
                            'cep',
                            'logradouro',
                            'bairro',
                            'localidade',
                            'uf'
                        ]
    )

# Preparando a conexão e gravando em uma tabela no banco de dados.

db_connection = 'mysql+pymysql://user:password@host:port/database'
db_connection = create_engine(db_connection)
df_enderecos.to_sql(
                    con=db_connection,
                    name='enderecos',
                    if_exists='append',
                    index=False
    )

```

Para instalar as bibliotecas necessárias no Python utilize o arquivo *requeriments.txt* e execute o seguinte comando: 

```bash
pip install -r requeriments.txt
```

### Requisitos mínimos:

>> Sistema operacional Linux (Ubuntu 20.04.2 LTS)  <br/>Memória RAM de 4GB ou mais  <br/>Python 3 instalado

<b>Até breve!</b>

> **Referências:**  <br/><font size="1">Pandas.pydata.org, **pandas Docs**. Disponível em: < https://pandas.pydata.org/pandas-docs/dev/user_guide/ >. Acesso em: 07 jan. 2022.  <br/>Pandas.pydata.org, **pandas.DataFrame.to_sql**. Disponível em: < https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html >. Acesso em: 05 jan. 2022.  <br/>Requests, **HTTP for Humans**. Disponível em: <https://docs.python-requests.org/en/latest/>. Acesso em: 1 fev. 2022.  <br/>Via CEP, **Consulte CEPs de todo o Brasil**. Disponível em: <https://viacep.com.br/>. Acesso em: 1 fev. 2022.  <br/></font>
