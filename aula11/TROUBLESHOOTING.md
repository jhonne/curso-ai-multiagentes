# Troubleshooting - Aula 11: RAG com CrewAI

Soluções para problemas comuns ao trabalhar com Memory e Knowledge Sources.

## 🔧 Problemas com ChromaDB

### Problema: Arquivos `.lock` espalhados na raiz

**Sintoma**: Vários arquivos `chromadb-*.lock` aparecem na raiz da `aula11/`:

```text
aula11/
├── chromadb-3b07b091bbcdd5ac73952d217efa03c5.lock  ❌
├── chromadb-7c19cefd3634454bd35ec942596ba13c.lock  ❌
├── chromadb-98abfc500271a34128be6c8536427f7d.lock  ❌
```

**Causa**: ChromaDB foi inicializado antes da configuração de storage customizado.

**Solução**: Os arquivos principais (`main.py`, exemplos) já estão corrigidos. Para limpar arquivos antigos:

```bash
cd aula11
rm -f chromadb-*.lock
```

Para prevenir no futuro, sempre configure storage **antes** de importar CrewAI:

```python
# ✅ CORRETO
import os
from pathlib import Path

STORAGE_DIR = Path(__file__).parent / ".chromadb"
os.environ["CREWAI_STORAGE_DIR"] = str(STORAGE_DIR)

# AGORA importar CrewAI
from crewai import Agent, Crew
```

### Problema: "ChromaDB not found" ou erro de importação

**Solução**: Reinstalar dependências:

```bash
uv sync
```

Se o problema persistir:

```bash
uv add chromadb --force
```

### Problema: Limpar cache do ChromaDB

**Quando**: Você modificou documentos e quer reprocessar embeddings.

**Solução**:

```bash
rm -rf .chromadb/
```

Na próxima execução, os embeddings serão recriados.

## 🧠 Problemas com Memory

### Problema: Memory não está funcionando

**Sintoma**: Agente não lembra de conversas anteriores.

**Verificações**:

1. **Memory está ativada?**

```python
agent = Agent(
    role="...",
    memory=True,  # ← Deve estar True
    verbose=True
)
```

2. **Crew está com memory?**

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,  # ← Também deve estar True
    verbose=True
)
```

3. **Verifique se arquivos de memory foram criados**:

```bash
ls -la .chromadb/
# Deve mostrar: short_term_memory/, long_term_memory/, entities/
```

### Problema: Memory persiste entre execuções quando não deveria

**Sintoma**: Agente lembra de conversas de execuções anteriores.

**Causa**: Long-term memory está habilitada por padrão.

**Solução temporária**: Limpar storage antes de executar:

```bash
rm -rf .chromadb/
uv run main.py
```

**Solução permanente**: Desabilitar long-term memory:

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    # Configurar para usar apenas short-term
    verbose=True
)
```

### Problema: Memory consome muita RAM

**Causa**: Histórico de conversas muito longo.

**Solução**: Limitar tamanho do histórico ou limpar periodicamente:

```bash
# Limpar memory antiga
rm -rf .chromadb/short_term_memory/
rm -rf .chromadb/long_term_memory/
```

## 📚 Problemas com Knowledge Sources

### Problema: Knowledge Source não encontra arquivo

**Sintoma**: Erro `FileNotFoundError` ao criar knowledge source.

**Solução**: Usar caminho absoluto ou relativo correto:

```python
from pathlib import Path

# Caminho absoluto
AULA11_DIR = Path(__file__).parent
arquivo = AULA11_DIR / "conhecimento_medico" / "protocolos" / "urgencia_emergencia.txt"

source = TextFileKnowledgeSource(file_path=str(arquivo))

# Verificar se existe
print(f"Arquivo existe? {arquivo.exists()}")
```

### Problema: Agente não está usando o conhecimento

**Sintoma**: Agente responde genericamente, sem consultar documentos.

**Verificações**:

1. **Knowledge source está configurada?**

```python
agent = Agent(
    role="...",
    knowledge_sources=[source1, source2],  # ← Deve ter sources
    verbose=True
)
```

2. **Conteúdo do documento é relevante?**

Teste com conteúdo explícito:

```python
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Teste simples
test_source = StringKnowledgeSource(
    content="A resposta para a questão principal é: 42",
    metadata={"tipo": "teste"}
)

agent = Agent(
    role="Assistente",
    goal="Responder perguntas",
    backstory="Assistente prestativo.",
    knowledge_sources=[test_source],
    verbose=True
)

task = Task(
    description="Qual é a resposta para a questão principal?",
    expected_output="A resposta",
    agent=agent
)
```

3. **Ative verbose para debug**:

```python
agent = Agent(
    role="...",
    verbose=True,  # ← Ver o que o agente está fazendo
    knowledge_sources=[source]
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True  # ← Ver processo completo
)
```

### Problema: Primeira execução muito lenta

