# %%
from datetime import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup
import xlwt
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

path_chrome = Path(__file__).parent / "chromedriver.exe"
path_chrome = Path(R"C:\Program Files\Google\Chrome\Application\chrome.exe")


def criar_conexao(link: str) -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        # options=chrome_options,
    )
    driver.get(link)

    return driver


def login(driver, username, passwd) -> webdriver:

    time.sleep(10)

    campo_login = driver.find_element(By.ID, "identificationForm:txtUsuario")
    campo_senha = driver.find_element(By.ID, "identificationForm:txtSenha")
    botao_login = driver.find_element(By.ID, "identificationForm:botaoAvancar")

    campo_login.send_keys(username)
    campo_senha.send_keys(passwd)
    botao_login.click()

    time.sleep(10)

    return driver


def extrai_bradesco(driver: webdriver):
    skip_anuncio = ActionChains(driver)
    skip_anuncio.move_by_offset(100, 100).click().perform()

    driver.get(
        "https://www.ne12.bradesconetempresa.b.br/ibpjsaldosextratos/extratoUltimosLancamentosCC.jsf?"
    )

    time.sleep(15)

    menu_select = Select(
        driver.find_element(By.NAME, "formFiltroUltimosLancamentos:filtro:_id58")
    )

    time.sleep(10)

    menu_select.select_by_index("3")

    time.sleep(15)

    html = driver.page_source

    time.sleep(10)

    driver.back()
    skip_anuncio.move_by_offset(100, 100).click().perform()

    time.sleep(10)

    driver.find_element(By.ID, "botaoSair").click()

    time.sleep(10)

    driver.quit()

    return html


# %%


def limpa_extrato(html: str):
    soup = BeautifulSoup(html, "html.parser")
    table_5959 = soup.find(
        "table", {"class": "tabelaSaldos mt10 tabBranco tabelaListagemImpressao"}
    )

    rows = table_5959.find_all("tr")

    header = [cell.text.strip() for cell in rows[0].find_all("th")]

    data = []
    for row in rows[1:]:
        values = [cell.text.strip() for cell in row.find_all("td")]
        data.append(dict(zip(header, values)))

    df = pd.DataFrame(data)

    df.drop(columns=["", ""], inplace=True)

    df = df.drop(index=df.index[-1])

    dict_substituicoes = {
        "RECEBIMENTO FORNECEDOR": "RECEBIMENTO FORNECEDOR ",
        "CREDITO AUTOMATICO*": "CREDITO AUTOMATICO*",
        "CHEQUE C/C-BDN": "CHEQUE C/C-BDN ",
        "TRANSFER BDN": "TRANSFER BDN ",
        "DISPONREMET": "DISPON REMET",
        "INTERNETTED": "INTERNET TED",
        "HBANK*DEST": "HBANK* DEST",
        "PARA CC PJ": "PARA CC PJ ",
        "ENTRE AGS": "ENTRE AGS ",
        "CP AUTOAT": "CP AUTOAT ",
        "PIXREM": "PIX REM",
        "PIXDES": "PIX DES",
    }

    df["Lançamento"] = df["Lançamento"].replace(dict_substituicoes, regex=True)

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce").ffill()
    df["Data"] = df["Data"].dt.strftime("%d/%m/%Y")

    return df


def salvar_extrato(df: pd.DataFrame):
    diretorio_saida = r"\\128.90.1.2\arquivos\bradesco"
    arquivo_saida = f"Bradesco_{dt.now().strftime('%d%m%Y_%H%M%S')}.xls"
    caminho_completo = diretorio_saida + "\\" + arquivo_saida

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet1")

    sheet.write_merge(6, 6, 0, 5, "Extrato de: Agência: 3645  Conta: 5959-5")

    for i, col in enumerate(df.columns):
        sheet.write(8, i, col)
        for j, value in enumerate(df[col]):
            sheet.write(j + 9, i, value)

    workbook.save(caminho_completo)


# %%
link = "https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf"
username = os.environ.get("login_bradesco")
passwd = os.environ.get("senha_bradesco")


def executar(username, passwd, link):
    conexao = criar_conexao(link)
    login(conexao, username, passwd)
    if "Sessão encerrada" in conexao.page_source:
        conexao = criar_conexao(link)
        login(conexao, username, passwd)
    else:
        pass
    time.sleep(5)
    html = extrai_bradesco(conexao)
    df = limpa_extrato(html)
    salvar_extrato(df)


if __name__ == "__main__":
    executar(username, passwd, link)
