import time

path = "resultados"

name_file = f"{path}/{time.strftime('%Y%m%d_%H%M%S')}_cep.jsonl"

custom_settings = {
    "LOG_FILE": f'{path}/log.txt',
    "DEBUG_LEVEL": "INFO",
    "DOWNLOAD_DELAY": 3
}

states_brazil = ["AC", 'AL', 'AP',
                 'AM', 'BA', 'CE',
                 'DF', 'ES', 'GO',
                 'MA', 'MT', 'MS',
                 'MG', 'PA', 'PB',
                 'PR', 'PE', 'PI',
                 'RJ', 'RN', 'RS',
                 'RO', 'RR', 'SC',
                 'SP', 'SE', 'TO'
                 ]

url = 'https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

# number of results in each search on the site
qtdrow = 100

# initial value of the states search page
start_value = 1

# quantidade de colunas que existe na tabela do resultado da busca
tabale_rows_results = 4
