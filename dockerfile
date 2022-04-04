FROM python:3

WORKDIR /app
COPY /scripts /app/scripts 
VOLUME /app/resultados

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN cd /app/scripts

ENTRYPOINT scrapy runspider scripts/cep_spider.py -a states=$states
