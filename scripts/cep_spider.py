from unittest import result
import scrapy
import var
import general


class search(scrapy.Spider):

    name = "cep"

    custom_settings = var.custom_settings

    def __init__(self, states: list = None):

        self.id = 0
        self.results = list()
        self.states = general.get_states(states)

    def start_requests(self):

        self.logger.info(f"states: {self.states}")

        for state in self.states:

            start_value = var.start_value

            data = general.created_payload(state, start_value)

            yield scrapy.FormRequest(url=var.url, callback=self.parse, method="POST", formdata=data, headers=var.headers, meta={"start": start_value, "state": state})

    def parse(self, response):

        is_init = general.is_init(response.meta["start"])
        table = general.get_table(response)
        organize_table = general.organize_table(table, is_init)

        state = response.meta["state"]

        self.logger.info(f"total rows: {len(organize_table)}")

        self.results += general.result_to_dict(organize_table, state)

        if general.next_page(len(table)):

            start = response.meta["start"] + var.qtdrow

            data = general.created_payload(state, start)

            yield scrapy.FormRequest(url=var.url, callback=self.parse, method="POST", formdata=data, headers=var.headers, meta={"start": start, "state": state})

    def closed(self, reason):

        self.logger.info(f"total rows: {len(self.results)}")

        general.output_jsonl(self.results)
