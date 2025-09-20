# Exercício PostgreSQL + CrewAI

## 📋 Objetivo
Exercício prático simples: criar um agente CrewAI que consulta estabelecimentos médicos no banco PostgreSQL.

## 🚀 Execução Rápida

```bash
# Executar exercício
uv run aula7/exercicio_agente_postgres.py
```

## 🔧 Pré-requisitos

### PostgreSQL
```bash
# Opção 1: Docker (recomendado)
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=arpus \
  -e POSTGRES_DB=curso \
  -p 5432:5432 \
  -d postgres:16

# Opção 2: PostgreSQL local
# Criar banco 'curso' no PostgreSQL local
```

### Dependências Python
```bash
uv add psycopg2-binary
```

### Variáveis de Ambiente (.env)
```env
OPENAI_API_KEY=sua_chave_aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=curso
POSTGRES_USER=postgres
POSTGRES_PASSWORD=arpus
```

## 📚 O que o Exercício Ensina

### 1. **Integração CrewAI + PostgreSQL**
- Como conectar agentes ao banco de dados
- Buscar informações estruturadas
- Processar resultados do banco

### 2. **Estrutura do Código**
```python
# Classe para gerenciar PostgreSQL
class BuscadorEstabelecimentos:
    def buscar_estabelecimentos(self, tipo, municipio)
    
# Agente CrewAI especializado
agente = Agent(
    role="Especialista em Busca de Estabelecimentos Médicos",
    # ... configuração
)
```

### 3. **Funcionalidades Implementadas**
- ✅ Conexão PostgreSQL
- ✅ Busca com filtros (tipo, município)
- ✅ Inserção de dados de exemplo
- ✅ Integração com agente CrewAI
- ✅ Tratamento de erros

## 🔍 Estrutura do Banco

```sql
-- Tabela principal do exercício
CREATE TABLE estabelecimentos (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,        -- hospital, upa, clinica
    municipio TEXT NOT NULL,
    telefone TEXT,
    endereco TEXT,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7)
);
```

## 📊 Exemplo de Saída

```
🏥 HOSPITAIS EM SÃO PAULO:
   • Hospital São Paulo - (11) 9999-9999
     Endereço: Rua Exemplo, 123 - São Paulo

🚑 UPAS DISPONÍVEIS:
   • UPA Central - São Paulo
     Telefone: (11) 9999-9999

🩺 CLÍNICAS ENCONTRADAS:
   • Clínica Santa Maria - Santo André
     Telefone: (11) 9999-9999

✅ EXERCÍCIO CONCLUÍDO!
📊 Resultados: 4 estabelecimentos encontrados
```

## 🎯 Conceitos Aprendidos

1. **Integração de Dados**: Como conectar agentes IA a bancos reais
2. **Busca Estruturada**: Filtros e queries dinâmicas
3. **Tratamento de Erros**: Conexões de banco robustas
4. **Organização de Código**: Separação de responsabilidades

## 🔧 Troubleshooting

### Erro de Conexão PostgreSQL
```bash
# Verificar se está rodando
docker ps

# Verificar logs
docker logs postgres-crewai

# Recriar container
docker rm -f postgres-crewai
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=arpus \
  -e POSTGRES_DB=curso \
  -p 5432:5432 \
  -d postgres:16
```

### Dependência Não Encontrada
```bash
uv add psycopg2-binary python-dotenv
```

## 💡 Extensões Possíveis

1. **Busca Geográfica**: Adicionar cálculos de distância
2. **Cache**: Implementar cache de consultas
3. **API REST**: Expor funcionalidades via Flask
4. **Embeddings**: Busca semântica com pgvector

---

**Próximo passo**: Explorar `aula7/main.py` para exemplos mais avançados com embeddings e geolocalização!