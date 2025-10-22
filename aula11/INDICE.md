# 📑 Índice Completo - Aula 11: RAG com CrewAI

## 🎯 Comece Aqui

**Novo na Aula 11?** Siga esta ordem:

1. **Leia primeiro**: [README.md](README.md) - Visão geral completa
2. **Aprofunde**: [GUIA_RAG.md](GUIA_RAG.md) - Conceitos detalhados
3. **Execute**: [INSTRUCOES_EXECUCAO.md](INSTRUCOES_EXECUCAO.md) - Como rodar
4. **Visualize**: [RESUMO_VISUAL.md](RESUMO_VISUAL.md) - Diagramas e esquemas

## 📚 Documentação

### Documentos Principais

| Arquivo | Propósito | Tamanho | Tempo de Leitura |
|---------|-----------|---------|------------------|
| [README.md](README.md) | Documentação completa da aula | ~25 KB | 20-30 min |
| [GUIA_RAG.md](GUIA_RAG.md) | Conceitos, boas práticas, troubleshooting | ~20 KB | 25-35 min |
| [INSTRUCOES_EXECUCAO.md](INSTRUCOES_EXECUCAO.md) | Como executar cada exemplo/exercício | ~10 KB | 10-15 min |
| [RESUMO_VISUAL.md](RESUMO_VISUAL.md) | Diagramas e visualizações | ~15 KB | 15-20 min |
| [INDICE.md](INDICE.md) | Este arquivo | ~5 KB | 5 min |

**Tempo total de leitura**: ~1h30min

## 💻 Código

### Sistema Principal

| Arquivo | Descrição | Linhas | Complexidade |
|---------|-----------|--------|--------------|
| [main.py](main.py) | Sistema interativo com menu | 464 | ⭐⭐⭐ Médio |

### Exemplos Progressivos

| # | Arquivo | O Que Ensina | Linhas | Nível |
|---|---------|--------------|--------|-------|
| 1 | [01_memory_basico.py](exemplos/01_memory_basico.py) | Memory System (com/sem) | 147 | ⭐ Básico |
| 2 | [02_knowledge_pdf.py](exemplos/02_knowledge_pdf.py) | Knowledge Sources | 195 | ⭐⭐ Básico+ |
| 3 | [03_rag_simples.py](exemplos/03_rag_simples.py) | RAG = Memory + Knowledge | 181 | ⭐⭐ Intermediário |
| 4 | [04_sistema_completo.py](exemplos/04_sistema_completo.py) | Sistema multi-agente | 256 | ⭐⭐⭐ Avançado |

**Tempo de execução**: ~15-30 min (todos os exemplos)

### Exercícios Práticos

| # | Arquivo | Desafio | Gabarito | Nível |
|---|---------|---------|----------|-------|
| 1 | [exercicio1_chatbot_memoria.py](exercicios/exercicio1_chatbot_memoria.py) | Chatbot com memória | ✅ Incluído | ⭐ Básico |
| 2 | [exercicio2_knowledge_base.py](exercicios/exercicio2_knowledge_base.py) | Consulta a protocolos | ✅ Incluído | ⭐⭐ Intermediário |
| 3 | [exercicio3_rag_completo.py](exercicios/exercicio3_rag_completo.py) | Sistema RAG completo | ✅ Incluído | ⭐⭐⭐ Avançado |

**Tempo estimado**: 2-3h (todos os exercícios)

### Utilitários (Utils)

| Arquivo | Funções Principais | Uso |
|---------|-------------------|-----|
| [__init__.py](utils/__init__.py) | Exports do módulo | Import automático |
| [rag_helper.py](utils/rag_helper.py) | `verificar_storage()`, `limpar_storage()`, `listar_knowledge_sources()` | Debug e gestão |
| [knowledge_loader.py](utils/knowledge_loader.py) | `criar_knowledge_automatico()`, `carregar_diretorio_completo()` | Carregar dados |

## 📊 Base de Conhecimento

### Dados Médicos

| Diretório | Arquivo | Conteúdo | Tamanho |
|-----------|---------|----------|---------|
| `conhecimento_medico/protocolos/` | [urgencia_emergencia.txt](conhecimento_medico/protocolos/urgencia_emergencia.txt) | Protocolos Manchester | ~1500 linhas |

**Uso**: Exemplos e exercícios usam estes dados para demonstrar RAG

## 🗂️ Estrutura Completa

```text
aula11/
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md                    ⭐ Comece aqui
│   ├── GUIA_RAG.md                  Conceitos detalhados
│   ├── INSTRUCOES_EXECUCAO.md       Como executar
│   ├── RESUMO_VISUAL.md             Diagramas
│   └── INDICE.md                    Este arquivo
│
├── 💻 CÓDIGO PRINCIPAL
│   └── main.py                      Sistema interativo
│
├── 📁 EXEMPLOS (4 arquivos)
│   ├── 01_memory_basico.py          Nível: ⭐
│   ├── 02_knowledge_pdf.py          Nível: ⭐⭐
│   ├── 03_rag_simples.py            Nível: ⭐⭐
│   └── 04_sistema_completo.py       Nível: ⭐⭐⭐
│
├── 📝 EXERCÍCIOS (3 arquivos)
│   ├── exercicio1_chatbot_memoria.py      ⭐
│   ├── exercicio2_knowledge_base.py       ⭐⭐
│   └── exercicio3_rag_completo.py         ⭐⭐⭐
│
├── 📚 CONHECIMENTO
│   └── conhecimento_medico/
│       └── protocolos/
│           └── urgencia_emergencia.txt
│
└── 🛠️ UTILITÁRIOS
    ├── __init__.py
    ├── rag_helper.py
    └── knowledge_loader.py
```

