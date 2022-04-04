import var
import json

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
    rows = [n.get() for n in table]

    if init:
        new_table.update({rows[0]: rows[1]})

        # the first two indexes of a search are search state information
        start = 2

    else:
        start = 0

    # each row of the courier table contains 4 columns
    new_table.update({rows[n]: rows[n+1] for n in range(start,
                     len(rows), 4) if (rows[n+3] == "Total do município")})

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


def format_result(results: list) -> dict:
    """format and save result to standard jsonl output

    Parameters:
        results (list): list with scrapy results.

    Returns:
        None 
    """
    
    with open(var.name_file, 'w') as outfile:
        for citys in results:
            json.dump(citys, outfile)
            outfile.write('\n')

