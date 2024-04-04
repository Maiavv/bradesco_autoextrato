# Descrição dos testes
Com TDD (Desenvolvimento Orientado a Testes), devemos primeiro escrever os testes para cada função e, em seguida, implementar a função para que ela passe nesses testes. Dessa forma, teríamos os seguintes testes para cada função:

## Testes para criar_conexao(link: str) -> WebDriver:
    1. Teste para verificar se a conexão é criada com sucesso quando o link é válido.
    2. Teste para verificar se uma exceção é lançada quando o link é inválido.
    3. Teste para verificar se uma exceção é lançada quando o site está indisponível.
    4. Teste para verificar se o retorno é uma instância de WebDriver.

## Testes para login(driver: WebDriver, username: str, passwd: str) -> None:
    1. Teste para verificar se o programa encontrou corretamente os campos de login e senha.
    2. Teste para verificar se uma exceção é lançada quando o nome de usuário ou senha é inválido.
    3. Teste para verificar se o retorno é None.


## Testes para acessar_pagina_extratos(driver: WebDriver) -> None:
    1. Teste para verificar se a página de extratos é acessada com sucesso.
    2. Teste para verificar se o botão para acessar a página de extratos é encontrado corretamente.
    3. Teste para verificar se uma exceção é lançada quando não é possível acessar a página.
    4. Teste para verificar se o retorno é None.

## Testes para baixar_extrato(driver: WebDriver) -> bytes:
    1. Teste para verificar se o arquivo de extrato é baixado com sucesso.
    2. Teste para verificar se uma exceção é lançada quando não é possível baixar o arquivo.
    3. Teste para verificar se o retorno é uma instância de bytes.

## Testes para finalizar_conexao(driver: WebDriver) -> None:
    1. Teste para verificar se o botão sair foi encontrado.
    2. Teste para verificar se a conexão é fechada com sucesso.
    3. Teste para verificar se uma exceção é lançada quando não é possível fechar a conexão.
    4. Teste para verificar se o retorno é None.

## Testes para executar() -> None:
    1. Teste para verificar se a função é executada com sucesso quando todas as etapas são bem-sucedidas.
    2. Teste para verificar se uma exceção é lançada quando ocorre um erro durante a execução.
    3. Teste para verificar se o retorno é None.