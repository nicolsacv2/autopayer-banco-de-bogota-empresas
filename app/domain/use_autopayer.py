import gspread
import pandas as pd

from app.settings import SHEET_ID, SHEET_NAME, GCP_CREDENTIALS_PATH
from app.utils.autopayer import AutoPayer

GSPREAD_CLIENT = gspread.service_account(GCP_CREDENTIALS_PATH)
SHEET = GSPREAD_CLIENT.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
SHEET_DATAFRAME = pd.DataFrame(SHEET.get_all_records(numericise_ignore=[8]))

print("----> Pagos pendientes:\n", SHEET_DATAFRAME)

if __name__ == "__main__":
    NIT = input("Ingrese el NIT:\n")
    autopayer = AutoPayer(NIT, pending_payments_dataframe=SHEET_DATAFRAME)
    dataframe = autopayer.main()
    print("----> Pagos realizados:\n", dataframe.sort_values('id'))
