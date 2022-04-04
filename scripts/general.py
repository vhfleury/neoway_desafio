import var
import json
import hashlib

def created_payload(states: str, ini: int) -> dict:
    """Returns the payload necessary for the request on the post office website. 

    Parameters:
        states (str): state search.
        ini (int): initial page search number.
    Returns:
        dict: Returns the payload necessary for the request on the post office website.

    """
    form_data = {"UF": states,
                 'Localidade': '',
                 "Bairro": "",
                 "qtdrow": str(var.qtdrow),
                 "pagini": str(ini),
                 "pagfim": str(ini + var.qtdrow)
                 }

    return form_data


def get_table(response) -> list:
    """pull the city table from the post office website

    Parameters:
        response (): html page response.
    Returns:
        list: returns the table with the location and zip code range.
    """

    return response.xpath("//table[contains(@class, 'tmp')]//tr//td//text()")


def is_init(start: int or str) -> bool:
    """Informs if the result is referring to the beginning of the search for a state.

    Parameters:
        start (int or str): Initial page value.
    Returns:
        Bool: Returning true if the position is equal to 1.
    """

    return int(start) == 1


def organize_table(table: list, init: bool) -> dict:
    """Organize a list with information from a table.

    Parameters:
        table (list): A table in the form of a list, results of an xpath.
        init (bool): Informs if the result is referring to the beginning of the search for a state.

    Returns:
        new_table (dict): Returning a dictionary where the key is the city and the value is the zip code.
    """

    new_table = dict()

    # pulling all texts inside xpath results list
    list_result_table = [n.get() for n in table]

    if init:
        new_table.update({list_result_table[0]: list_result_table[1]})

        # the first two indexes of a search are search state information
        start = 2

    else:
        start = 0

    # each row of the courier table contains 4 columns
    new_table.update({list_result_table[n]: list_result_table[n+1] for n in range(start,
                     len(list_result_table), var.tabale_rows_results) if (list_result_table[n+3] == "Total do município")})

    return new_table


def get_states(states: str or None) -> list:
    """Method that defines the number of states that should be part of the search,
    if no state is passed, all states will be entered in the search.

    Parameters:
        states (str or None): Abbreviations of Brazilian states.

    Returns:
        states (list): Returning list with abbreviations of Brazilian states.
    """

    if states is None or states == '':
        states = var.states_brazil
    else:
        states = states.split(",")

    return states


def output_jsonl(results: list) -> dict:
    """format and save result to standard jsonl output

    Parameters:
        results (list): list with scrapy results.

    Returns:
        None 
    """
    
    ids_export = set()

    with open(var.name_file, 'w') as outfile:
        for city in results:

            id = city["id"]
            
            if id not in ids_export:
                json.dump(city, outfile)
                outfile.write('\n')



def result_to_dict(organize_table:dict, state:str) -> list:
    """format results in dict and create id

    Parameters:
        organize_table (dict): with key is the city and value is range zip code

    Returns:
        results (list): lista de dicionario com as informacoes coletadas 
    """
    results = list()

    for city, cep in organize_table.items():
        
        values_search_str = "".join([state, city, cep])
        id = hashlib.md5(values_search_str.encode('utf-8')).hexdigest()

        results.append({"id":id,
                "estado": state,
                "localidade": city,
                "faixa de cep":cep
            })

    return results


def next_page(len_table:int):
    """metodo verifica se tem uma proxima pagina para puxar mais dados 

    Parameters:
        len_table (int): with key is the city and value is range zip code

    Returns:
        bool : retorna True se existe uma proxima pagina
    """
    return len_table > (var.tabale_rows_results*var.qtdrow) - (var.tabale_rows_results+1)