**Causa**: Embeddings estão sendo criados pela primeira vez.

**Comportamento normal**: Primeira execução pode levar 30-60 segundos para processar documentos grandes.

**Próximas execuções**: Serão rápidas (embeddings em cache).

**Solução**: Apenas aguardar. Para documentos muito grandes, considere dividir em partes menores.

### Problema: "Embedding dimension mismatch"

**Sintoma**: Erro sobre dimensões incompatíveis de embeddings.

**Causa**: Você mudou o modelo de embeddings mas o cache antigo ainda existe.

**Solução**: Limpar cache e recriar embeddings:

```bash
rm -rf .chromadb/knowledge/
uv run main.py
```

## 🔑 Problemas com API Keys

### Problema: "OpenAI API key not found"

**Solução**: Configurar chave no `.env`:

```bash
# No arquivo .env na raiz do projeto
OPENAI_API_KEY=sk-proj-sua_chave_aqui
```

Ou configurar automaticamente:

```bash
uv run configurar-crewai
```

### Problema: "Rate limit exceeded"

**Causa**: Muitas requisições para a API OpenAI em curto espaço de tempo.

**Soluções**:

1. **Aguardar alguns minutos** antes de executar novamente
2. **Reduzir volume de testes**: Testar com documentos menores
3. **Usar cache**: Embeddings são cacheados automaticamente

## 💾 Problemas com Banco de Dados SQLite

### Problema: "Database is locked"

**Sintoma**: Erro ao tentar acessar `long_term_memory_storage.db`.

**Causa**: Outro processo está usando o banco ou processo anterior não finalizou corretamente.

**Solução**:

```bash
# Verificar processos Python rodando
ps aux | grep python

# Matar processos se necessário
pkill -f "python.*aula11"

# Limpar arquivo de lock
rm -f .chromadb/*.db-wal
rm -f .chromadb/*.db-shm
```

### Problema: Banco de dados corrompido

**Sintoma**: Erros estranhos ao acessar memory.

**Solução**: Recriar banco de dados:

```bash
rm -f .chromadb/long_term_memory_storage.db
rm -f .chromadb/*.db-wal
rm -f .chromadb/*.db-shm
uv run main.py  # Recria automaticamente
```

## 🐛 Problemas Gerais

### Problema: Script não executa

**Verificar Python e UV**:

```bash
uv --version
python --version
```

**Reinstalar dependências**:

```bash
uv sync
```

### Problema: Erro "Module not found"

**Solução**: Verificar se está executando do diretório correto:

```bash
# Deve estar em: /home/lotus/supra/curso_crewai/
pwd

# Executar com uv run
uv run aula11/main.py
```

### Problema: Verbose=True não mostra detalhes

**Causa**: Output pode estar sendo redirecionado.

**Solução**: Forçar output para stdout:

```python
import sys

# No início do script
sys.stdout.flush()
sys.stderr.flush()

# Executar crew
resultado = crew.kickoff()
print(resultado, flush=True)
```

## 📊 Problemas de Performance

### Problema: Execução muito lenta

**Causas possíveis**:

1. **Primeira execução**: Embeddings sendo criados (normal)
2. **Documentos grandes**: Processar PDFs grandes leva tempo
3. **Muitos documentos**: Múltiplas knowledge sources

**Otimizações**:

```python
# 1. Usar modelo de embedding mais rápido
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2. Processar documentos em lote
# (já implementado automaticamente)

# 3. Limitar tamanho de contexto
task = Task(
    description="...",
    expected_output="Máximo 200 palavras",  # Limitar output
    agent=agent
)
```

### Problema: Uso alto de memória RAM

**Causa**: ChromaDB carrega embeddings em memória.

**Soluções**:

1. **Usar documentos menores**
2. **Processar um documento por vez**
3. **Limpar cache periodicamente**

```bash
# Limpar cache entre execuções
rm -rf .chromadb/
```

## 🔄 Reset Completo

Se nada funcionar, fazer reset completo:

```bash
cd aula11

# 1. Limpar todo storage
rm -rf .chromadb/
rm -f chromadb-*.lock

# 2. Reinstalar dependências
cd ..
uv sync

# 3. Reconfigurar API keys
uv run configurar-crewai

# 4. Testar exemplo simples
uv run aula11/exemplos/01_memory_basico.py
```

## 📞 Suporte Adicional

Se o problema persistir:

1. **Verificar logs**: Ativar `verbose=True` em todos os agentes
2. **Testar exemplo mínimo**: Executar `exemplos/01_memory_basico.py`
3. **Documentação oficial**: <https://docs.crewai.com/concepts/memory>
4. **Verificar versões**:

```bash
uv run python -c "import crewai; print(crewai.__version__)"
uv run python -c "import chromadb; print(chromadb.__version__)"
```

---

**Lembre-se**: A maioria dos problemas é resolvida com `rm -rf .chromadb/` e reexecução! 🚀