## 🚀 Guias de Execução Rápida

### Para Iniciantes

```bash
# 1. Ler documentação (30 min)
cat aula11/README.md

# 2. Executar sistema interativo
cd aula11
uv run main.py
# Escolha opção 6: "Testar todos os exemplos"

# 3. Fazer primeiro exercício
cd exercicios
uv run exercicio1_chatbot_memoria.py
```

### Para Intermediários

```bash
# 1. Ler guia avançado
cat aula11/GUIA_RAG.md

# 2. Executar exemplos individualmente
cd aula11/exemplos
uv run 01_memory_basico.py
uv run 02_knowledge_pdf.py
uv run 03_rag_simples.py
uv run 04_sistema_completo.py

# 3. Fazer todos os exercícios
cd ../exercicios
uv run exercicio1_chatbot_memoria.py
uv run exercicio2_knowledge_base.py
uv run exercicio3_rag_completo.py
```

### Para Avançados

```bash
# 1. Explorar código fonte
code aula11/

# 2. Experimentar com utils
cd aula11
python -c "from utils.rag_helper import verificar_storage; verificar_storage()"

# 3. Criar seu próprio RAG
# (Use exemplos como base e customize!)
```

## 📖 Glossário

| Termo | Significado |
|-------|-------------|
| **RAG** | Retrieval-Augmented Generation - Geração aumentada por recuperação |
| **Memory** | Sistema de memória do CrewAI (Short/Long/Entity) |
| **Knowledge** | Fontes de conhecimento (PDFs, TXTs, CSVs, etc.) |
| **Embedding** | Representação vetorial de texto (Aula 10) |
| **ChromaDB** | Banco vetorial para armazenar embeddings |
| **SQLite** | Banco relacional para memória de longo prazo |
| **Manchester** | Sistema de classificação de triagem médica |
| **Crew** | Equipe de agentes no CrewAI |
| **Agent** | Agente individual com role/goal/backstory |
| **Task** | Tarefa atribuída a um agente |

## 🎓 Trilha de Aprendizado

### Fase 1: Fundamentos (1-2h)

- ✅ Ler README.md
- ✅ Executar main.py (opção 1: Memory)
- ✅ Executar main.py (opção 2: Knowledge)
- ✅ Executar exemplo 01_memory_basico.py

**Objetivo**: Entender Memory e Knowledge separadamente

### Fase 2: Integração (1-2h)

- ✅ Executar exemplo 02_knowledge_pdf.py
- ✅ Executar exemplo 03_rag_simples.py
- ✅ Ler GUIA_RAG.md (seções 1-3)

**Objetivo**: Combinar Memory + Knowledge

### Fase 3: Complexidade (1-2h)

- ✅ Executar exemplo 04_sistema_completo.py
- ✅ Ler GUIA_RAG.md completo
- ✅ Estudar código dos exemplos

**Objetivo**: Sistema multi-agente com RAG

### Fase 4: Prática (2-3h)

- ✅ Exercício 1: Chatbot
- ✅ Exercício 2: Knowledge Base
- ✅ Exercício 3: RAG Completo

**Objetivo**: Aplicar conhecimento

### Fase 5: Maestria (Ilimitado)

- ✅ Criar seus próprios knowledge sources
- ✅ Desenvolver sistema RAG personalizado
- ✅ Integrar com Aula 10 (embeddings)
- ✅ Deploy em produção

**Objetivo**: Dominar RAG na prática

## 🔗 Links Úteis

### Documentação Oficial

- [CrewAI Docs](https://docs.crewai.com)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB](https://docs.trychroma.com)

### Aulas Relacionadas

- **Aula 10**: Embeddings e Similaridade Semântica
- **Aulas 1-4**: Fundamentos de agentes e crews
- **Aula 5**: Boas práticas e otimização

## 📊 Estatísticas da Aula

```text
┌──────────────────────────────────────┐
│      ESTATÍSTICAS AULA 11            │
├──────────────────────────────────────┤
│ 📄 Arquivos de documentação:      5  │
│ 💻 Exemplos progressivos:         4  │
│ 📝 Exercícios práticos:           3  │
│ 🛠️ Utilitários (utils):          3  │
│ 📚 Bases de conhecimento:         1  │
│                                      │
│ 📏 Total de linhas (código):  ~2500  │
│ 📖 Total de linhas (docs):    ~2000  │
│                                      │
│ ⏱️ Tempo estimado (completo):  8-10h │
└──────────────────────────────────────┘
```

## ✅ Checklist Completo

### Leitura

- [ ] README.md (~30 min)
- [ ] GUIA_RAG.md (~35 min)
- [ ] INSTRUCOES_EXECUCAO.md (~15 min)
- [ ] RESUMO_VISUAL.md (~20 min)

### Exemplos

- [ ] main.py - Sistema interativo
- [ ] 01_memory_basico.py
- [ ] 02_knowledge_pdf.py
- [ ] 03_rag_simples.py
- [ ] 04_sistema_completo.py

### Exercícios

- [ ] exercicio1_chatbot_memoria.py
- [ ] exercicio2_knowledge_base.py
- [ ] exercicio3_rag_completo.py

### Prática

- [ ] Criar seu próprio knowledge source
- [ ] Desenvolver chatbot personalizado
- [ ] Integrar com embeddings (Aula 10)

## 🎯 Próximos Passos

Após completar a Aula 11:

1. **Revisar Aula 10** - Integrar embeddings customizados
2. **Explorar produções** - Deploy de sistemas RAG
3. **Avançar para Aula 12** - [Tema futuro]
4. **Projetos pessoais** - Aplicar RAG em seus domínios

---

**🎓 Domine RAG com CrewAI! Boa jornada de aprendizado!**
