#!/bin/bash
# Script de instalação automática do PostgreSQL com pgvector usando Docker
# Para o Curso CrewAI - Sistema de Triagem Médica

set -e

# Configurações padrão
CONTAINER_NAME="postgres-pgvector-crewai"
DB_NAME="curso"
DB_USER="postgres"
DB_PASSWORD="password"
DB_PORT="5432"
PGVECTOR_VERSION="pg17"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${PURPLE}🚀 INSTALAÇÃO PGVECTOR + POSTGRESQL (DOCKER)${NC}"
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${BLUE}📋 Container: ${CONTAINER_NAME}${NC}"
    echo -e "${BLUE}🗄️  Database: ${DB_NAME}${NC}"
    echo -e "${BLUE}👤 User: ${DB_USER}${NC}"
    echo -e "${BLUE}🔌 Port: ${DB_PORT}${NC}"
    echo -e "${PURPLE}===============================================${NC}"
}

check_docker() {
    echo -e "${BLUE}🔍 Verificando Docker...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não encontrado!${NC}"
        echo -e "${YELLOW}💡 Instale o Docker primeiro: https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker não está rodando!${NC}"
        echo -e "${YELLOW}💡 Inicie o Docker e tente novamente.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker disponível${NC}"
}

stop_existing_container() {
    echo -e "${BLUE}🛑 Verificando container existente...${NC}"
    if docker ps -a | grep -q "$CONTAINER_NAME"; then
        echo -e "${YELLOW}⚠️ Container $CONTAINER_NAME já existe${NC}"
        echo -e "${BLUE}🔄 Removendo container anterior...${NC}"
        docker stop "$CONTAINER_NAME" &> /dev/null || true
        docker rm "$CONTAINER_NAME" &> /dev/null || true
        echo -e "${GREEN}✅ Container anterior removido${NC}"
    fi
}

create_postgres_container() {
    echo -e "${BLUE}🐳 Criando container PostgreSQL com pgvector...${NC}"
    
    docker run -d \
        --name "$CONTAINER_NAME" \
        -e POSTGRES_DB="$DB_NAME" \
        -e POSTGRES_USER="$DB_USER" \
        -e POSTGRES_PASSWORD="$DB_PASSWORD" \
        -p "$DB_PORT:5432" \
        -v pgvector_data:/var/lib/postgresql/data \
        "pgvector/pgvector:${PGVECTOR_VERSION}"
    
    echo -e "${GREEN}✅ Container criado: $CONTAINER_NAME${NC}"
}

wait_for_postgres() {
    echo -e "${BLUE}⏳ Aguardando PostgreSQL inicializar...${NC}"
    
    for i in {1..30}; do
        if docker exec "$CONTAINER_NAME" pg_isready -U "$DB_USER" &> /dev/null; then
            echo -e "${GREEN}✅ PostgreSQL pronto!${NC}"
            return 0
        fi
        echo -e "${YELLOW}⌛ Tentativa $i/30...${NC}"
        sleep 2
    done
    
    echo -e "${RED}❌ Timeout: PostgreSQL não inicializou${NC}"
    return 1
}

