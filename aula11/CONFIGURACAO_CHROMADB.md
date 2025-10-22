# Configuração do ChromaDB - Desenvolvedor

## Sobre a Organização Automática

Todos os scripts da Aula 11 importam automaticamente `config_chromadb.py`, que:

1. **Cria o diretório `.chromadb/`** na raiz da aula11
2. **Configura variáveis de ambiente** para o ChromaDB usar este diretório
3. **Funciona em qualquer subpasta** (detecta automaticamente a raiz)

## Como Funciona

### Importação Automática

Todos os scripts principais já incluem:

```python
import config_chromadb  # noqa: F401
```

Isso garante que o ChromaDB use `.chromadb/` em vez da raiz.

### Para Novos Scripts

Se criar um novo script na aula11, adicione no início:

```python
# Seu script: aula11/meu_script.py
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Adicione esta linha
import config_chromadb  # noqa: F401

load_dotenv()
```

### Para Scripts em Módulos

Se criar scripts dentro de `modulos/`:

```python
# Seu script: aula11/modulos/meu_modulo/script.py
import sys
from pathlib import Path

# Adicionar aula11 ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config_chromadb  # noqa: F401
```

## Variáveis de Ambiente

O `config_chromadb.py` configura automaticamente:

```bash
CHROMA_DB_IMPL=duckdb+parquet
CHROMA_PERSIST_DIRECTORY=/caminho/para/aula11/.chromadb
IS_PERSISTENT=TRUE
```

Você pode sobrescrever no seu `.env` local se necessário.

## Limpeza

### Limpar Cache do ChromaDB

```bash
cd aula11
rm -rf .chromadb/
```

Os scripts recriarão automaticamente quando executados.

### Arquivos Lock Órfãos

Se encontrar arquivos `chromadb-*.lock` na raiz, pode movê-los:

```bash
mv chromadb-*.lock .chromadb/
```

Ou executar o script de limpeza:

```bash
./.organize_chromadb.sh
```

## Verificação

### Ver Configuração Atual

```bash
uv run python config_chromadb.py
```

Saída:
```
============================================================
CONFIGURAÇÃO CHROMADB
============================================================
📁 Diretório da Aula11: /caminho/para/aula11
💾 Diretório ChromaDB: /caminho/para/aula11/.chromadb
✅ Diretório existe: True
📋 Arquivos no ChromaDB:
   - chromadb-xxx.lock
   - chromadb-yyy.lock
   ...
============================================================
```

### Verificar que Está Funcionando

1. Execute qualquer script
2. Verifique que não há arquivos lock na raiz:

```bash
ls -1 | grep "chromadb-.*\.lock"
# Não deve retornar nada
```

3. Verifique que estão no lugar certo:

```bash
ls -1 .chromadb/
# Deve listar arquivos .lock
```

## Troubleshooting

### Problema: Arquivos ainda aparecem na raiz

**Solução 1:** Verifique se o script importa `config_chromadb`:

```python
import config_chromadb  # noqa: F401
```

**Solução 2:** Verifique se está usando `uv run`:

```bash
uv run script.py  # ✅ Correto
python script.py  # ❌ Pode não carregar config
```

**Solução 3:** Mova manualmente e reporte:

```bash
mv chromadb-*.lock .chromadb/
```

### Problema: Erro de import config_chromadb

Se o script estiver em um módulo, adicione ao path:

```python
import sys
from pathlib import Path

# Para scripts em modulos/*/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config_chromadb  # noqa: F401
```

### Problema: ChromaDB não persiste dados

Verifique as variáveis de ambiente:

```python
import os
print(os.environ.get('CHROMA_PERSIST_DIRECTORY'))
print(os.environ.get('IS_PERSISTENT'))
```

Deve mostrar:
```
/caminho/para/aula11/.chromadb
TRUE
```

## Estrutura de Arquivos

```text
aula11/
├── .chromadb/                    ← Arquivos do ChromaDB aqui
│   ├── chromadb-xxx.lock
│   ├── chromadb-yyy.lock
│   └── chroma.sqlite3 (se criado)
│
├── config_chromadb.py            ← Configuração automática
├── .env.example                  ← Template de configuração
├── quick_start.py                ← Já importa config_chromadb
├── exercicio_rapido.py           ← Já importa config_chromadb
│
└── modulos/
    ├── 01_memory/
    │   ├── exemplo.py            ← Já importa config_chromadb
    │   └── .chromadb/            ← Pode ter cache local
    └── ...
```

## Benefícios

- ✅ **Zero configuração manual** - Funciona automaticamente
- 📁 **Organização** - Arquivos em pasta dedicada
- 🧹 **Fácil limpeza** - `rm -rf .chromadb/`
- 🔧 **Centralizado** - Um lugar para gerenciar
- 🚫 **Git limpo** - `.gitignore` já configurado

## Git

O `.gitignore` do projeto já inclui:

```gitignore
# ChromaDB files
.chromadb/
**/chromadb-*.lock
```

Arquivos do ChromaDB não serão commitados.
