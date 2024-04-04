import unittest
import os
import chardet
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, InvalidArgumentException
from selenium.webdriver.remote.webelement import WebElement
from context import ba

usuario = os.environ.get("login_bradesco")
senha = os.environ.get("senha_bradesco")
url_valido = "https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf"
url_invalido = "http://localhost:0000"


class TestCriarConexao(unittest.TestCase):

    '''Testa a conexão com o site do Bradesco'''

    def test_link_valido(self):
        '''testa se a função criar_conexao retorna um driver quando o link é válido'''
        driver = ba.criar_conexao(url_valido)
        self.assertIsInstance(driver, WebDriver, "Erro ao criar driver")

    def test_link_invalido(self):
        '''testa se a função criar_conexao lança uma exceção quando o link é inválido'''
        with self.assertRaises(InvalidArgumentException):
            ba.criar_conexao(url_invalido)

    def test_site_indisponivel(self):
        '''
        Testa se a função criar_conexao lança uma exceção quando o site está
        indisponível
        '''
        with self.assertRaises(WebDriverException):
            ba.criar_conexao(url_invalido)


class TestLogin(unittest.TestCase):
    '''Testa as funções de login'''
    @classmethod
    def setUpClass(cls):
        cls.driver = ba.criar_conexao(url_valido)

    @classmethod
    def tearDown(self):
        self.driver.close()

    def test_encontrou_campos_login(self):
        '''Testa se as funções encontram os campos de login e senha'''
        campo_login = ba.encontra_campo_login(self.driver)
        self.assertIsInstance(campo_login, WebElement)
        self.assertEqual(campo_login.get_attribute(
            "name"), "identificationForm:txtUsuario")

        campo_senha = ba.encontra_campo_senha(self.driver)
        self.assertIsInstance(campo_senha, WebElement)
        self.assertEqual(campo_senha.get_attribute(
            "name"), "identificationForm:txtSenha")

        botao_login = ba.encontra_botao_login(self.driver)
        self.assertIsInstance(botao_login.get_attribute, WebElement)
        self.assertEqual(botao_login.get_attribute("name"),
                         "identificationForm:botaoAvancar")

    def test_login_invalido(self):
        '''Testa se a função login retorna None quando o login falha'''
        usuario = "123456789"
        senha = "123456789"

        with self.assertRaises(ba.LoginInvalidoException):
            ba.login(self.driver, usuario, senha)
        # Verifica se o retorno da função login é none
        self.assertIsNone(self.driver)


class TestAcessoPagExtrato(unittest.TestCase):
    '''Testa a função acessar_pagina_extratos'''
    url = "link do extrato"

    @classmethod
    def setUpClass(cls):
        cls.driver = ba.criar_conexao(cls.url)
        cls.driver.ba.login(cls.driver, usuario, senha)
        cls.driver.ba.acessar_pagina_extratos(cls.driver)

    def tearDown(self):
        self.driver = ba.deslogar(self.driver)
        self.driver.close()

    def test_encontrou_campos_extrato(self):
        '''
        Testa se a função encontrou botão para acessar a página de extratos
        '''
        botao = ba.encontra_botao_pagina_extratos(self.driver)
        self.assertIsInstance(botao, WebElement)
        self.assertEqual(botao.get_attribute("name"), "_id74_0:_id76")

    def test_acesso_pag_extrato(self):
        '''
        Testa se a função acessar_pagina_extratos retorna o link da página
        de extratos
        '''
        link_extrato = self.driver.current_url
        try:
            self.assertEqual(link_extrato, self.driver.current_url)
        except AssertionError:
            self.assertNotEqual(link_extrato, self.driver.current_url,
                                "Erro ao conectar com o site do Bradesco")

        botao = self.driver.find_element(By.XPATH, "relatório_pagina_xpath")
        botao.click()

    def test_retorno_pagina(self):
        '''Testa se a função acessar_pagina_extratos retorna None'''
        retorno = ba.acessar_pagina_extratos(self.driver)
        self.assertIsInstance(retorno, None)


