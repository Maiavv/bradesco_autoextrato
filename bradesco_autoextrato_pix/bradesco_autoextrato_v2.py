# %%
from datetime import datetime as dt
from datetime import date
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

# %%

def criar_conexao(link: str) -> webdriver:
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(r'C:\Users\vitor\Pictures\Camera Roll\chromedriver.exe')
    driver.get(link)
    return driver

def login(driver, username, passwd) -> webdriver:
    campo_login = driver.find_element(By.ID, "identificationForm:txtUsuario")
    campo_senha = driver.find_element(By.ID, "identificationForm:txtSenha")
    botao_login = driver.find_element(By.ID, "identificationForm:botaoAvancar")

    campo_login.send_keys(username)
    campo_senha.send_keys(passwd)
    botao_login.click()

    time.sleep(10)

    return driver

# %%
columns_rename = {
    'Nome' : 'Lançamento',
    'CPF/CNPJ' : 'CDC',
    'TX.ID' : 'drop',
    'DOCTO': 'Dcto.',
    'Crédito' : 'Crédito (R$)',
    'Débito' : 'Débito (R$)',
    'Identificação' : 'drop2',
    'TIPO DE TRANSAÇÃO' : 'drop3',
}



def acessa_baixa_pix(driver: webdriver):
    data_fim = pd.to_datetime(date.today())
    data_inicio = data_fim - 2 * pd.offsets.Day()

    skip_anuncio = ActionChains(driver)
    skip_anuncio.move_by_offset(100, 100).click().perform()

    botao_pix = driver.find_element(By.ID, '_id74_2:_id76')
    botao_pix.click()

    link_pag_inicial = driver.current_url
    driver.get('https://www.ne12.bradesconetempresa.b.br/ibpjtelainicial/menuPix.jsf?')
    element = driver.find_element(By.XPATH, "//a[@title='Relatório Pix']")
    element.click()

    time.sleep(10)

    text_box_conta = driver.find_element(By.NAME, 'contaDebito__sexyCombo')
    text_box_conta.clear()
    text_box_conta.send_keys('3645 | 0005959-5 | conta-corrente')

    time.sleep(5)

    tira_lista = ActionChains(driver)
    tira_lista.move_by_offset(100, 100).click().perform()

    time.sleep(2)

    botao_data = driver.find_element(By.XPATH, '//label[@for="relatorioExtratoArquivoForm:tipoConsultaRadioPeriodo"]')
    botao_data.click()

    time.sleep(10)

    dia_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataInicioDia')
    dia_inicial.send_keys(data_inicio.day)
    mes_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataInicioMes')
    mes_inicial.send_keys(data_inicio.month)
    ano_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataInicioAno')
    ano_inicial.send_keys(data_inicio.year)

    dia_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataFimDia')
    dia_inicial.send_keys(data_fim.day)
    mes_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataFimMes')
    mes_inicial.send_keys(data_fim.month)
    ano_inicial = driver.find_element(By.NAME, 'relatorioExtratoArquivoForm:dataFimAno')
    ano_inicial.send_keys(data_fim.year)

    time.sleep(5)

    botao_relatorio = driver.find_element(By.ID, 'relatorioExtratoArquivoForm:btnGerarRelatorio')
    botao_relatorio.click()

    driver.get(link_pag_inicial)

    time.sleep(5)

    skip_anuncio = ActionChains(driver)
    skip_anuncio.move_by_offset(100, 100).click().perform()
    botao_sair = driver.find_element(By.ID, 'botaoSair')
    botao_sair.click()
    driver.quit()

def processa_extrato():
    pasta = r'C:\Users\vitor\Downloads'
    arquivos = os.listdir(pasta)
    arquivos_pix = [arquivo for arquivo in arquivos if 'PIX' in arquivo]
    arquivos_pix = sorted(arquivos_pix, key=lambda x: os.path.getmtime(os.path.join(pasta, x)), reverse=True)
    arquivo_mais_recente_pix = arquivos_pix[0]
    caminho_extrato = os.path.join(pasta, arquivo_mais_recente_pix)

    df = pd.read_excel(caminho_extrato)
    index = df['Relatório PIX'].isin(['Data']).idxmax()
    df.columns = df.iloc[index]
    df = df[index + 1:]

    df = df.rename(columns=columns_rename)
    df['Lançamento'] = df['Lançamento'] + ' - ' + df['CDC']
    df = df.drop(columns=['drop', 'drop2', 'drop3', 'CDC'])

    diretorio_saida = r"\\storm\bradesco"
    arquivo_saida = f"Bradesco_{dt.now().strftime('%d%m%Y_%H%M%S')}.xls"
    caminho_completo = diretorio_saida + "\\" + arquivo_saida

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Sheet1')

    sheet.write_merge(6, 6, 0, 5, 'Extrato de: Agência: 3645  Conta: 5959-5')

    for i, col in enumerate(df.columns):
        sheet.write(8, i, col)
        for j, value in enumerate(df[col]):
            sheet.write(j+9, i, value)

    workbook.save(caminho_completo)


# %%
link = "https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf"
username = os.environ.get("login_bradesco")
passwd = os.environ.get("senha_bradesco")


def executar(username, passwd, link):
    conexao = criar_conexao(link)
    login(conexao, username, passwd)
    if 'Sessão encerrada' in conexao.page_source:
        conexao = criar_conexao(link)
        login(conexao, username, passwd)
    else:
        pass
    time.sleep(5)
    acessa_baixa_pix(conexao)
    time.sleep(5)
    processa_extrato()

#%%
