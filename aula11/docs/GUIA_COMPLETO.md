# 📚 Guia Completo de RAG (Retrieval-Augmented Generation)

## O Que é RAG?

**RAG** = **R**etrieval **A**ugmented **G**eneration

É uma técnica que combina:

1. **Retrieval** (Recuperação) - Buscar informações relevantes
2. **Augmented** (Aumentado) - Adicionar informações ao contexto
3. **Generation** (Geração) - LLM gera resposta baseada no contexto enriquecido

## Por Que Usar RAG?

### ❌ Problemas sem RAG

**LLM sozinho:**

- ❌ Conhecimento limitado à data de treino
- ❌ Pode "alucinar" (inventar informações)
- ❌ Não tem acesso a dados proprietários
- ❌ Não se atualiza automaticamente
- ❌ Não cita fontes

**Exemplo:**

```python
User: "Qual o protocolo de triagem de 2024?"
LLM: "Baseado no meu conhecimento até 2023..." # ❌ Desatualizado!
```

### ✅ Vantagens com RAG

**LLM + RAG:**

- ✅ Acessa informações atualizadas
- ✅ Consulta documentos proprietários
- ✅ Cita fontes específicas
- ✅ Reduz alucinações
- ✅ Conhecimento pode ser atualizado sem retreinar

**Exemplo:**

```python
User: "Qual o protocolo de triagem de 2024?"
↓
Sistema busca: "protocolo_triagem_2024.pdf"
↓
LLM: "Segundo o protocolo de 2024 (pág. 5)..." # ✅ Fundamentado!
```

## Como Funciona RAG no CrewAI?

### Fluxo Completo

```text
1. USUÁRIO faz pergunta
   ↓
2. QUERY é convertida em EMBEDDING
   ↓
3. BUSCA SEMÂNTICA nos documentos (ChromaDB)
   ↓
4. DOCUMENTOS RELEVANTES são recuperados
   ↓
5. CONTEXTO é montado (query + documentos)
   ↓
6. LLM recebe contexto ENRIQUECIDO
   ↓
7. RESPOSTA é gerada baseada em FONTES
```

### Componentes do RAG no CrewAI

#### 1. Memory System

**Tipos de Memória:**

| Memória | Storage | Propósito | Exemplo |
|---------|---------|-----------|---------|
| **Short-Term** | ChromaDB | Contexto da conversa atual | "Você mencionou febre há 2 msgs" |
| **Long-Term** | SQLite | Histórico entre sessões | "Última consulta: 15/10/2024" |
| **Entity** | ChromaDB | Informações sobre entidades | "João, 30 anos, hipertenso" |

**Habilitação:**

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,  # ✨ Habilita todas as memórias!
    verbose=True
)
```

#### 2. Knowledge Sources

**Tipos Suportados:**

- 📄 **Texto**: `.txt`
- 📕 **PDF**: `.pdf`
- 📊 **Planilhas**: `.csv`, `.xlsx`
- 🗂️ **Dados**: `.json`
- 🌐 **Web**: URLs
- 💬 **String**: Texto direto no código

**Uso:**

```python
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

protocolos = PDFKnowledgeSource(
    file_paths=["protocolos/triagem_2024.pdf"]
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    knowledge_sources=[protocolos],  # 📚 Acesso aos PDFs!
    verbose=True
)
```

#### 3. Embeddings (Opcional - Aula 10)

Para busca semântica customizada:

```python
from openai import OpenAI

client = OpenAI()
embedding = client.embeddings.create(
    input="dor de cabeça",
    model="text-embedding-3-small"
)

# Buscar sintomas similares semanticamente
```

## Arquitetura RAG Típica

### Sistema Básico (Memory + Knowledge)

```python
from crewai import Agent, Task, Crew, LLM
from crewai.knowledge.source.text_file_knowledge_source import (
    TextFileKnowledgeSource
)

llm = LLM(model="gpt-4o-mini")

# Knowledge base
protocolos = TextFileKnowledgeSource(
    file_paths=["protocolos/urgencia.txt"]
)

# Agente
agente = Agent(
    role="Médico Virtual",
    goal="Atender baseado em protocolos atualizados",
    backstory="Médico com acesso a protocolos e memória perfeita.",
    llm=llm
)

tarefa = Task(
    description="Atenda o paciente: {caso}",
    expected_output="Diagnóstico e orientações",
    agent=agente
)

# Crew com RAG
crew = Crew(
    agents=[agente],
    tasks=[tarefa],
    memory=True,  # 🧠 Memória
    knowledge_sources=[protocolos],  # 📚 Conhecimento
    verbose=True
)