setup_pgvector() {
    echo -e "${BLUE}🔧 Configurando extensão pgvector...${NC}"
    
    # Habilitar extensão pgvector
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS vector;"
    
    # Verificar versão instalada
    VERSION=$(docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';")
    echo -e "${GREEN}✅ pgvector $VERSION instalado${NC}"
}

create_test_data() {
    echo -e "${BLUE}🧪 Criando dados de teste...${NC}"
    
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" << 'EOF'
-- Criar tabela de teste
DROP TABLE IF EXISTS teste_pgvector_instalacao;
CREATE TABLE teste_pgvector_instalacao (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    descricao TEXT,
    embedding VECTOR(1536)  -- Dimensões do OpenAI
);

-- Inserir dados de teste com embeddings simulados
INSERT INTO teste_pgvector_instalacao (nome, descricao, embedding) VALUES 
    ('Sintoma A', 'Dor de cabeça leve', 
     ('[' || string_agg(random()::text, ',') || ']')::vector(1536)
    ),
    ('Sintoma B', 'Febre alta', 
     ('[' || string_agg(random()::text, ',') || ']')::vector(1536)
    ),
    ('Sintoma C', 'Dor no peito', 
     ('[' || string_agg(random()::text, ',') || ']')::vector(1536)
    )
FROM generate_series(1, 1536);

-- Criar índice HNSW para performance
CREATE INDEX idx_teste_pgvector_hnsw 
ON teste_pgvector_instalacao 
USING hnsw (embedding vector_l2_ops);

-- Mostrar dados criados
SELECT id, nome, descricao FROM teste_pgvector_instalacao;
EOF

    echo -e "${GREEN}✅ Dados de teste criados${NC}"
}

test_pgvector_functionality() {
    echo -e "${BLUE}🧪 Testando funcionalidades do pgvector...${NC}"
    
    # Testar busca por similaridade
    echo -e "${YELLOW}🔍 Teste de busca por similaridade:${NC}"
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" << 'EOF'
-- Criar vetor de consulta aleatório
WITH vetor_consulta AS (
    SELECT ('[' || string_agg(random()::text, ',') || ']')::vector(1536) as query_vec
    FROM generate_series(1, 1536)
)
SELECT 
    nome, 
    descricao,
    embedding <-> query_vec AS distancia_l2
FROM teste_pgvector_instalacao, vetor_consulta
ORDER BY embedding <-> query_vec
LIMIT 3;
EOF

    echo -e "${GREEN}✅ Teste de similaridade concluído${NC}"
}

create_env_file() {
    echo -e "${BLUE}📄 Criando arquivo .env...${NC}"
    
    ENV_FILE="../.env"
    
    # Backup do .env existente
    if [ -f "$ENV_FILE" ]; then
        cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}📁 Backup do .env criado${NC}"
    fi
    
    # Criar/atualizar .env
    cat > "$ENV_FILE" << EOF
# Configuração PostgreSQL com pgvector - Curso CrewAI
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
POSTGRES_HOST=localhost
POSTGRES_PORT=${DB_PORT}
POSTGRES_DB=${DB_NAME}
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}

# OpenAI API (configure com sua chave)
OPENAI_API_KEY=sua_chave_openai_aqui
EOF

    echo -e "${GREEN}✅ Arquivo .env criado: $ENV_FILE${NC}"
}

show_connection_info() {
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${GREEN}🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!${NC}"
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${BLUE}📊 Informações de Conexão:${NC}"
    echo -e "${YELLOW}  Host: localhost${NC}"
    echo -e "${YELLOW}  Port: ${DB_PORT}${NC}"
    echo -e "${YELLOW}  Database: ${DB_NAME}${NC}"
    echo -e "${YELLOW}  User: ${DB_USER}${NC}"
    echo -e "${YELLOW}  Password: ${DB_PASSWORD}${NC}"
    echo ""
    echo -e "${BLUE}🔗 String de Conexão:${NC}"
    echo -e "${YELLOW}  postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}${NC}"
    echo ""
    echo -e "${BLUE}🛠️ Comandos Úteis:${NC}"
    echo -e "${YELLOW}  # Acessar PostgreSQL${NC}"
    echo -e "  docker exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME"
    echo ""
    echo -e "${YELLOW}  # Ver logs do container${NC}"
    echo -e "  docker logs $CONTAINER_NAME"
    echo ""
    echo -e "${YELLOW}  # Parar container${NC}"
    echo -e "  docker stop $CONTAINER_NAME"
    echo ""
    echo -e "${YELLOW}  # Iniciar container${NC}"
    echo -e "  docker start $CONTAINER_NAME"
    echo ""
    echo -e "${BLUE}🧪 Próximos Passos:${NC}"
    echo -e "${GREEN}  1. Configure sua OPENAI_API_KEY no arquivo .env${NC}"
    echo -e "${GREEN}  2. Teste a configuração: uv run scripts/configurar_pgvector.py${NC}"
    echo -e "${GREEN}  3. Execute os exemplos da aula7${NC}"
    echo -e "${PURPLE}===============================================${NC}"
}

# Função principal
main() {
    print_header
    
    # Verificações preliminares
    check_docker
    
    # Parar container existente se houver
    stop_existing_container
    
    # Criar novo container
    create_postgres_container
    
    # Aguardar PostgreSQL inicializar
    if ! wait_for_postgres; then
        echo -e "${RED}❌ Falha na inicialização do PostgreSQL${NC}"
        exit 1
    fi
    
    # Configurar pgvector
    setup_pgvector
    
    # Criar dados de teste
    create_test_data
    
    # Testar funcionalidades
    test_pgvector_functionality
    
    # Criar arquivo .env
    create_env_file
    
    # Mostrar informações finais
    show_connection_info
    
    echo -e "${GREEN}🚀 Pronto para usar o pgvector no Curso CrewAI!${NC}"
}

# Executar script
main "$@"