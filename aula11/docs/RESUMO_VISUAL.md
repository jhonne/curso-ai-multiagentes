# 📊 Resumo Visual - Aula 11: RAG com CrewAI

## O Que É RAG?

```text
┌─────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM                          │
│                                                             │
│  ┌─────────┐     ┌──────────┐     ┌──────────────────┐    │
│  │ Pergunta│ --> │  Busca   │ --> │  Documentos      │    │
│  │ Usuário │     │ Semântica│     │  Relevantes      │    │
│  └─────────┘     └──────────┘     └──────────────────┘    │
│                                             │               │
│                                             v               │
│                                    ┌────────────────┐       │
│                                    │  LLM com       │       │
│                                    │  Contexto      │       │
│                                    │  Enriquecido   │       │
│                                    └────────────────┘       │
│                                             │               │
│                                             v               │
│                                    ┌────────────────┐       │
│                                    │   Resposta     │       │
│                                    │  Fundamentada  │       │
│                                    └────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Componentes do RAG no CrewAI

### Memory System

```text
┌─────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🧠 SHORT-TERM (ChromaDB)                              │
│  ├─ Conversa atual                                     │
│  ├─ Contexto imediato                                  │
│  └─ Embeddings temporários                             │
│                                                         │
│  💾 LONG-TERM (SQLite)                                 │
│  ├─ Histórico entre sessões                            │
│  ├─ Aprendizado persistente                            │
│  └─ Dados estruturados                                 │
│                                                         │
│  👤 ENTITY (ChromaDB)                                  │
│  ├─ Informações sobre pessoas                          │
│  ├─ Contexto sobre entidades                           │
│  └─ Relações e atributos                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Knowledge Sources

```text
┌─────────────────────────────────────────────────────────┐
│                 KNOWLEDGE SOURCES                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📄 TEXT (.txt)                                        │
│  └─ TextFileKnowledgeSource                            │
│                                                         │
│  📕 PDF (.pdf)                                         │
│  └─ PDFKnowledgeSource                                 │
│                                                         │
│  📊 CSV (.csv)                                         │
│  └─ CSVKnowledgeSource                                 │
│                                                         │
│  🗂️  JSON (.json)                                     │
│  └─ JSONKnowledgeSource                                │
│                                                         │
│  📈 EXCEL (.xlsx)                                      │
│  └─ ExcelKnowledgeSource                               │
│                                                         │
│  🌐 WEB (URLs)                                         │
│  └─ WebKnowledgeSource                                 │
│                                                         │
│  💬 STRING (texto direto)                              │
│  └─ StringKnowledgeSource                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Arquitetura de Sistema RAG

### Sistema Básico

```text
┌────────────────────────────────────────────────┐
│              SISTEMA BÁSICO                    │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────┐                                 │
│  │  Agente  │ <--- LLM (gpt-4o-mini)          │
│  └──────────┘                                 │
│       │                                        │
│       ├─── Memory: True                       │
│       │     └─ Short/Long/Entity              │
│       │                                        │
│       └─── Knowledge Sources                  │
│             └─ protocolos.txt                 │
│                                                │
│  ┌──────────┐                                 │
│  │  Tarefa  │                                 │
│  └──────────┘                                 │
│       │                                        │
│  ┌──────────┐                                 │
│  │   Crew   │                                 │
│  └──────────┘                                 │
│                                                │
└────────────────────────────────────────────────┘
```

### Sistema Multi-Agente

```text
┌──────────────────────────────────────────────────────────┐
│           SISTEMA MULTI-AGENTE COMPLETO                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  AGENTE 1: Recepcionista                                │
│  ├─ Role: Coletar informações                           │
│  ├─ Memory: Lembra pacientes anteriores                 │
│  └─ Knowledge: FAQ básico                               │
│           │                                              │
│           v                                              │
│  AGENTE 2: Triagista                                    │
│  ├─ Role: Classificar urgência                          │
│  ├─ Memory: Histórico de classificações                 │
│  └─ Knowledge: Protocolos Manchester                    │
│           │                                              │
│           v                                              │
│  AGENTE 3: Coordenador                                  │
│  ├─ Role: Encaminhar paciente                           │
│  ├─ Memory: Capacidade das unidades                     │
│  └─ Knowledge: Rede de atendimento                      │
│           │                                              │
│           v                                              │
│  ┌────────────────────┐                                 │
│  │  Resultado Final   │                                 │
│  │  - Classificação   │                                 │
│  │  - Recomendação    │                                 │
│  │  - Justificativa   │                                 │
│  └────────────────────┘                                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Fluxo de Execução

