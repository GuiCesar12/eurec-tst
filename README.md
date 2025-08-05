# API - Documentação Completa

## 🔧 Variáveis de Ambiente

A aplicação utiliza as seguintes variáveis de ambiente para configuração:

### Configurações do Banco de Dados

| Variável         | Descrição                           | Exemplo                    | Obrigatório |
|------------------|-------------------------------------|----------------------------|-------------|
| POSTGRES_HOST    | Endereço do servidor PostgreSQL      | db (Docker) ou rds.amazonaws.com | Sim        |
| POSTGRES_USER    | Usuário para autenticação           | user                       | Sim         |
| POSTGRES_PASSWORD| Senha para autenticação             | password                   | Sim         |
| POSTGRES_DB      | Nome do banco de dados              | publications               | Sim         |
| POSTGRES_PORT    | Porta de conexão (opcional)         | 5432                       | Não         |

### Configurações do RabbitMQ

| Variável            | Descrição                          | Exemplo                        | Obrigatório |
|---------------------|------------------------------------|--------------------------------|-------------|
| AMQP_URL            | URL completa de conexão            | amqp://guest:guest@rabbitmq    | Sim         |
| AMQP_EXCHANGE_NAME  | Nome do exchange para publicações  | diario_oficial                 | Sim         |
| AMQP_ROUTING_KEY    | Chave de roteamento padrão         | publications.new               | Sim         |
| AMQP_QUEUE          | Nome da fila (opcional)            | publications_queue             | Não         |

### Configurações da Aplicação

| Variável    | Descrição                       | Exemplo | Obrigatório |
|-------------|---------------------------------|---------|-------------|
| API_PORT    | Porta onde a API rodará         | 8000    | Não         |
| DEBUG       | Modo debug (True/False)         | False   | Não         |
| LOG_LEVEL   | Nível de log (DEBUG, INFO, WARNING, ERROR) | INFO | Não |

---

## 📦 Variáveis de Ambiente para CI/CD com AWS ECR

No pipeline de deploy para AWS ECR e ECS, são necessários os seguintes secrets/configurações no GitHub:

| Variável               | Descrição                     | Exemplo        |
|------------------------|------------------------------|----------------|
| AWS_ACCESS_KEY_ID      | Chave de acesso AWS          | ...            |
| AWS_SECRET_ACCESS_KEY  | Chave secreta AWS            | ...            |
| AWS_REGION             | Região AWS                   | us-east-1      |
| ECR_REPOSITORY         | Nome do repositório ECR      | eurec-tst      |
| ECS_CLUSTER            | Nome do cluster ECS          | cluster-name   |
| ECS_SERVICE            | Nome do serviço ECS          | eurec-service  |

Arquivos necessários:
- `.github/workflows/deploy.yml`: Define as etapas do pipeline
- `.aws/task-definition.json`: Configuração do container no ECS

---

## 📊 Endpoints da API

### 1. Upload de Arquivos

- **Método:** `POST /upload`
- **Descrição:** Processa arquivos ZIP contendo XMLs do Diário Oficial.
- **Content-Type:** multipart/form-data
- **Parâmetro:** `file` (arquivo ZIP)
- **Respostas:**
  - 201: Arquivo processado com sucesso
  - 400: Erro no formato do arquivo
  - 500: Erro interno no processamento

### 2. Listagem de Publicações

- **Método:** `GET /publications`
- **Parâmetros:**
  - `skip`: Número de registros para pular (padrão: 0)
  - `limit`: Número máximo de registros (padrão: 100, máximo: 1000)
  - `start_date`: Filtro por data inicial (formato YYYY-MM-DD)
  - `end_date`: Filtro por data final (formato YYYY-MM-DD)
  - `art_type`: Filtro por tipo de artigo
  - `search`: Busca textual nos campos
- **Exemplo:**
  ```bash
  curl "http://localhost:8000/publications?limit=10&start_date=2023-01-01"
  ```

### 3. Detalhes da Publicação

- **Método:** `GET /publications/{id}`
- **Exemplo:**
  ```bash
  curl "http://localhost:8000/publications/12345"
  ```

### 4. Contagem de Publicações

- **Método:** `GET /publications/count`
- **Parâmetro opcional:** `art_type` (filtrar por tipo)
- **Exemplo:**
  ```bash
  curl "http://localhost:8000/publications/count?art_type=Lei"
  ```

### 5. Monitoramento e Health Check

- **Métricas:** Endpoint `/metrics` (se configurado)
- **Health Check:** Endpoint `/health` retorna status da aplicação

---

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- Python 3.12+
- PostgreSQL
- RabbitMQ

### Configuração do Ambiente

1. Clone o repositório:
    ```bash
    git clone https://github.com/GuiCesar12/eurec-tst.git
    cd eurec-tst
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements-dev.txt
    ```

4. Configure as variáveis de ambiente:
    ```bash
    cp .env.example .env
    # Edite o arquivo .env com suas configurações
    ```

5. Execute os testes:
    ```bash
    pytest tests/ -v
    ```

6. Inicie a aplicação:
    ```bash
    uvicorn src.main:app --reload
    ```

---

## ☁️ Pipeline CI/CD com GitHub Actions e AWS

### Fluxo do Pipeline

- **Trigger:** Acionado por push na branch `main` ou por pull requests.
- **Testes:**
  - Instalação de dependências
  - Execução de testes unitários e de integração
- **Build e Deploy (apenas se os testes passarem):**
  - Construção da imagem Docker
  - Push para o Amazon ECR
  - Deploy automático no ECS

### Estrutura do Pipeline (Exemplo)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # ... (etapas de teste)
  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment: production
    steps:
      # ... (etapas de build e deploy)
```

---

## 📦 Implantação com Docker

1. **Construa a imagem localmente:**
    ```bash
    docker build -t eurec-tst .
    ```

2. **Execute com Docker Compose:**
    ```bash
    docker-compose up -d
    ```

3. **Acesse a API:**
    ```
    http://localhost:8000/docs
    ```

---

## 🔎 Monitoramento

- **Logs da Aplicação:** Visualize com `docker-compose logs -f app`
- **Métricas:** Endpoint `/metrics` (se configurado)
- **Health Check:** Endpoint `/health`

---

## 🗂️ Testes

Os testes automatizados cobrem upload de arquivos, listagem, busca por ID e tratamento de erros:

- Testes de unidade para upload ZIP, extração, API REST e integração com RabbitMQ e banco de dados.
- Para rodar:
    ```bash
    pytest tests/ -v
    ```

---

## 📁 Estrutura de Diretórios

- `src/` - Código fonte principal
- `.github/workflows/` - Workflows de CI/CD (GitHub Actions)
- `.aws/` - Configurações AWS, como Task Definition para ECS

---

## ℹ️ Observações

- O arquivo `.env_example` serve de referência para configuração local.
- Ajuste variáveis de ambiente sensíveis via secrets do GitHub para produção.
- O sistema implementa boas práticas de segurança (usuário não-root em Docker, healthcheck, logs).

---