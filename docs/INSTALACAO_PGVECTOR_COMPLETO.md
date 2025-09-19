# 📦 Guia de Instalação do pgvector - Curso CrewAI

## 🎯 Visão Geral

O **pgvector** é uma extensão open-source do PostgreSQL que adiciona suporte nativo para **busca de similaridade de vetores**. Esta extensão é essencial para o Curso CrewAI, pois permite:

- ✅ Armazenamento eficiente de embeddings OpenAI
- ✅ Busca semântica ultrarrápida em sintomas e queixas médicas  
- ✅ Consultas por similaridade usando L2, coseno, produto interno
- ✅ Índices otimizados (HNSW e IVFFlat)
- ✅ Suporte completo a ACID, JOINs e recursos PostgreSQL

## ⚡ Compatibilidade

### Versões Suportadas

- **PostgreSQL**: 13, 14, 15, 16, 17+
- **pgvector**: v0.8.1+ (recomendado v0.8.1)
- **Sistemas**: Linux, macOS, Windows
- **Dimensões suportadas**: até 2.000 (vector), 4.000 (halfvec), 64.000 (bit)

### Para o Curso CrewAI

- **Embedding OpenAI**: 1.536 dimensões (suportado ✅)
- **Modelo usado**: `text-embedding-3-small`
- **Índices recomendados**: HNSW para performance otimizada

## 🚀 Instalação por Sistema Operacional

### 📱 **Método 1: Ubuntu/Debian (Recomendado)**

#### Instalação via APT (Mais Fácil)

```bash
# Atualizar repositórios
sudo apt update

# Instalar pgvector (PostgreSQL 15)
sudo apt install postgresql-15-pgvector

# Para PostgreSQL 16
sudo apt install postgresql-16-pgvector

# Para PostgreSQL 17
sudo apt install postgresql-17-pgvector
```

#### Instalação Manual (Compilação)

```bash
# Instalar dependências
sudo apt update
sudo apt install -y \
    postgresql-server-dev-15 \
    postgresql-15 \
    build-essential \
    git \
    cmake

# Baixar e compilar pgvector
cd /tmp
git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
cd pgvector

# Compilar e instalar
make
sudo make install

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### 🍎 **Método 2: macOS**

#### Usando Homebrew (Recomendado)

```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar pgvector
brew install pgvector

# Se já tiver PostgreSQL instalado
brew services restart postgresql
```

#### Usando MacPorts

```bash
sudo port install pgvector
```

#### Compilação Manual no macOS

```bash
# Instalar Xcode Command Line Tools
xcode-select --install

# Instalar PostgreSQL via Homebrew
brew install postgresql

# Baixar e compilar pgvector
cd /tmp
git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
cd pgvector

# Compilar (ajustar caminho do PostgreSQL se necessário)
make PG_CONFIG=/opt/homebrew/bin/pg_config
make install PG_CONFIG=/opt/homebrew/bin/pg_config

# Reiniciar PostgreSQL
brew services restart postgresql
```

### 🪟 **Método 3: Windows**

#### Pré-requisitos

```cmd
# Instalar Visual Studio Build Tools
# Download: https://visualstudio.microsoft.com/pt-br/downloads/

# Instalar PostgreSQL para Windows
# Download: https://www.postgresql.org/download/windows/

# Instalar Git para Windows
# Download: https://git-scm.com/download/win
```

#### Compilação no Windows

```cmd
# Abrir "x64 Native Tools Command Prompt for VS 2022" como Administrador

# Definir caminho do PostgreSQL (ajustar versão)
set "PGROOT=C:\Program Files\PostgreSQL\17"

# Baixar pgvector
cd %TEMP%
git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
cd pgvector

# Compilar
nmake /F Makefile.win

# Instalar
nmake /F Makefile.win install