### Exemplo 1: Memory Básico

```text
SEM MEMÓRIA:
User: "Meu nome é João"
Bot: "Olá! Como posso ajudar?"
User: "Qual meu nome?"
Bot: "Desculpe, não sei." ❌

COM MEMÓRIA:
User: "Meu nome é João"
Bot: "Prazer, João! Como posso ajudar?"
User: "Qual meu nome?"
Bot: "Seu nome é João!" ✅
```

### Exemplo 2: Knowledge Source

```text
SEM KNOWLEDGE:
User: "Dor no peito há 1h"
Bot: "Procure um médico." (genérico) ❌

COM KNOWLEDGE:
User: "Dor no peito há 1h"
Bot: "Segundo protocolo Manchester: VERMELHO
     Atendimento imediato.
     Possível IAM." ✅
```

### Exemplo 3: RAG Completo

```text
COMBINANDO MEMORY + KNOWLEDGE:

User: "Meu nome é João, 45 anos"
Bot: [MEMORY] "Registrado: João, 45 anos" ✅

User: "Dor no peito há 1h"
Bot: [KNOWLEDGE] Consulta protocolos
     [MEMORY] Lembra: João, 45 anos
     Resposta: "João, sua idade (45) é fator
     agravante. Classificação VERMELHO.
     Procure emergência imediatamente!" ✅
```

## Comparação: Antes vs Depois do RAG

### Antes (LLM Sozinho)

```text
❌ Conhecimento limitado (treino até data X)
❌ Não acessa documentos proprietários
❌ Inventa informações (alucinação)
❌ Não lembra conversas anteriores
❌ Não cita fontes
```

### Depois (LLM + RAG)

```text
✅ Acessa conhecimento atualizado
✅ Consulta documentos proprietários
✅ Respostas fundamentadas em fontes
✅ Lembra contexto de conversas
✅ Cita protocolos específicos
```

## Casos de Uso

### 1. Chatbot de Atendimento

```text
┌─────────────────────────────────┐
│     CHATBOT ATENDIMENTO         │
├─────────────────────────────────┤
│ Memory:                         │
│ ├─ Lembra cliente               │
│ └─ Histórico de tickets         │
│                                 │
│ Knowledge:                      │
│ ├─ FAQ.pdf                      │
│ ├─ Manuais.txt                  │
│ └─ Políticas.json               │
│                                 │
│ Resultado:                      │
│ └─ Atendimento personalizado    │
│    com respostas precisas       │
└─────────────────────────────────┘
```

### 2. Sistema de Triagem Médica

```text
┌─────────────────────────────────┐
│     TRIAGEM MÉDICA              │
├─────────────────────────────────┤
│ Memory:                         │
│ ├─ Histórico do paciente        │
│ └─ Consultas anteriores         │
│                                 │
│ Knowledge:                      │
│ ├─ Protocolo Manchester         │
│ ├─ Medicamentos.csv             │
│ └─ Contraindicações.json        │
│                                 │
│ Resultado:                      │
│ └─ Classificação fundamentada   │
│    em protocolos oficiais       │
└─────────────────────────────────┘
```

### 3. Assistente de Pesquisa

```text
┌─────────────────────────────────┐
│     ASSISTENTE PESQUISA         │
├─────────────────────────────────┤
│ Memory:                         │
│ ├─ Análises anteriores          │
│ └─ Contexto da pesquisa         │
│                                 │
│ Knowledge:                      │
│ ├─ Papers científicos.pdf       │
│ ├─ Datasets.csv                 │
│ └─ Metodologias.txt             │
│                                 │
│ Resultado:                      │
│ └─ Análise baseada em           │
│    literatura científica        │
└─────────────────────────────────┘
```

