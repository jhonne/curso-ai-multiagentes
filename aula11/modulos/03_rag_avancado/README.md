# 🚀 Módulo 3: RAG Avançado

**Tempo estimado:** 60-90 minutos

## O Que Você Vai Aprender

✅ Combinar Memory + Knowledge = RAG  
✅ Sistemas multi-agente com RAG  
✅ Integração com embeddings (Aula 10)  
✅ RAG pronto para produção  

## Arquivos Deste Módulo

- `README.md` - Este arquivo
- `03_rag_simples.py` - RAG básico
- `exemplo_multiagent.py` - Sistema com 3 agentes
- `exercicio.py` - RAG completo (com gabarito)

## Conceito: RAG = Memory + Knowledge

### Evolução

```text
BÁSICO          INTERMEDIÁRIO       AVANÇADO
   ↓                  ↓                 ↓
Memory          Knowledge          RAG Completo
(lembra)        (consulta)      (lembra + consulta)
```

### O Poder do RAG

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,              # 🧠 Lembra do usuário
    knowledge_sources=[docs]  # 📚 Consulta documentos
)

# Resultado: Respostas personalizadas E fundamentadas!
```

## Exemplos Progressivos

### 1. RAG Simples (03_rag_simples.py)

**O que é:** Memory + Knowledge básico

```bash
uv run 03_rag_simples.py
```

**Demonstra:**
- Consulta única com RAG
- Conversa contextual
- Como combinar ambos recursos

**Tempo:** ~20 min

### 2. Sistema Multi-Agente (exemplo_multiagent.py)

**O que é:** 3 agentes colaborando com RAG

```bash
uv run exemplo_multiagent.py
```

**Arquitetura:**

```text
┌─────────────────────────────────────────┐
│         SISTEMA COMPLETO                │
├─────────────────────────────────────────┤
│                                         │
│  AGENTE 1: Recepcionista                │
│  ├─ Memory: Lembra pacientes            │
│  └─ Knowledge: FAQ básico               │
│           │                             │
│           v                             │
│  AGENTE 2: Triagista                    │
│  ├─ Memory: Histórico                   │
│  └─ Knowledge: Protocolos               │
│           │                             │
│           v                             │
│  AGENTE 3: Coordenador                  │
│  ├─ Memory: Capacidade                  │
│  └─ Knowledge: Rede                     │
│                                         │
└─────────────────────────────────────────┘
```

**Tempo:** ~30 min

### 3. Exercício Completo (exercicio.py)

**Objetivo:** Criar sistema RAG production-ready

```bash
uv run exercicio.py
```

**Inclui:**
- 3 agentes especializados
- Memory configurado
- Knowledge organizado
- TODOs para completar
- Gabarito incluído

**Tempo:** ~40 min

## Código: RAG Simples

```python
from crewai import Agent, Task, Crew, LLM
from crewai.knowledge.source.string_knowledge_source import (
    StringKnowledgeSource
)

# Knowledge
protocolo = """
VERMELHO: Dor torácica + idade >40
LARANJA: Dor torácica + idade <40
"""
knowledge = StringKnowledgeSource(content=protocolo)

# Agente
llm = LLM(model="gpt-4o-mini")
agent = Agent(
    role="Triagista",
    goal="Classificar com memória e protocolo",
    backstory="Combina histórico com protocolos.",
    llm=llm
)

# Crew com RAG
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,                    # 🧠 Memory
    knowledge_sources=[knowledge]   # 📚 Knowledge
)

# Interação 1: Registra dados
r1 = crew.kickoff(inputs={"msg": "Carlos, 45 anos"})

# Interação 2: Usa memory + knowledge!
r2 = crew.kickoff(inputs={"msg": "Dor no peito"})
# Resultado: "Carlos (45 anos) = VERMELHO por protocolo"
```

## Código: Multi-Agente

```python
# 3 Agentes especializados
recepcionista = Agent(
    role="Recepcionista",
    goal="Coletar informações",
    backstory="Lembra de todos os pacientes."
)