# Reiniciar serviço PostgreSQL
net stop postgresql-x64-17
net start postgresql-x64-17
```

### 🐳 **Método 4: Docker (Mais Simples)**

#### Docker Compose (Recomendado para Desenvolvimento)

Criar arquivo `docker-compose.yml`:

```yaml
version: '3.8'
services:
  postgres-pgvector:
    image: pgvector/pgvector:pg17
    container_name: postgres_crewai
    environment:
      POSTGRES_DB: curso
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d/
    restart: unless-stopped

volumes:
  postgres_data:
```

```bash
# Subir o container
docker-compose up -d

# Verificar se está rodando
docker-compose ps

# Conectar ao banco
docker-compose exec postgres-pgvector psql -U postgres -d curso
```

#### Docker Run Simples

```bash
# Executar container com pgvector
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_DB=curso \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg17

# Conectar ao banco
docker exec -it postgres-pgvector psql -U postgres -d curso
```

### ☁️ **Método 5: Serviços Hospedados (Produção)**

#### Providers com pgvector Pré-instalado

```bash
# Supabase (Recomendado - Gratuito até 500MB)
# https://supabase.com/

# Neon (PostgreSQL Serverless)
# https://neon.tech/

# Railway
# https://railway.app/

# Render
# https://render.com/

# Azure Database for PostgreSQL
# Microsoft Azure

# Amazon RDS com pgvector
# AWS (requer configuração manual)

# Google Cloud SQL
# Google Cloud (requer configuração manual)
```

## ⚙️ Configuração e Habilitação

### 1. **Habilitar Extensão pgvector**

```sql
-- Conectar ao banco de dados
psql -U postgres -d curso

-- Habilitar extensão (executar uma vez por banco)
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar se foi instalada
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Ver versão instalada
SELECT extversion FROM pg_extension WHERE extname = 'vector';
```

### 2. **Testar Instalação Básica**

```sql
-- Criar tabela de teste
CREATE TABLE teste_pgvector (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    embedding VECTOR(3)
);

-- Inserir dados de teste
INSERT INTO teste_pgvector (nome, embedding) VALUES 
    ('Teste A', '[1,2,3]'),
    ('Teste B', '[4,5,6]'),
    ('Teste C', '[7,8,9]');

-- Testar busca por similaridade L2
SELECT 
    nome, 
    embedding <-> '[2,3,4]' AS distancia_l2
FROM teste_pgvector 
ORDER BY embedding <-> '[2,3,4]' 
LIMIT 3;

-- Testar outras funções de distância
SELECT 
    nome,
    embedding <-> '[2,3,4]' AS l2_distance,
    embedding <#> '[2,3,4]' AS inner_product,
    embedding <=> '[2,3,4]' AS cosine_distance,
    embedding <+> '[2,3,4]' AS l1_distance
FROM teste_pgvector;

-- Limpeza
DROP TABLE teste_pgvector;
```

### 3. **Configurar Parâmetros Otimizados**

```sql
-- Configurações para melhor performance (sessão atual)
SET hnsw.ef_search = 100;              -- Melhora qualidade de busca
SET maintenance_work_mem = '512MB';     -- Acelera criação de índices  
SET work_mem = '64MB';                  -- Otimiza consultas de vetores
SET max_parallel_maintenance_workers = 4; -- Paralelismo na criação de índices

-- Para tornar permanente, editar postgresql.conf:
-- hnsw.ef_search = 100
-- maintenance_work_mem = 512MB
-- work_mem = 64MB
-- max_parallel_maintenance_workers = 4
```

## 🧪 Script de Verificação Automática

Criar arquivo `verificar_pgvector.py`:

```python
#!/usr/bin/env python3
import asyncio
import asyncpg
import os