resultado = crew.kickoff(inputs={"caso": "dor no peito há 1h"})
```

### Sistema Avançado (Multi-Agente + RAG)

```python
# Múltiplos agentes colaborando com RAG

# AGENTE 1: Coleta (com memória)
recepcionista = Agent(
    role="Recepcionista",
    goal="Coletar informações",
    backstory="Lembra de todos os pacientes.",
    llm=llm
)

# AGENTE 2: Triagem (com conhecimento)
triagista = Agent(
    role="Triagista",
    goal="Classificar urgência",
    backstory="Consulta protocolos oficiais.",
    llm=llm
)

# AGENTE 3: Encaminhamento
coordenador = Agent(
    role="Coordenador",
    goal="Recomendar unidade",
    backstory="Conhece toda a rede de saúde.",
    llm=llm
)

# Tasks com context
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

## Boas Práticas RAG

### ✅ DO (Faça)

#### 1. Estruture Bem o Conhecimento

```python
# ✅ BOM: Documentos bem organizados
conhecimento_medico/
├── protocolos/
│   ├── triagem_2024.pdf
│   ├── urgencia_emergencia.txt
│   └── primeiros_socorros.pdf
├── medicamentos/
│   ├── antibioticos.csv
│   └── analgesicos.json
└── estabelecimentos/
    └── capacidade_atendimento.xlsx
```

#### 2. Use Knowledge Sources Apropriadas

```python
# ✅ BOM: Tipo certo para cada dado
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource

protocolos = PDFKnowledgeSource(file_paths=["triagem.pdf"])
medicamentos = CSVKnowledgeSource(file_paths=["remedios.csv"])
```

#### 3. Combine Memory e Knowledge Estrategicamente

```python
# ✅ BOM: Usa memory para histórico, knowledge para regras
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,  # Lembrar do paciente
    knowledge_sources=[protocolos],  # Consultar regras atualizadas
    verbose=True
)
```

#### 4. Dê Contexto Claro aos Agentes

```python
# ✅ BOM: Backstory menciona acesso ao conhecimento
agent = Agent(
    role="Triagista",
    goal="Classificar urgência",
    backstory="""Enfermeiro especializado que SEMPRE consulta
    os protocolos oficiais antes de classificar.""",
    llm=llm
)
```

### ❌ DON'T (Evite)

#### 1. Documentos Desorganizados

```python
# ❌ RUIM: Arquivos misturados sem estrutura
arquivos/
├── doc1.pdf
├── random_stuff.txt
├── old_protocol_2020.pdf  # ❌ Versão antiga!
└── backup_copy_final_v3.pdf  # ❌ Duplicata!
```

#### 2. Knowledge Desnecessária

```python
# ❌ RUIM: Carregar TODO o conhecimento quando só precisa de parte
protocolos_todos = PDFKnowledgeSource(file_paths=[
    "proto1.pdf", "proto2.pdf", ... "proto999.pdf"  # ❌ Muito!
])

# ✅ BOM: Apenas o necessário
proto_triagem = PDFKnowledgeSource(file_paths=["triagem.pdf"])
```

#### 3. Confundir Memory com Knowledge

```python
# ❌ RUIM: Usar memory para armazenar regras
# Memory é para HISTÓRICO, não para DOCUMENTAÇÃO

# ✅ BOM: Knowledge para regras, Memory para histórico
crew = Crew(
    memory=True,  # Histórico de pacientes
    knowledge_sources=[regras],  # Protocolos fixos
)
```

## Otimização de RAG

### 1. Chunking (Divisão de Documentos)

```python
# Para documentos muito grandes, divida em chunks
# CrewAI faz isso automaticamente, mas você pode controlar:

from crewai.knowledge.source.text_file_knowledge_source import (
    TextFileKnowledgeSource
)

# Documento será dividido em chunks menores automaticamente
doc_grande = TextFileKnowledgeSource(
    file_paths=["manual_completo_500_paginas.txt"]
)
```

### 2. Cache de Embeddings

```python
# CrewAI cacheia embeddings automaticamente em ChromaDB
# Primeira vez: cria embeddings (demora)
# Próximas vezes: usa cache (rápido!)

# Localização do cache:
from crewai.utilities.paths import db_storage_path
print(f"Cache em: {db_storage_path()}")
```

### 3. Limitar Contexto