## Métricas de Sucesso

### KPIs de RAG

```text
┌─────────────────────────────────────────────┐
│         MÉTRICAS DE SUCESSO                 │
├─────────────────────────────────────────────┤
│                                             │
│  ✅ Citação de Fontes                      │
│     └─ % respostas com referências         │
│                                             │
│  ✅ Contexto Mantido                       │
│     └─ % conversas contextualizadas        │
│                                             │
│  ✅ Redução de Alucinações                 │
│     └─ % informações verificáveis          │
│                                             │
│  ✅ Satisfação do Usuário                  │
│     └─ Score de relevância                 │
│                                             │
│  ✅ Tempo de Resposta                      │
│     └─ Latência média                      │
│                                             │
└─────────────────────────────────────────────┘
```

## Estrutura dos Arquivos da Aula

```text
aula11/
├── 📖 README.md              # Documentação principal
├── 📚 GUIA_RAG.md            # Conceitos detalhados
├── 🚀 INSTRUCOES_EXECUCAO.md # Como executar
├── 📊 RESUMO_VISUAL.md       # Este arquivo
│
├── 🎯 main.py                # Sistema interativo
│
├── 📁 exemplos/
│   ├── 01_memory_basico.py
│   ├── 02_knowledge_pdf.py
│   ├── 03_rag_simples.py
│   └── 04_sistema_completo.py
│
├── 📝 exercicios/
│   ├── exercicio1_chatbot_memoria.py
│   ├── exercicio2_knowledge_base.py
│   └── exercicio3_rag_completo.py
│
├── 📚 conhecimento_medico/
│   └── protocolos/
│       └── urgencia_emergencia.txt
│
└── 🛠️ utils/
    ├── __init__.py
    ├── rag_helper.py
    └── knowledge_loader.py
```

## Progressão de Aprendizado

```text
┌────────────────────────────────────────────────┐
│         JORNADA DE APRENDIZADO                 │
├────────────────────────────────────────────────┤
│                                                │
│  NÍVEL 1: Fundamentos (Exemplos 1-2)          │
│  ├─ Memory System                             │
│  └─ Knowledge Sources                         │
│                                                │
│  NÍVEL 2: Integração (Exemplo 3)              │
│  └─ RAG Básico (Memory + Knowledge)           │
│                                                │
│  NÍVEL 3: Avançado (Exemplo 4)                │
│  └─ Sistema Multi-Agente Completo             │
│                                                │
│  NÍVEL 4: Prática (Exercícios)                │
│  ├─ Exercício 1: Chatbot                      │
│  ├─ Exercício 2: Knowledge Base               │
│  └─ Exercício 3: RAG Completo                 │
│                                                │
│  NÍVEL 5: Maestria                            │
│  └─ Seus próprios projetos RAG!               │
│                                                │
└────────────────────────────────────────────────┘
```

## Comandos Rápidos

```bash
# Executar sistema interativo
cd aula11 && uv run main.py

# Executar exemplo específico
cd aula11/exemplos && uv run 01_memory_basico.py

# Fazer exercício
cd aula11/exercicios && uv run exercicio1_chatbot_memoria.py

# Verificar storage
cd aula11 && python -c "from utils.rag_helper import verificar_storage; verificar_storage()"

# Limpar storage
cd aula11 && python -c "from utils.rag_helper import limpar_storage; limpar_storage()"
```

## Checklist de Estudo

```text
□ Ler README.md
□ Ler GUIA_RAG.md
□ Executar main.py (menu interativo)
□ Exemplo 1: Memory básico
□ Exemplo 2: Knowledge sources
□ Exemplo 3: RAG simples
□ Exemplo 4: Sistema completo
□ Exercício 1: Chatbot
□ Exercício 2: Knowledge base
□ Exercício 3: RAG completo
□ Criar seu próprio projeto RAG
```

---

**🎯 Visualização completa da Aula 11! Agora é praticar!**
