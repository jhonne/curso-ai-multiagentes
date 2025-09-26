# 🔄 Migração PostgreSQL → SQLite

Este script migra os dados do banco PostgreSQL 'curso' para um banco SQLite 'curso.db', preservando toda a estrutura e dados das tabelas de atendimento médico.

## 📋 Tabelas Migradas

- **ia_estabelecimento** - Estabelecimentos de saúde
- **ia_queixa_principal** - Queixas principais 
- **ia_sintoma** - Sintomas médicos
- **ia_historico_atendimento_sintoma** - Histórico de atendimento com sintomas

## 🔧 Pré-requisitos

### 1. Dependências Python
```bash
# Instalar psycopg2 para conexão PostgreSQL
uv add psycopg2-binary

# SQLite3 já vem nativo com Python
```

### 2. Banco PostgreSQL
- PostgreSQL rodando em localhost:5432
- Banco 'curso' criado e populado com os dados
- Usuário 'postgres' com acesso ao banco
- Senha 'postgres' (ajustar no script se necessário)

## 🚀 Como Usar

### 1. Testar Ambiente (Recomendado)
```bash
uv run testar_ambiente_migracao.py
```

Este script verifica:
- ✅ Dependências instaladas
- ✅ Conexão com PostgreSQL
- ✅ Existência das tabelas
- ✅ Funcionalidade do SQLite

### 2. Executar Migração
```bash
uv run migrar_postgres_para_sqlite.py
```

O script irá:
- 🔌 Conectar aos dois bancos
- 📋 Criar estrutura das tabelas em SQLite
- 📊 Migrar todos os dados
- ✅ Validar a migração
- 📁 Gerar log detalhado

## ⚙️ Configurações

### PostgreSQL (migrar_postgres_para_sqlite.py, linha 25)
```python
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': '5432', 
    'database': 'curso',
    'user': 'postgres',      # Ajustar se necessário
    'password': 'postgres'   # Ajustar se necessário
}
```

### SQLite
```python
SQLITE_DB = 'curso.db'  # Arquivo será criado na pasta atual
```

## 📊 Estrutura das Tabelas SQLite

### ia_estabelecimento
```sql
CREATE TABLE ia_estabelecimento (
    cnes TEXT PRIMARY KEY,     -- Código CNES
    nome TEXT,                 -- Nome do estabelecimento
    endereco TEXT,             -- Endereço
    fone TEXT,                 -- Telefone
    bairro TEXT,               -- Bairro
    longitude REAL,            -- Coordenada longitude
    latitude REAL              -- Coordenada latitude
);
```

### ia_queixa_principal  
```sql
CREATE TABLE ia_queixa_principal (
    id INTEGER PRIMARY KEY,    -- ID da queixa
    nome TEXT                  -- Descrição da queixa
);
```

### ia_sintoma
```sql
CREATE TABLE ia_sintoma (
    id INTEGER PRIMARY KEY,    -- ID do sintoma
    nome TEXT                  -- Descrição do sintoma
);
```

### ia_historico_atendimento_sintoma
```sql
CREATE TABLE ia_historico_atendimento_sintoma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto incremento
    estabelecimento_cnes TEXT,              -- FK para estabelecimento
    queixa_principal_id INTEGER,            -- FK para queixa principal
    sintoma_id INTEGER,                     -- FK para sintoma
    FOREIGN KEY (estabelecimento_cnes) REFERENCES ia_estabelecimento(cnes),
    FOREIGN KEY (queixa_principal_id) REFERENCES ia_queixa_principal(id),
    FOREIGN KEY (sintoma_id) REFERENCES ia_sintoma(id)
);
```

## 📈 Volume de Dados Esperado

Baseado nos scripts SQL:
- **ia_estabelecimento**: ~8 registros
- **ia_queixa_principal**: ~148 registros  
- **ia_sintoma**: ~266 registros
- **ia_historico_atendimento_sintoma**: ~1.579 registros

## 📝 Arquivos Gerados

- **curso.db** - Banco SQLite com os dados migrados
- **migracao.log** - Log detalhado do processo de migração

## 🔍 Validação

O script inclui validação automática que compara:
- Contagem de registros entre PostgreSQL e SQLite
- Integridade referencial das chaves estrangeiras
- Estrutura das tabelas criadas

## ⚠️ Observações Importantes

1. **Sobrescrita**: O script pergunta se deve sobrescrever o arquivo SQLite existente
2. **Tipos de Dados**: Adaptação automática de tipos PostgreSQL → SQLite:
   - `char(7)` → `TEXT`
   - `varchar(255)` → `TEXT`  
   - `INTEGER` → `INTEGER`
   - `DOUBLE PRECISION` → `REAL`
3. **Chaves Estrangeiras**: Incluídas no SQLite para manter integridade
4. **Log**: Processo completo registrado em migracao.log

## 🐛 Troubleshooting

### Erro de Conexão PostgreSQL
```
❌ Erro na conexão PostgreSQL: could not connect to server
```
**Solução**: Verificar se PostgreSQL está rodando e configurações de conexão

### Dependência Não Encontrada  
```
❌ psycopg2 não encontrado
```
**Solução**: `uv add psycopg2-binary`

### Tabela Não Existe
```  
❌ ia_estabelecimento: relation "ia_estabelecimento" does not exist
```
**Solução**: Executar os scripts SQL da pasta `/sql` no PostgreSQL primeiro

### Permissão Negada
```
❌ permission denied for relation ia_estabelecimento
```
**Solução**: Verificar permissões do usuário PostgreSQL

## 🎯 Exemplo de Uso

```bash
# 1. Instalar dependências
uv add psycopg2-binary

# 2. Testar ambiente
uv run testar_ambiente_migracao.py

# 3. Se tudo OK, executar migração
uv run migrar_postgres_para_sqlite.py

# 4. Verificar resultado
ls -la curso.db
sqlite3 curso.db "SELECT COUNT(*) FROM ia_estabelecimento;"
```

## 📊 Exemplo de Consulta SQLite

```sql
-- Estabelecimentos com mais atendimentos
SELECT 
    e.nome,
    COUNT(*) as total_atendimentos
FROM ia_historico_atendimento_sintoma h
JOIN ia_estabelecimento e ON h.estabelecimento_cnes = e.cnes
GROUP BY e.cnes, e.nome
ORDER BY total_atendimentos DESC
LIMIT 5;
```

---

**Autor**: Gerado pelo GitHub Copilot  
**Data**: 26 de setembro de 2025  
**Versão**: 1.0