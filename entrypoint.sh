#!/bin/sh

# Espera o PostgreSQL ficar disponível
echo "⌛ Aguardando PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ PostgreSQL pronto!"

# Cria/atualiza tabelas
echo "⚙️ Criando tabelas..."
python -c "
from src.database.db import engine
from src.database.base import Base
Base.metadata.create_all(bind=engine)
" || exit 1

# Inicia a aplicação
echo "🚀 Iniciando aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --app-dir src