# requisitos
- docker
- python

# Passo a passo

## construindo container docker
    ```docker build -t search_cep . ```

## rodando container com argumentos de busca 

### caso deseja pesquisa uma lista especifica de estados, definir utilizando a variavel states
    ```docker run -e states="GO, DF, MA, SP" -v $(pwd)/resultados:/app/resultados search_cep``` 

### para puxar todos os estados, nao definir nada
    ```docker run -v $(pwd)/resultados:/app/resultados search_cep``` 

# diretorio

- resultados/log.txt: log gerado pelo scrapy
- resultados/DATA_cep.json: dados raspado pelo crawler

- scripts/var.py: arquivo python contendo as variaveis utilizados
- scripts/general.py: arquivo python contendo as funcoes secundarias
- scripts/cep_spider.py: arquivo python com o crawler de raspagem dos CEPs

- dockerfile: arquivo docker com a imagem do projeto
- output_file.png: imagem contendo um sample da saida do crawler
- requirements.txt: arquivo txt com as bibliotecas necessarias

# sample saida

- data: lista de dicionarios com informacoes de "id", "estado", "localidade", "faixa de cep"
- extract_at: horario da extrracao dos dados 
- len_results: quantidados de registros salvados

![](/output_file.png) 
