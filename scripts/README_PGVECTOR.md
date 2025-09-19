# 🚀 Instalação e Configuração do pgvector - Curso CrewAI

Este diretório contém todos os recursos necessários para instalar, configurar e verificar o pgvector no PostgreSQL para o Curso CrewAI.

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [⚡ Instalação Rápida (Docker)](#-instalação-rápida-docker)
- [🔧 Instalação Manual](#-instalação-manual)  
- [✅ Verificação Automática](#-verificação-automática)
- [📚 Documentação Completa](#-documentação-completa)
- [🩺 Troubleshooting](#-troubleshooting)
- [🎭 Contexto do Curso](#-contexto-do-curso)

---

## 🎯 Visão Geral

O **pgvector** é uma extensão PostgreSQL que adiciona suporte a vetores e busca por similaridade, essencial para o sistema de triagem médica inteligente do Curso CrewAI.

### 🏥 Por que pgvector no Curso CrewAI?

- **🤖 Embeddings OpenAI**: Armazenar vetores de 1536 dimensões
- **🔍 Busca Semântica**: Encontrar sintomas similares por proximidade
- **⚡ Performance**: Índices HNSW e IVFFlat para consultas rápidas
- **🏥 Triagem Inteligente**: Classificação automática de sintomas

---

## ⚡ Instalação Rápida (Docker)

### 🐳 Método Recomendado

```bash
# 1. Executar instalação automática
./scripts/instalar_pgvector_docker.sh

# 2. Verificar instalação  
uv run scripts/configurar_pgvector.py

# 3. Testar funcionalidades
uv run aula7/exemplos/teste_pgvector.py
```

### 🎊 O que o script faz

- ✅ Instala PostgreSQL 17 + pgvector via Docker
- ✅ Cria database `curso` com usuário `postgres`
- ✅ Habilita extensão pgvector automaticamente
- ✅ Cria dados de teste com embeddings 1536D
- ✅ Configura índices HNSW para performance
- ✅ Gera arquivo `.env` com configurações
- ✅ Testa funcionalidades básicas

### 📊 Resultado Esperado

```
🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!
===============================================
📊 Informações de Conexão:
  Host: localhost
  Port: 5432
  Database: curso
  User: postgres
  Password: password

🔗 String de Conexão:
  postgresql://postgres:password@localhost:5432/curso
```

---

## 🔧 Instalação Manual

### 🐧 Ubuntu/Debian

```bash
# Instalar PostgreSQL e pgvector
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo apt install postgresql-15-pgvector

# Configurar banco
sudo -u postgres createdb curso
sudo -u postgres psql curso -c "CREATE EXTENSION vector;"
```

### 🍎 macOS

```bash
# Instalar via Homebrew
brew install postgresql
brew install pgvector

# Iniciar PostgreSQL
brew services start postgresql

# Configurar banco
createdb curso
psql curso -c "CREATE EXTENSION vector;"
```

### 🪟 Windows

Recomendamos usar **Docker** no Windows. Para instalação nativa:

1. Baixar PostgreSQL: <https://www.postgresql.org/download/windows/>
2. Compilar pgvector: <https://github.com/pgvector/pgvector#windows>

### ☁️ Serviços Hospedados

#### Supabase (Recomendado)

```bash
# pgvector já incluído
# 1. Criar projeto em https://supabase.com
# 2. Ir para SQL Editor
# 3. Executar: CREATE EXTENSION vector;
```

#### Neon

```bash  
# 1. Criar projeto em https://neon.tech
# 2. Habilitar pgvector nas configurações
```

#### Railway

```bash
# 1. Deploy PostgreSQL template
# 2. Adicionar pgvector via SQL
```

---

## ✅ Verificação Automática

### 🔍 Script de Configuração Inteligente

```bash
# Verificar e configurar automaticamente
uv run scripts/configurar_pgvector.py
```

### 🧪 O que o script verifica

- ✅ **Versão PostgreSQL**: Compatibilidade (13+)
- ✅ **Extensão pgvector**: Instalação e versão
- ✅ **Funcionalidades**: Vetores, índices, similaridade
- ✅ **Dimensões OpenAI**: Suporte a 1536 dimensões
- ✅ **Performance**: Índices HNSW e IVFFlat
- ✅ **Configurações**: Parâmetros otimizados

### 📊 Relatório de Status

```json
{
  "status": "ready",
  "postgresql": {
    "version": "17.1",
    "compatible": true
  },
  "pgvector": {
    "version": "0.8.1",
    "installed": true
  },
  "testes": {
    "basic_functionality": true,
    "openai_embedding_support": true,
    "indices_suportados": ["hnsw", "ivfflat"]
  }
}
```

---

## 📚 Documentação Completa

### 📖 Guias Disponíveis

| Arquivo | Descrição |
|---------|-----------|
| 📘 [`INSTALACAO_PGVECTOR_COMPLETO.md`](../docs/INSTALACAO_PGVECTOR_COMPLETO.md) | Guia completo com todos os métodos de instalação |
| 🐍 [`configurar_pgvector.py`](configurar_pgvector.py) | Script de configuração e verificação automática |
| 🐳 [`instalar_pgvector_docker.sh`](instalar_pgvector_docker.sh) | Instalação automática via Docker |
| 📋 [`README_PGVECTOR.md`](README_PGVECTOR.md) | Este arquivo - índice de recursos |

### 🔧 Scripts Utilitários

```bash
# Configuração completa
./scripts/instalar_pgvector_docker.sh     # Docker (recomendado)
uv run scripts/configurar_pgvector.py     # Verificação automática

# Testes e exemplos  
uv run aula7/exemplos/01_test_pgvector.py  # Teste básico
uv run aula7/exemplos/02_embeddings_openai.py  # OpenAI + pgvector
```

---

## 🩺 Troubleshooting

### ❌ Problemas Comuns

#### 🔌 "Erro de conexão PostgreSQL"

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql   # Linux
brew services list | grep postgresql  # macOS  
docker ps | grep postgres        # Docker

# Verificar porta 5432
netstat -tulpn | grep 5432
```

#### 📦 "pgvector não encontrado"

```bash
# Ubuntu/Debian - instalar pgvector
sudo apt install postgresql-15-pgvector

# macOS - instalar via Homebrew
brew install pgvector

# Docker - usar imagem oficial
docker run pgvector/pgvector:pg17
```

#### 🔑 "Permissão negada para criar extensão"

```bash
# Conectar como superuser
sudo -u postgres psql curso

# Dar permissões ao usuário
ALTER USER seu_usuario CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE curso TO seu_usuario;
```

#### 🐳 "Docker não encontrado"

```bash
# Instalar Docker
# Linux: https://docs.docker.com/engine/install/ubuntu/  
# macOS: https://docs.docker.com/desktop/mac/
# Windows: https://docs.docker.com/desktop/windows/

# Verificar instalação
docker --version
docker run hello-world
```

### 🔍 Diagnóstico Avançado

```bash
# 1. Testar conexão manual
psql "postgresql://postgres:password@localhost:5432/curso"

# 2. Verificar extensões disponíveis  
SELECT * FROM pg_available_extensions WHERE name = 'vector';

# 3. Verificar versão instalada
SELECT extversion FROM pg_extension WHERE extname = 'vector';

# 4. Testar funcionalidade básica
SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector;
```

### 📞 Suporte

Se os problemas persistirem:

1. 📋 Execute: `uv run scripts/configurar_pgvector.py`
2. 📄 Compartilhe o arquivo `pgvector_config_report.json` gerado
3. 🔍 Inclua logs de erro completos
4. 💻 Especifique seu sistema operacional e versão

---

## 🎭 Contexto do Curso

### 🏥 Sistema de Triagem Médica Inteligente

O pgvector será usado para:

#### 1. 🤖 **Embeddings de Sintomas**

```sql
-- Tabela de sintomas com embeddings OpenAI
CREATE TABLE sintomas (
    id SERIAL PRIMARY KEY,
    descricao TEXT,
    categoria TEXT,
    embedding VECTOR(1536)  -- OpenAI text-embedding-3-small
);
```

#### 2. 🔍 **Busca por Similaridade**  

```sql
-- Encontrar sintomas similares
SELECT descricao, categoria,
       embedding <-> $1 AS similaridade
FROM sintomas 
ORDER BY embedding <-> $1 
LIMIT 5;
```

#### 3. ⚡ **Índices para Performance**

```sql
-- HNSW: Melhor para consultas
CREATE INDEX idx_sintomas_hnsw 
ON sintomas USING hnsw (embedding vector_l2_ops);

-- IVFFlat: Mais rápido para construir
CREATE INDEX idx_sintomas_ivfflat 
ON sintomas USING ivfflat (embedding vector_l2_ops) 
WITH (lists = 100);
```

#### 4. 🎯 **Integração com CrewAI**

```python
# Agente que usa pgvector para encontrar sintomas similares
agente_triagem = Agent(
    role="Especialista em Triagem",
    goal="Classificar sintomas usando similaridade semântica",
    backstory="Usa embeddings para encontrar padrões em sintomas",
    tools=[FerramentaBuscaSintomas(pgvector_conn)]
)
```

### 📚 Aulas que Usam pgvector

- **🎓 Aula 7**: Introdução a embeddings e pgvector
- **🎓 Aula 8**: Sistema de triagem com busca semântica  
- **🎓 Aula 9**: Otimização de performance com índices
- **🎓 Aula 10**: Deploy do sistema completo

### 🎯 Objetivos de Aprendizado

Após configurar o pgvector, você será capaz de:

- ✅ **Armazenar** embeddings de texto em PostgreSQL
- ✅ **Buscar** por similaridade semântica
- ✅ **Otimizar** consultas com índices apropriados
- ✅ **Integrar** pgvector com agentes CrewAI
- ✅ **Construir** sistemas de IA baseados em similaridade

---

## 🚀 Próximos Passos

1. **⚡ Instale** o pgvector usando um dos métodos acima
2. **✅ Verifique** a instalação com o script automático  
3. **🎓 Continue** para a Aula 7: Embeddings e Busca Semântica
4. **🏥 Implemente** o sistema de triagem médica
5. **📈 Otimize** performance para produção

---

**💡 Dica**: Para melhor experiência, use o **método Docker** - é mais rápido, confiável e funciona em todos os sistemas operacionais.

**🎯 Meta**: Ter pgvector funcionando 100% para construir o sistema de triagem médica mais inteligente do curso!

---

*📚 Curso CrewAI - Sistemas Multi-Agentes Inteligentes*  
*🏥 Aplicação: Triagem Médica Automatizada com IA*
