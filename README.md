# Bradesco-Extrato-Bancario-Automatico

Este projeto em Python utiliza o Selenium para automatizar o processo de baixar o extrato bancário do Bradesco a cada 20 minutos. Ele economiza tempo e esforço ao evitar a necessidade de fazer login manualmente e baixar o extrato repetidamente. Pode ser usado para monitorar finanças de forma eficiente e manter um controle regular das transações bancárias.

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