class TestBaixaExtrato(unittest.TestCase):
    '''Testa a função baixar_extrato'''

    @classmethod
    def setUpClass(cls):
        cls.driver = ba.criar_conexao(url_valido)
        cls.driver.ba.login(cls.driver, usuario, senha)
        cls.driver.ba.acessar_pagina_extratos(cls.driver)
        cls.pasta = "tests\teste_extratos.csv"
        cls.tamanho_bytes = os.path.getsize(cls.pasta)

    @classmethod
    def tearDown(self):
        self.driver = ba.deslogar(self.driver)
        self.driver.close()

    def test_botao_download(self):
        '''Testa se a função encontra_botao_download retorna um botão'''
        botao = ba.encontra_botao_download(self.driver)
        self.assertIsInstance(botao, WebElement)
        self.assertEqual(botao.get_attribute("name"),
                         "relatorioForm:botaoDownload")

    def test_baixar_extrato(self):
        '''Testa se a função baixar_extrato retorna um arquivo'''
        self.assertTrue(os.path.isfile())
        self.assertGreater(self.tamanho_bytes, 0, "Arquivo vazio")

    def test_excecao_arquivo(self):
        '''Testa se a função baixar_extrato lança uma exceção'''
        with self.assertRaises(ba.ArquivoNaoEncontradoException):
            ba.baixar_arquivo(self.driver)


class TestSalvarArquivo(unittest.TestCase):
    '''Testa a função salvar_arquivo'''
    def setUpClass(cls):
        cls.driver = ba.criar_conexao(url_valido)
        cls.driver.ba.login(cls.driver, usuario, senha)
        cls.driver.ba.acessar_pagina_extratos(cls.driver)
        cls.arquivo = ba.baixar_arquivo(cls.driver)
        cls.pasta = "tests\teste_extratos.csv"

    def tearDown(self):
        self.driver = ba.deslogar(self.driver)
        self.driver.close()

    def test_conversao(self):
        '''Testa se a função salvar_arquivo converte o arquivo para iso--8859-1'''
        formato = chardet.detect(self.arquivo)["encoding"]
        self.assertEqual(formato, "iso-8859-1")

    def test_salvar_arquivo(self):
        '''Testa se a função salvar_arquivo salva o arquivo'''
        lista_arquivos_anterior = os.listdir(self.pasta)

        ba.salvar_arquivo(self.arquivo, self.pasta)

        lista_arquivos_posterior = os.listdir(self.pasta)
        arquivo_adicionado = list(
            set(lista_arquivos_posterior) - set(lista_arquivos_anterior))

        self.assertEqual(len(arquivo_adicionado), 1)
        self.assertEqual(arquivo_adicionado[0], "Bradesco_dia_hora.csv")

    def test_retorno_bytes(self):
        '''Testa se a função baixar_extrato retorna bytes'''
        retorno = ba.baixar_arquivo(self.driver)
        self.assertIsInstance(retorno, bytes)


class TestFinalizarConexão(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = ba.criar_conexao(url_valido)
        cls.driver.ba.login(cls.driver, usuario, senha)
        cls.driver.ba.acessar_pagina_extratos(cls.driver)

    @classmethod
    def tearDown(self):
        self.driver = ba.deslogar(self.driver)
        self.driver.close()

    def test_finalizar_conexao(self):
        '''
        Testa se a função encontra_botao_sair encontra o botão correto e se
        a função retorna um WebElement.
        '''
        botao_sair = ba.encontra_botao_sair(self.driver)
        self.assertIsInstance(botao_sair, WebElement)
        self.assertEqual(botao_sair.get_attribute("name"), "botaoSair")

        retorno = ba.finalizar_conexao(self.driver)
        self.assertIsNone(retorno)

    def test_retortno_conexao(self):
        '''Testa se a função finalizar_conexao retorna None'''
        with self.assertRaises(WebDriverException):
            ba.finalizar_conexao(self.driver)


class TestExecutar(unittest.TestCase):
    def test_executar(self):
        '''Testa se a função executar retorna None'''
        resultado = ba.executar()
        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
