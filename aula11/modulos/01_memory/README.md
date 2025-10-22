# 🧠 Módulo 1: Memory System

**Tempo estimado:** 45-60 minutos

## O Que Você Vai Aprender

✅ Como funciona o Memory System do CrewAI  
✅ Diferença entre agentes com e sem memória  
✅ 3 tipos de memória: Short-term, Long-term, Entity  
✅ Quando usar memória em seus projetos  

## Arquivos Deste Módulo

- `README.md` - Este arquivo
- `exemplo.py` - Demonstração prática
- `exercicio.py` - Exercício com gabarito

## Conceito: Memory System

### O Problema

```python
# SEM MEMÓRIA ❌
User: "Meu nome é João"
Bot: "Olá!"
User: "Qual meu nome?"
Bot: "Não sei" ❌
```

### A Solução

```python
# COM MEMÓRIA ✅
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True  # 🔑 Ativa memória!
)

User: "Meu nome é João"
Bot: "Prazer, João!"
User: "Qual meu nome?"
Bot: "João!" ✅
```

## 3 Tipos de Memória

### 1. Short-Term Memory (ChromaDB)

**O que é:** Contexto da conversa atual  
**Quando usar:** Chat, conversas, contexto imediato  
**Exemplo:**

```python
User: "Tenho dor de cabeça"
Bot: "Que tipo de dor?"
User: "Latejante"
Bot: [lembra: dor latejante]
```

### 2. Long-Term Memory (SQLite)

**O que é:** Histórico entre sessões  
**Quando usar:** Dados persistentes, aprendizado contínuo  
**Exemplo:**

```python
# Sessão 1
User: "Sou alérgico a penicilina"
Bot: "Registrado!"

# Sessão 2 (dias depois)
Bot: "Vejo que você é alérgico a penicilina"
```

### 3. Entity Memory (ChromaDB)

**O que é:** Informações sobre entidades específicas  
**Quando usar:** Perfis, relacionamentos, atributos  
**Exemplo:**

```python
Bot armazena sobre "João":
- Nome: João Silva
- Idade: 35 anos
- Alergia: Penicilina
- Última visita: 10/10/2025
```

## Como Executar

### 1. Exemplo Prático

```bash
cd modulos/01_memory
uv run exemplo.py
```

**O que mostra:**
- Agente SEM memória (esquece tudo)
- Agente COM memória (lembra contexto)
- Informações do storage

**Tempo:** ~15 minutos

### 2. Exercício

```bash
uv run exercicio.py
```

**Objetivo:** Criar chatbot que lembra do paciente

**Gabarito:** Incluído no arquivo

**Tempo:** ~30 minutos

## Código Mínimo

```python
from crewai import Agent, Task, Crew, LLM

llm = LLM(model="gpt-4o-mini")

agent = Agent(
    role="Atendente",
    goal="Conversar lembrando do paciente",
    backstory="Atendente com memória perfeita.",
    llm=llm
)

task = Task(
    description="Converse: {mensagem}",
    expected_output="Resposta contextualizada",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True  # 🔑 MEMORY ATIVADO
)

# Primeira interação
r1 = crew.kickoff(inputs={"mensagem": "Meu nome é Ana"})

# Segunda interação - vai lembrar!
r2 = crew.kickoff(inputs={"mensagem": "Qual meu nome?"})
```

## Quando Usar Memory

### ✅ Use Memory Quando

- Chatbots conversacionais
- Assistentes pessoais
- Sistemas de atendimento
- Histórico é importante
- Contexto entre interações

### ❌ Não Use Memory Quando

- Tarefas isoladas/únicas
- Processos batch sem contexto
- Privacy/LGPD exige esquecimento
- Performance crítica (overhead)

## Verificar Storage

```python
from crewai.utilities.paths import db_storage_path
print(db_storage_path())  # Ver onde está armazenado
```

## Limpar Storage

```bash
# CUIDADO: Deleta TODA a memória!
rm -rf ~/.local/share/aula11/
```

## Próximos Passos

Após dominar Memory:

1. **Módulo 2:** Knowledge Sources
2. **Módulo 3:** RAG Avançado (Memory + Knowledge)

## Troubleshooting

**Problema:** Memory não funciona  
**Solução:** Verificar se `memory=True` na Crew

**Problema:** Storage muito grande  
**Solução:** Limpar periodicamente

**Problema:** Lentidão  
**Solução:** Memory adiciona overhead, normal em primeiras chamadas

---

**📚 Ver também:**
- [GUIA_COMPLETO.md](../../docs/GUIA_COMPLETO.md)
- [Quick Start](../../QUICK_START.md)
