"""Group data"""

import pandas as pd

def format_ids(serie: pd.Series) -> str:
    """Format ids to a string.
    
    :param pd.Series: Pandas serie with ids.
    :return: String with ids.
    :rtype: str.
    """
    object_list = sorted(serie.tolist())
    id = object_list[0]
    result = str(id)
    for i in range(1, len(object_list)):
        new_id = object_list[i]
        if new_id == id + 1:
            if result[-1] != "-":
                result += "-"
        else:
            if result[-len(str(id)):] != str(id):
                result += f"{id}_{new_id}"
            else:
                result += f"_{new_id}"
        id = new_id
    if result[-1] == "-":
        result += str(object_list[-1])
    return result

def group_data(pending_payments_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Group data by document type and document number.
    
    :param pd.DataFrame: Pandas dataframe with pending payments.
    :return: Pandas dataframe with grouped data.
    :rtype: pd.DataFrame.
    """

    grouped_dataframe = pending_payments_dataframe.groupby(
        ["tipo_documento", "no_documento"]
    ).agg(
        {
            "id": format_ids,
            "nombre": "first",
            "valor": "sum",
            "banco": "first",
            "tipo_cuenta": "first",
            "no_cuenta": "first",
            "tipo_pago": lambda serie: " ".join(list(serie.unique())).upper()
        }
    ).reset_index()
    grouped_dataframe = grouped_dataframe.sort_values(by="valor", ascending=False).reset_index(drop=True)

    return grouped_dataframe
