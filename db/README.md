# 🗄️ Pasta DB - Migração PostgreSQL → SQLite

Esta pasta contém todos os arquivos relacionados à migração dos dados do banco PostgreSQL 'curso' para SQLite.

## 📁 Estrutura dos Arquivos

### 🚀 Scripts de Migração
- **`migrar_postgres_para_sqlite.py`** - Script principal de migração
- **`configurar_migracao.py`** - Configurador interativo de credenciais PostgreSQL
- **`testar_ambiente_migracao.py`** - Teste de ambiente e dependências
- **`testar_sqlite.py`** - Validação do banco SQLite criado
- **`exemplo_uso_sqlite.py`** - Exemplos práticos de uso do banco

### 🗄️ Banco de Dados
- **`curso.db`** - Banco SQLite com os dados migrados (81 KB)

### ⚙️ Configurações e Logs
- **`config_migracao.json`** - Configurações de conexão PostgreSQL
- **`migracao.log`** - Log detalhado da migração

### 📊 Dados Exportados
- **`dados_curso_*.json`** - Exemplo de exportação dos dados para JSON

### 📚 Documentação
- **`README_MIGRACAO.md`** - Guia completo de instalação e uso
- **`MIGRACAO_CONCLUIDA.md`** - Resumo final da migração
- **`README.md`** - Este arquivo (índice da pasta)

## 🚀 Como Usar

### Primeira Migração
```bash
cd db

# 1. Configurar credenciais PostgreSQL
uv run python configurar_migracao.py

# 2. Testar ambiente (opcional)
uv run python testar_ambiente_migracao.py

# 3. Executar migração
uv run python migrar_postgres_para_sqlite.py

# 4. Validar resultado
uv run python testar_sqlite.py
```

### Usar o Banco SQLite
```bash
cd db

# Ver exemplos de uso
uv run python exemplo_uso_sqlite.py

# Usar em seus próprios scripts
python
>>> from exemplo_uso_sqlite import BancoCursoSQLite
>>> banco = BancoCursoSQLite()
>>> banco.conectar()
>>> estabelecimentos = banco.obter_estabelecimentos()
```

### Consulta Direta SQLite
```python
import sqlite3

# Conectar ao banco
conn = sqlite3.connect('db/curso.db')
cursor = conn.cursor()

# Fazer consulta
cursor.execute("SELECT * FROM ia_estabelecimento")
resultados = cursor.fetchall()
print(f"Encontrados {len(resultados)} estabelecimentos")

conn.close()
```

## 📊 Dados Disponíveis

### Tabelas Migradas
- **ia_estabelecimento** (8 registros) - Estabelecimentos de saúde
- **ia_queixa_principal** (141 registros) - Queixas principais
- **ia_sintoma** (266 registros) - Sintomas médicos  
- **ia_historico_atendimento_sintoma** (1,579 registros) - Histórico de atendimentos

### Total: 1,994 registros migrados com 100% de sucesso

## 🔧 Atualização dos Dados

Para atualizar os dados do banco SQLite:

```bash
cd db
uv run python migrar_postgres_para_sqlite.py
```

O script irá:
- Conectar ao PostgreSQL
- Recriar as tabelas no SQLite
- Migrar todos os dados atualizados
- Validar a integridade

## 📖 Documentação Completa

Consulte os arquivos de documentação para informações detalhadas:
- `README_MIGRACAO.md` - Guia técnico completo
- `MIGRACAO_CONCLUIDA.md` - Resumo e estatísticas

---

*Migração criada em 26 de setembro de 2025 pelo GitHub Copilot*