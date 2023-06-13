import os
from typing import Union
from getpass import getpass
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from app.utils.format_dataframe import group_data
from app.settings import URL, DOWNLOAD_FILEPATH

class AutoPayer:

    def __init__(self, nit: str, pending_payments_dataframe: Union[pd.DataFrame, None] = None) -> None:
        if pending_payments_dataframe is not None:
            self.grouped_dataframe = group_data(pending_payments_dataframe)
        self.nit = nit
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 600)

    def login(self) -> None:
        self.driver.get(URL)
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "iframe2")
            )
        )
        text_field = self.driver.find_element(By.ID, "viewns_Z7_2HHCHK02J0VD80QCBMOALT2007_:formEmpresas:numeroDocumento")
        text_field.send_keys(self.nit)
        login_button = self.driver.find_element(
            By.ID,
            "viewns_Z7_2HHCHK02J0VD80QCBMOALT2007_:formEmpresas:ns_Z7_2HHCHK02J0VD80QCBMOALT2007_j_id1930797831_7315a2c2"
        )
        login_button.click()
    
        user = self.wait.until(EC.visibility_of_element_located((By.ID, "CustLoginID")))
        user.send_keys(self.nit)

        token = self.driver.find_element(By.ID, "f_ssecurID")
        token.click()
        self.driver.minimize_window()
        token.send_keys(getpass("Ingrese el token:\n"))

        checkbox = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='custom-control custom-checkbox']")
        ))
        checkbox.click()

        password = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "f_password")
        ))
        password.send_keys(getpass("Introduzca la contraseña:\n"))
        self.driver.maximize_window()

        button = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="form"]/div/div/div/form/div[1]/div[4]/button[2]')
        ))
        button.click()
    
    def close_ad(self) -> None:
        close_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="splash-97385-close-button"]')
        ))
        close_button.click()
    
    def open_transaction(self) -> None:
        transaction_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mainMenu"]/ul[3]/li/h3/span[1]')
        ))
        transaction_button.click()

        payment_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mainMenu"]/ul[3]/li/div/ul[1]/li[1]/ul/li[1]/a')
        ))
        payment_button.click()

    def open_new_transaction(self) -> None:
        new_transaction_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="tabs-ajax"]/ul/li[2]/a')
        ))
        new_transaction_button.click()

    def set_prepare_new_transaction(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divProductType"]/div[1]/div/div/button')
        ))
        button.click()

        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ulcmbproductType"]/li[text()="Cuenta Corriente"]')
        ))
        object_list.click()

        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divProductType"]/div[2]/div/div/button')
        ))
        button.click()

        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ulcmbaccountID"]/li[text() = "CC2093"]')
        ))
        object_list.click()
    
    def insert_new_transaction_values(self, row: pd.Series) -> None:
        # tipo_documento
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divPayRollIDType"]/div/div/div/button')
        ))
        button.click()

        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="ulcmbidentificationType"]/li[text() = "{row["tipo_documento"]}"]')
        ))
        object_list.click()
        row["tipo_documento"]

        # no_documento
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="nroID"]')
        ))
        input.send_keys(str(row["no_documento"]))

        # nombre
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="beneficiary"]')
        ))
        input.send_keys(row["nombre"])

        # valor
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="payVal"]')
        ))
        input.send_keys(str(row["valor"]))

        # banco
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divAcctTo"]/div[1]/div/div/button')
        ))
        button.click()
        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="ulcmbentityDestiny"]/li[text() = "{row["banco"]}"]')
        ))
        object_list.click()

        # tipo_cuenta
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divAcctTo"]/div[2]/div/div/button')
        ))
        button.click()
        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="ulcmbproductTypeDestiny"]/li[text() = "{row["tipo_cuenta"]}"]')
        ))
        object_list.click()

        # no_cuenta
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="cmbaccountDestiny"]')
        ))
        input.send_keys(str(row["no_cuenta"]))

        # tipo_pago nomina proveedores
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="payRollCreateTxFrom"]/fieldset/div[2]/div[6]/div/div/button')
        ))
        button.click()
        tipo_pago = row["tipo_pago"]
        if tipo_pago != "NOMINA":
            tipo_pago = "PROVEEDORES"
        object_list = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="ulcmbpaymentType"]/li[text() = "{tipo_pago}"]')
        ))
        object_list.click()

        # id
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="pmtRefId"]')
        ))
        input.send_keys(str(row["id"]).replace("-", "to").replace("_", " "))

        # informacion adicional
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="infoAdditional"]')
        ))
        input.send_keys(row["tipo_pago"])

    def confirm_payment(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="btnNext"]')
        ))
        button.click()

        time.sleep(5)

        self.driver.minimize_window()
        input = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="ssecurID"]')
        ))
        input.send_keys(getpass("Ingrese el token:\n"))

        self.driver.maximize_window()
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="btnAcept"]')
        ))
        button.click()

    def save_transaction(self, row: pd.Series) -> None:
        download = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="btnExp"]/a[3]')
        ))
        download.click()
        time.sleep(2)
        filename = sorted([file for file in os.listdir(DOWNLOAD_FILEPATH) if "nominaproveedores" in file.lower()])[-1]
        os.rename(DOWNLOAD_FILEPATH + filename, DOWNLOAD_FILEPATH + str(row["id"]) + ".pdf")

    def update_transaction(self, index) -> None:
        self.grouped_dataframe.loc[index, "datetime"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    def end_transaction(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="btnEnd"]')
        ))
        button.click()

    def main(self) -> pd.DataFrame:
        self.login()
        self.close_ad()
        self.open_transaction()
        for index, row in self.grouped_dataframe.iterrows():
            self.open_new_transaction()
            self.set_prepare_new_transaction()
            self.insert_new_transaction_values(row)
            self.confirm_payment()
            self.save_transaction(row)
            self.update_transaction(index)
            self.end_transaction()
            time.sleep(2)
        return self.grouped_dataframe
