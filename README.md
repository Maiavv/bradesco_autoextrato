# Bradesco-Extrato-Bancario-Automatico

Este projeto em Python utiliza o Selenium e o Airflow para automatizar o processo de baixar o extrato bancário do Bradesco a cada 20 minutos. Ele economiza tempo e esforço ao evitar a necessidade de fazer login manualmente e baixar o extrato repetidamente. Pode ser usado para monitorar finanças de forma eficiente e manter um controle regular das transações bancárias.

## Estrutura do Projeto
O projeto está organizado da seguinte maneira:

```
Bradesco-Extrato-Bancario-Automatico/
│
├── logs/
│   └── bradesco_autoextrato.log
│
├── bradesco_autoextrato/
│   ├── dags/
|   |   └── bradesco_autoextrato_dag.py
│   ├── __init__.py
│   ├── bradesco_autoextrato.py
│   ├── bradesco_exceptions.py
│   ├── secrets.py
│   └── utils.py
│
├── tests/
│   ├── __init__.py
│   ├── context.py
│   ├── test_bradesco_autoextrato.py
│   └── test_utils.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

### logs/
Esta pasta contém o arquivo de log do script, que registra todas as atividades durante a execução do programa.

### bradesco_autoextrato/
Esta pasta contém o código fonte do projeto. O arquivo `bradesco_autoextrato.py` é o script principal que executa o Selenium e baixa o extrato bancário. O arquivo `utils.py` contém funções auxiliares para lidar com as operações de arquivo e log. O arquivo `secrets.py` contém configurações das variáveis de ambiente. O arquivo `bradesco_exceptions.py` contém classes de exceção específicas do módulo `bradesco_autoestrato.py`

### tests/
Esta pasta contém os arquivos de testes unitários do projeto. Os arquivos `test_bradesco_autoextrato.py` e `test_utils.py` contêm testes para as funções e métodos do script e do arquivo `utils.py`, respectivamente.

### .gitignore
Este arquivo contém uma lista de arquivos e pastas que serão ignorados pelo Git durante o controle de versão.

### README.md
Este arquivo. Contém as informações sobre o projeto e como utilizá-lo.

### requirements.txt
Este arquivo contém a lista de dependências do projeto, que devem ser instaladas antes da execução do script.

### setup.py
Este arquivo contém as informações de configuração do pacote Python, incluindo a versão, autor e dependências.

## Como Usar

### 1. Clonando o repositório
Para utilizar o Bradesco-Auto-Extrato, você precisará clonar o repositório para o seu computador:
```shell
git clone https://github.com/LSBlrti/Bradesco-Extrato-Bancario-Automatico.git
```

### 2. Instalando as dependências
As dependências do projeto podem ser instaladas utilizando o pip, executando o seguinte comando na pasta raiz do projeto:
```shell
pip install -r requirements.txt
```

### 3. Configurando as informações de login
As informações de login do Bradesco e outras configurações necessárias devem ser configuradas como variáveis de ambiente em um servidor ou em uma ferramenta de gerenciamento de segredos. Para isso, é necessário criar as seguintes variáveis de ambiente:

- `BRADESCO_USER`: Nome de usuário da conta bancária do Bradesco.
- `BRADESCO_PASS`: Senha da conta bancária do Bradesco.
- `BRADESCO_AGENCY`: Número da agência bancária do Bradesco.
- `BRADESCO_ACCOUNT`: Número da conta bancária do Bradesco.
- `DOWNLOAD_PATH`: Caminho absoluto onde os extratos serão salvos.
Observação: As variáveis de ambiente podem ser definidas de diferentes maneiras, dependendo do sistema operacional ou ferramenta de gerenciamento de segredos que você está usando. Consulte a documentação correspondente para saber como definir as variáveis de ambiente.

### 4. Executando o script
O script principal do projeto é o `bradesco_autoextrato.py`. Ele pode ser executado diretamente no terminal, digitando o seguinte comando:
```shell
python bradesco_autoextrato/bradesco_autoextrato.py
```
Ou você pode executá-lo usando o Airflow. Para isso, basta importar o DAG `bradesco_autoextrato_dag.py` localizado na pasta `dags/` do projeto no seu ambiente Airflow. Certifique-se de que as dependências do projeto estejam instaladas no ambiente Airflow antes de executá-lo.

### 5. Monitorando a execução do script
O script salvará os extratos no caminho especificado na variável de ambiente `DOWNLOAD_PATH`. Além disso, ele também registrará todas as atividades em um arquivo de log, localizado em `logs/bradesco_autoextrato.log`.

Você pode monitorar a execução do script verificando o arquivo de log ou verificando o status de execução do DAG no Airflow. Se o DAG não estiver sendo executado corretamente, verifique as configurações de ambiente e certifique-se de que as dependências do projeto estejam instaladas corretamente.
