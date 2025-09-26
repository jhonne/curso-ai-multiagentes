# 🗄️ Migração PostgreSQL → SQLite

Esta migração foi **organizada na pasta `db/`** para melhor estruturação do projeto.

## 📁 Localização dos Arquivos

Todos os arquivos da migração estão agora em: **`db/`**

### 🚀 Como Usar

```bash
# Navegar para a pasta db
cd db

# Executar scripts de migração
uv run python migrar_postgres_para_sqlite.py

# Testar banco
uv run python testar_sqlite.py

# Ver exemplos
uv run python exemplo_uso_sqlite.py
```

### 📊 Acessar o Banco SQLite

O banco SQLite está em: **`db/curso.db`**

```python
import sqlite3

# Conectar ao banco
conn = sqlite3.connect('db/curso.db')
cursor = conn.cursor()

# Fazer consultas
cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
print(f"Estabelecimentos: {cursor.fetchone()[0]}")

conn.close()
```

### 📚 Documentação Completa

Consulte a documentação na pasta `db/`:
- **`db/README.md`** - Índice da pasta db
- **`db/README_MIGRACAO.md`** - Guia técnico completo  
- **`db/MIGRACAO_CONCLUIDA.md`** - Resumo e estatísticas

---

**✅ Migração concluída com 100% de sucesso!**  
*1.994 registros migrados de 4 tabelas do PostgreSQL para SQLite*