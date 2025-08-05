🔧 Variáveis de Ambiente
Variável	Descrição	Exemplo
POSTGRES_HOST	Host do banco de dados PostgreSQL	db (local) ou RDS endpoint
POSTGRES_USER	Usuário do PostgreSQL	user
POSTGRES_PASSWORD	Senha do PostgreSQL	password
POSTGRES_DB	Nome do banco de dados	publications
AMQP_URL	URL de conexão com RabbitMQ	amqp://guest:guest@rabbitmq
AMQP_EXCHANGE_NAME	Nome do exchange no RabbitMQ	diario_oficial
AMQP_ROUTING_KEY	Routing key para publicação	publications.new
📊 Endpoints

    POST /upload - Processa arquivo ZIP com XMLs

    GET /publications - Lista publicações (com paginação)

    GET /publications/{id} - Obtém uma publicação específica

    GET /publications/count - Contagem total de publicações

🛠️ Desenvolvimento

Para desenvolvimento local:
bash

# Instale as dependências
pip install -r requirements-dev.txt

# Execute os testes
pytest tests/
📄 Licença

MIT License - Veja o arquivo LICENSE para detalhes.
