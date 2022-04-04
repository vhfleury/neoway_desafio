import scrapy
import var
import general

class search(scrapy.Spider):

    name = "cep"

    custom_settings = var.custom_settings

    def __init__(self, states:list = None):

        self.id = 0
        self.results = list()
        self.states = general.get_states(states)

    def start_requests(self):

        self.logger.info(f"states: {self.states}")

        for uf in self.states:
            
            start_value = var.start_value
            
            data = general.created_payload(uf, start_value)

            yield scrapy.FormRequest(url=var.url, callback=self.parse, method="POST", formdata=data, headers=var.headers, meta={"start":start_value, "uf": uf})

    def parse(self, response):

        is_init = general.is_init(response.meta["start"])
        
        table = general.get_table(response)
        
        organize_table = general.organize_table(table, is_init)
        
        self.logger.info(f"total rows: {len(organize_table)}")
        
        for city, cep in organize_table.items():
            
            self.id +=1    

            self.results.append({"id":self.id,
                   "estado": response.meta['uf'],
                   "localidade": city,
                   "faixa de cep":cep
                })
        
        if len(table) > (4*var.qtdrow)-5:
            
            start = response.meta["start"] + var.qtdrow
            uf = response.meta["uf"]
            data = general.created_payload(uf, start)
            
            yield scrapy.FormRequest(url=var.url, callback=self.parse, method="POST", formdata=data, headers=var.headers, meta={"start":start, "uf":uf})

    def closed(self, reason):
        
        self.logger.info(f"total rows: {len(self.results)}")
        
        general.format_result(self.results)
        
        