async def verificar_pgvector():
    """Verifica se pgvector está funcionando corretamente"""
    
    # Conectar ao banco
    try:
        conn = await asyncpg.connect(
            os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/curso")
        )
        print("✅ Conectado ao PostgreSQL")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    try:
        # Verificar versão PostgreSQL
        version = await conn.fetchval("SELECT version()")
        print(f"🐘 PostgreSQL: {version.split()[1]}")
        
        # Verificar se pgvector está disponível
        available = await conn.fetchval(
            "SELECT 1 FROM pg_available_extensions WHERE name = 'vector'"
        )
        if not available:
            print("❌ pgvector não está instalado")
            return False
        
        # Tentar habilitar extensão
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Verificar versão do pgvector
        version = await conn.fetchval(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        )
        print(f"📦 pgvector: {version}")
        
        # Teste funcional básico
        await conn.execute("""
            CREATE TEMP TABLE teste (embedding VECTOR(3));
            INSERT INTO teste VALUES ('[1,2,3]'), ('[4,5,6]');
        """)
        
        result = await conn.fetchval("""
            SELECT embedding <-> '[2,3,4]' 
            FROM teste 
            ORDER BY embedding <-> '[2,3,4]' 
            LIMIT 1
        """)
        
        if result is not None:
            print("✅ Busca por similaridade funcionando")
            print(f"📊 Distância de teste: {result:.4f}")
        else:
            print("❌ Falha na busca por similaridade")
            return False
        
        # Testar criação de índice HNSW
        await conn.execute("""
            CREATE TEMP TABLE teste_idx AS 
            SELECT ('[' || x || ',' || y || ',' || z || ']')::vector(3) as emb
            FROM generate_series(1,100) x, 
                 generate_series(1,10) y, 
                 generate_series(1,10) z 
            LIMIT 1000;
            
            CREATE INDEX ON teste_idx USING hnsw (emb vector_l2_ops);
        """)
        print("✅ Índice HNSW criado com sucesso")
        
        print("🎉 pgvector está totalmente funcional!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    
    finally:
        await conn.close()

if __name__ == "__main__":
    # Executar verificação
    success = asyncio.run(verificar_pgvector())
    exit(0 if success else 1)
```

**Executar verificação:**

```bash
# Instalar dependência
uv add asyncpg

# Executar teste
uv run verificar_pgvector.py
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. **Erro: "extension not found"**

```bash
# Verificar se pgvector está instalado no sistema
sudo find /usr -name "*vector*" | grep -E "\.(so|dll)$"

# Ubuntu/Debian: Reinstalar
sudo apt remove postgresql-*-pgvector
sudo apt install postgresql-15-pgvector

# macOS: Reinstalar via Homebrew
brew uninstall pgvector
brew install pgvector
```

#### 2. **Erro: "permission denied"**

```sql
-- Conectar como superuser
sudo -u postgres psql -d curso

-- Habilitar extensão como superuser
CREATE EXTENSION IF NOT EXISTS vector;

-- Dar permissões ao usuário
GRANT ALL ON SCHEMA public TO seu_usuario;
```

#### 3. **Erro: "could not load library"**

```bash
# Linux: Verificar bibliotecas
ldd /usr/lib/postgresql/15/lib/vector.so

# macOS: Verificar instalação
otool -L /opt/homebrew/lib/postgresql/vector.so

# Reinstalar se bibliotecas estiverem faltando
```

#### 4. **Performance baixa em consultas**

```sql
-- Aumentar parâmetros de performance
SET hnsw.ef_search = 200;
SET work_mem = '128MB';

-- Criar índices apropriados
CREATE INDEX USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);
```

#### 5. **Erro na criação de índices**

```sql
-- Aumentar memória para criação de índices
SET maintenance_work_mem = '1GB';
SET max_parallel_maintenance_workers = 4;

-- Criar índice em background (PostgreSQL 11+)
CREATE INDEX CONCURRENTLY idx_embedding 
ON tabela USING hnsw (embedding vector_l2_ops);
```

### Verificações de Sistema

#### Linux

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar versão instalada
sudo -u postgres psql -c "SELECT version();"

# Verificar diretório de extensões
sudo -u postgres psql -c "SHOW shared_preload_libraries;"

# Localizar arquivos do pgvector
dpkg -L postgresql-15-pgvector
```

#### macOS

```bash
# Verificar serviços Homebrew
brew services list | grep postgresql

# Verificar instalação
brew list pgvector

# Reiniciar PostgreSQL
brew services restart postgresql
```

#### Windows

```cmd
# Verificar serviço PostgreSQL
sc query postgresql-x64-17

# Verificar instalação via Registry
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\PostgreSQL"
```

## 📈 Otimização para Produção

### 1. **Configurações PostgreSQL**

Editar `postgresql.conf`:

```ini
# Configurações gerais
shared_buffers = 256MB                    # 25% da RAM disponível
effective_cache_size = 1GB                # 75% da RAM disponível
work_mem = 64MB                          # Para consultas de vetores
maintenance_work_mem = 512MB              # Para criação de índices

# Configurações específicas do pgvector
hnsw.ef_search = 100                     # Qualidade vs velocidade
max_parallel_maintenance_workers = 4      # Paralelismo
max_parallel_workers = 8                 # Workers totais

# Logging para debugging
log_min_duration_statement = 1000        # Log de queries > 1s
log_statement = 'all'                    # Para desenvolvimento apenas
```

### 2. **Estratégias de Indexação**

```sql
-- Para embeddings OpenAI (1536 dimensões)
CREATE INDEX idx_embeddings_hnsw 
ON tabela_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

-- Para consultas com filtros
CREATE INDEX idx_categoria_embedding 
ON tabela_embeddings (categoria_id, embedding) 
USING hnsw (embedding vector_cosine_ops);

-- Índice parcial para dados frequentes
CREATE INDEX idx_embeddings_ativos 
ON tabela_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WHERE ativo = true;
```

### 3. **Monitoramento**

```sql
-- Verificar uso de índices
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE indexname LIKE '%hnsw%';

-- Monitorar performance de queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE query LIKE '%<%' -- Operadores de distância
ORDER BY total_time DESC;

-- Verificar tamanho dos índices
SELECT 
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes 
WHERE indexname LIKE '%hnsw%';
```

## 🎯 Configuração para o Curso CrewAI

### 1. **Variáveis de Ambiente**

Criar arquivo `.env`:

```bash
# Banco de dados
DATABASE_URL=postgresql://postgres:password@localhost:5432/curso

# Para Docker
DATABASE_URL=postgresql://postgres:password@localhost:5432/curso

# Para produção (exemplo Supabase)
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### 2. **Script de Inicialização**

Criar `init_pgvector.sql`:

```sql
-- Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Configurações otimizadas para o curso
SET hnsw.ef_search = 100;
SET maintenance_work_mem = '512MB';
SET work_mem = '64MB';

-- Verificar instalação
SELECT 
    'pgvector instalado com sucesso!' as status,
    extversion as versao
FROM pg_extension 
WHERE extname = 'vector';

-- Teste rápido
CREATE TEMP TABLE teste_instalacao (
    id SERIAL,
    embedding VECTOR(1536)  -- Dimensão do OpenAI
);

INSERT INTO teste_instalacao (embedding) 
SELECT random_vector(1536) 
FROM generate_series(1, 10);

SELECT 'Teste concluído - pgvector funcionando!' as resultado;
```

### 3. **Executar Inicialização**

```bash
# Conectar e executar script
psql $DATABASE_URL -f init_pgvector.sql

# Ou via Docker
docker exec -i postgres-pgvector psql -U postgres -d curso < init_pgvector.sql
```

## 🎉 Próximos Passos

Após instalar e configurar o pgvector com sucesso:

1. ✅ **Execute o script de migração de dados**:
   ```bash
   uv run aula7/scripts/01_criar_tabelas_embeddings.sql
   ```

2. ✅ **Migre os dados existentes para embeddings**:
   ```bash
   uv run aula7/scripts/02_migrar_dados_embeddings.py
   ```

3. ✅ **Teste o sistema completo**:
   ```bash
   uv run aula7/scripts/03_testar_embeddings.py
   ```

4. ✅ **Continue com as aulas do CrewAI**:
   - Aula 7: Agentes com embeddings
   - Aula 8: API FastAPI + WhatsApp
   - Aula 9: Sistema completo em produção

---

**🎊 Parabéns! Você agora tem pgvector instalado e configurado para criar um sistema de triagem médica inteligente com CrewAI!**