```python
# Evite sobrecarregar o contexto do LLM
# Use agentes especializados para tipos específicos de conhecimento

# ❌ RUIM: Um agente com TODO o conhecimento
agente_geral = Agent(
    knowledge=Knowledge(sources=[
        proto1, proto2, proto3, ... # Muito contexto!
    ])
)

# ✅ BOM: Agentes especializados
agente_triagem = Agent(knowledge=Knowledge(sources=[proto_triagem]))
agente_medicamentos = Agent(knowledge=Knowledge(sources=[lista_remedios]))
```

## Troubleshooting RAG

### Problema 1: "Agente não consulta knowledge"

**Sintoma:** Agente responde sem usar documentos

**Solução:**

```python
# 1. Verificar se knowledge está configurado
crew = Crew(
    knowledge_sources=[source],  # ✅ Está aqui?
    verbose=True  # Ver logs
)

# 2. Backstory deve mencionar consulta
agent = Agent(
    backstory="SEMPRE consulta protocolos..."  # ✅ Explícito!
)

# 3. Task deve pedir consulta
task = Task(
    description="Consulte os protocolos e classifique..."  # ✅ Direto!
)
```

### Problema 2: "Memory não funciona"

**Sintoma:** Agente não lembra de conversas anteriores

**Solução:**

```python
# 1. Verificar se memory está habilitada
crew = Crew(
    memory=True,  # ✅ Deve ser True!
    verbose=True
)

# 2. Verificar storage path
from crewai.utilities.paths import db_storage_path
print(f"Storage: {db_storage_path()}")  # Existe?

# 3. Limpar cache se necessário
# rm -rf ~/.local/share/CrewAI/{projeto}/
```

### Problema 3: "Respostas genéricas"

**Sintoma:** LLM responde sem usar fontes

**Solução:**

```python
# 1. Pedir explicitamente para citar fontes
task = Task(
    description="""Classifique E cite o protocolo usado.
    Formato: "Segundo protocolo X, página Y..."
    """
)

# 2. Usar temperature baixo para seguir documentos
llm = LLM(model="gpt-4o-mini", temperature=0.1)  # ✅ Mais determinístico
```

## Casos de Uso RAG

### 1. Chatbot de Atendimento

```python
# Atendente que lembra + consulta FAQ
crew = Crew(
    agents=[atendente],
    tasks=[responder],
    memory=True,  # Lembrar do cliente
    knowledge_sources=[faq_pdf],  # Consultar perguntas frequentes
)
```

### 2. Sistema de Triagem Médica

```python
# Triagem que consulta protocolos + lembra histórico
crew = Crew(
    agents=[triagista],
    tasks=[classificar],
    memory=True,  # Histórico do paciente
    knowledge_sources=[protocolos],  # Protocolos de Manchester
)
```

### 3. Assistente de Pesquisa

```python
# Pesquisador que consulta papers + mantém contexto
crew = Crew(
    agents=[pesquisador],
    tasks=[analisar],
    memory=True,  # Lembrar análises anteriores
    knowledge_sources=[papers_pdf],  # Artigos científicos
)
```

## Métricas de Sucesso RAG

### Como Saber Se Seu RAG Está Funcionando?

1. **✅ Respostas fundamentadas em fontes**
   - Agente cita documentos específicos
   - Menciona páginas/seções relevantes

2. **✅ Contexto mantido entre conversas**
   - Lembra de interações anteriores
   - Faz referência ao histórico

3. **✅ Redução de alucinações**
   - Informações verificáveis nos documentos
   - Admite quando não sabe

4. **✅ Respostas atualizadas**
   - Usa informações mais recentes
   - Não depende apenas do treino do LLM

## Resumo

**RAG = Retrieval + Augmented + Generation**

**No CrewAI:**

- 🧠 **Memory**: Lembrar histórico
- 📚 **Knowledge**: Consultar documentos
- 🔍 **Embeddings**: Busca semântica (opcional)
- 🤝 **Agentes**: Orquestrar tudo

**Quando usar:**

- ✅ Precisa de informações atualizadas
- ✅ Tem documentos proprietários
- ✅ Quer citar fontes
- ✅ Precisa de contexto entre sessões

**Evite:**

- ❌ Documentos desorganizados
- ❌ Knowledge desnecessária
- ❌ Confundir memory com knowledge

**Próximos passos:**

1. Execute os exemplos em `aula11/exemplos/`
2. Complete os exercícios em `aula11/exercicios/`
3. Experimente com seus próprios documentos!

---

**🎯 Agora você domina RAG com CrewAI!**
