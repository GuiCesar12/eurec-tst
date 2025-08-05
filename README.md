# Diário Oficial API

## Descrição
Este projeto é uma API REST desenvolvida em Python utilizando FastAPI, que permite o upload de arquivos comprimidos (.zip) e extrai os arquivos XML contendo os metadados de publicações do Diário Oficial da União. Os dados extraídos são disponibilizados através de uma API e publicados em um tópico via AMQP.

## Estrutura do Projeto
```
diario-oficial-api
├── src
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── api
│   │   └── routes.py          # Definição das rotas da API
│   ├── services
│   │   ├── zip_extractor.py    # Serviço para extração de arquivos ZIP
│   │   ├── xml_parser.py       # Serviço para parsing de arquivos XML
│   │   └── amqp_publisher.py   # Serviço para publicação de dados via AMQP
│   ├── models
│   │   └── publication.py      # Modelo de dados para publicações
│   ├── database
│   │   └── db.py              # Gerenciamento da conexão com o banco de dados
│   ├── utils
│   │   └── logger.py          # Utilitários de logging
│   └── tests
│       ├── test_zip_extractor.py # Testes unitários para o serviço de extração
│       ├── test_xml_parser.py    # Testes unitários para o serviço de parsing
│       └── test_api.py           # Testes unitários para a API
├── requirements.txt            # Dependências do projeto
├── Dockerfile                  # Instruções para construir a imagem Docker
├── docker-compose.yml          # Configuração dos serviços Docker
├── .gitignore                  # Arquivos e diretórios a serem ignorados pelo Git
├── .github
│   └── workflows
│       └── ci.yml              # Pipeline de CI para testes e análise estática
└── README.md                   # Documentação do projeto
```

## Instruções para Execução

### Pré-requisitos
- Docker
- Docker Compose

### Executando a Aplicação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd diario-oficial-api
   ```

2. Construa e inicie os serviços:
   ```
   docker-compose up --build
   ```

3. Acesse a API:
   A API estará disponível em `http://localhost:8000`.

### Testes
Para executar os testes, utilize o seguinte comando:
```
docker-compose exec app pytest
```

## Contribuição
Sinta-se à vontade para contribuir com melhorias ou correções. Faça um fork do repositório e envie um pull request com suas alterações.

## Licença
Este projeto está licenciado sob a MIT License - consulte o arquivo LICENSE para mais detalhes.