triagista = Agent(
    role="Triagista",
    goal="Classificar urgência",
    backstory="Consulta protocolos oficiais."
)

coordenador = Agent(
    role="Coordenador",
    goal="Encaminhar paciente",
    backstory="Conhece toda a rede."
)

# Tarefas com contexto
coleta = Task(description="Colete dados", agent=recepcionista)
classificacao = Task(description="Classifique", agent=triagista, context=[coleta])
encaminhamento = Task(description="Encaminhe", agent=coordenador, context=[coleta, classificacao])

# Crew completa
crew = Crew(
    agents=[recepcionista, triagista, coordenador],
    tasks=[coleta, classificacao, encaminhamento],
    memory=True,
    knowledge_sources=[protocolos],
    process=Process.sequential
)
```

## Integração com Aula 10 (Embeddings)

### Busca Semântica Customizada

```python
from openai import OpenAI

# Da Aula 10: Embeddings
client = OpenAI()

def buscar_similar(query, documentos):
    # Criar embedding da query
    query_emb = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    
    # Buscar docs similares
    # ... (código da Aula 10)
    
    return docs_relevantes

# Integrar com RAG
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,
    knowledge_sources=[knowledge],
    # + embeddings customizados para busca
)
```

## Boas Práticas RAG

### ✅ Arquitetura Recomendada

```python
# Agente especializado por função
recepcionista = Agent(memory=True)      # Dados do paciente
triagista = Agent(knowledge=[proto])    # Protocolos
coordenador = Agent(knowledge=[rede])   # Rede

# Tarefas com contexto
# Cada agente usa o que precisa
```

### ⚡ Otimizações

**Cache de Embeddings:**

```python
# CrewAI cacheia automaticamente em ChromaDB
# Primeira vez: lento (cria embeddings)
# Próximas: rápido (usa cache)
```

**Limitar Contexto:**

```python
# Não carregue tudo
knowledge = TextFileKnowledgeSource(
    file_paths=["protocolo_especifico.txt"]  # Apenas necessário
)
```

## Quando Usar RAG

### ✅ Casos de Uso Ideais

**Chatbot de Atendimento:**

```python
Memory: Lembra do cliente
Knowledge: FAQ, manuais
Resultado: Atendimento personalizado
```

**Sistema de Triagem:**

```python
Memory: Histórico do paciente
Knowledge: Protocolos médicos
Resultado: Classificação precisa
```

**Assistente de Pesquisa:**

```python
Memory: Análises anteriores
Knowledge: Papers científicos
Resultado: Análise fundamentada
```

### ❌ Quando NÃO Usar

- Tarefas batch simples
- Sem necessidade de contexto
- Performance crítica (real-time)
- Dados sensíveis (LGPD)

## Métricas de Sucesso

```text
✅ Citação de fontes
✅ Contexto mantido
✅ Redução de alucinações
✅ Respostas atualizadas
```

## Próximos Passos

### Deploy em Produção

1. **API REST:** Flask/FastAPI
2. **Frontend:** Streamlit/React
3. **Monitoring:** Logs de qualidade
4. **Cache:** Redis para performance
5. **Segurança:** Rate limiting, moderação

### Projetos Sugeridos

- Chatbot de suporte técnico
- Sistema de diagnóstico médico
- Assistente jurídico
- Analista financeiro
- Professor virtual

## Troubleshooting

**Problema:** RAG muito lento  
**Solução:** Limitar knowledge, usar cache

**Problema:** Respostas genéricas  
**Solução:** Backstory deve mencionar consulta, task pedir fontes

**Problema:** Memory demais  
**Solução:** Limpar storage periodicamente

---

**📚 Ver também:**
- [GUIA_COMPLETO.md](../../docs/GUIA_COMPLETO.md)
- [Módulo 1: Memory](../01_memory/README.md)
- [Módulo 2: Knowledge](../02_knowledge/README.md)
- [Aula 10: Embeddings](../../README.md#integração-com-aula-10)
