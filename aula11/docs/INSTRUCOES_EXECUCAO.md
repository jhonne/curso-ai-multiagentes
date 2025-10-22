# 🚀 Como Executar a Aula 11 - RAG com CrewAI

## Pré-requisitos

### 1. Dependências Instaladas

```bash
# Certifique-se que está no diretório raiz do projeto
cd /home/lotus/supra/curso_crewai

# Instalar/atualizar dependências
uv sync
```

### 2. API Key Configurada

```bash
# Verificar se .env existe com OPENAI_API_KEY
cat .env | grep OPENAI_API_KEY

# Se não existir, configurar:
uv run configurar-crewai
```

### 3. Testar Conexão

```bash
# Testar API OpenAI
uv run teste-api
```

## Executar os Exemplos

### Sistema Interativo Principal

```bash
cd aula11
uv run main.py
```

**Menu disponível:**

1. Demonstração Memory System
2. Demonstração Knowledge Sources
3. Sistema RAG Completo
4. Ver informações de storage
5. Limpar storage (cuidado!)
6. Testar todos os exemplos
7. Sair

### Exemplos Individuais

#### Exemplo 1: Memory Básico

```bash
cd aula11/exemplos
uv run 01_memory_basico.py
```

**O que faz:**

- Demonstra agente SEM memória (não lembra)
- Demonstra agente COM memória (lembra contexto)
- Mostra informações do storage

#### Exemplo 2: Knowledge Sources

```bash
uv run 02_knowledge_pdf.py
```

**O que faz:**

- Cria protocolo de triagem em arquivo
- Compara agente SEM knowledge (genérico)
- Compara agente COM knowledge (consulta protocolo)
- Testa múltiplos casos clínicos

#### Exemplo 3: RAG Simples

```bash
uv run 03_rag_simples.py
```

**O que faz:**

- Combina Memory + Knowledge
- Consulta única com contexto enriquecido
- Conversa contextual com histórico

#### Exemplo 4: Sistema Completo

```bash
uv run 04_sistema_completo.py
```

**O que faz:**

- Sistema multi-agente (3 agentes)
- Recepcionista (coleta dados)
- Triagista (classifica urgência)
- Coordenador (recomenda encaminhamento)
- Usa Memory + Knowledge integrados

## Fazer os Exercícios

### Exercício 1: Chatbot com Memória

```bash
cd aula11/exercicios
uv run exercicio1_chatbot_memoria.py
```

**Desafio:**

- Completar TODOs para criar chatbot
- Implementar memory system
- Testar conversação contextual

**Gabarito:** Dentro do próprio arquivo (comentado)

### Exercício 2: Base de Conhecimento

```bash
uv run exercicio2_knowledge_base.py
```

**Desafio:**

- Criar protocolo médico
- Configurar knowledge source
- Comparar agentes com/sem knowledge
- Testar 3 casos clínicos

**Gabarito:** Dentro do próprio arquivo (comentado)

### Exercício 3: RAG Completo

```bash
uv run exercicio3_rag_completo.py
```

**Desafio:**

- Implementar sistema completo
- 3 agentes especializados
- Memory + Knowledge integrados
- DESAFIO EXTRA: Integrar embeddings (Aula 10)

**Gabarito:** Dentro do próprio arquivo (comentado)

## Verificar Storage

### Ver Informações

```bash
cd aula11
python -c "from utils.rag_helper import verificar_storage; verificar_storage()"
```

### Ver Tamanho

```bash
python -c "from utils.rag_helper import tamanho_storage; print(f'{tamanho_storage():.2f} MB')"
```

### Limpar Storage (CUIDADO!)

```bash
python -c "from utils.rag_helper import limpar_storage; limpar_storage()"
```

## Usar Utils

### Exemplo de rag_helper

```python
from utils.rag_helper import (
    verificar_storage,
    verificar_knowledge_source,
    listar_knowledge_sources
)

# Ver storage
verificar_storage()

# Verificar arquivo específico
verificar_knowledge_source("conhecimento_medico/protocolos/urgencia_emergencia.txt")

# Listar todos os arquivos de conhecimento
listar_knowledge_sources("conhecimento_medico")
```

### Exemplo de knowledge_loader

```python
from utils.knowledge_loader import (
    criar_protocolo_exemplo,
    criar_string_knowledge,
    criar_knowledge_automatico
)

# Criar protocolo de exemplo
protocolo = criar_protocolo_exemplo()

# Criar knowledge source automaticamente
source = criar_knowledge_automatico("arquivo.txt")
```

## Estrutura de Arquivos

```text
aula11/
├── README.md                    # Documentação principal
├── GUIA_RAG.md                  # Guia detalhado de conceitos
├── INSTRUCOES_EXECUCAO.md       # Este arquivo
├── main.py                      # Sistema interativo
│
├── exemplos/                    # Exemplos progressivos
│   ├── 01_memory_basico.py      # Memory system
│   ├── 02_knowledge_pdf.py      # Knowledge sources
│   ├── 03_rag_simples.py        # RAG básico
│   └── 04_sistema_completo.py   # Sistema multi-agente
│
├── exercicios/                  # Exercícios práticos
│   ├── exercicio1_chatbot_memoria.py
│   ├── exercicio2_knowledge_base.py
│   └── exercicio3_rag_completo.py
│
├── conhecimento_medico/         # Base de conhecimento
│   └── protocolos/
│       └── urgencia_emergencia.txt
│
└── utils/                       # Funções auxiliares
    ├── __init__.py
    ├── rag_helper.py
    └── knowledge_loader.py
```

## Ordem Sugerida de Estudo

### 1. Teoria (30-45 min)

- Ler `README.md` - Visão geral
- Ler `GUIA_RAG.md` - Conceitos detalhados

### 2. Prática Guiada (1-2h)

- Executar `main.py` - Explorar menu interativo
- Executar exemplos na ordem:
  1. `01_memory_basico.py`
  2. `02_knowledge_pdf.py`
  3. `03_rag_simples.py`
  4. `04_sistema_completo.py`

### 3. Exercícios (2-3h)

- `exercicio1_chatbot_memoria.py` - Básico
- `exercicio2_knowledge_base.py` - Intermediário
- `exercicio3_rag_completo.py` - Avançado

### 4. Exploração (1h+)

- Experimentar com seus próprios documentos
- Testar diferentes configurações
- Integrar com Aula 10 (embeddings)

## Troubleshooting

### Erro: "No module named 'crewai'"

```bash
# Instalar dependências
uv sync
```

### Erro: "OPENAI_API_KEY not found"

```bash
# Configurar API key
uv run configurar-crewai
```

### Erro: "File not found: urgencia_emergencia.txt"

```bash
# Verificar se está no diretório correto
cd /home/lotus/supra/curso_crewai/aula11

# Verificar se arquivo existe
ls -la conhecimento_medico/protocolos/
```

### Storage não funciona

```bash
# Limpar storage e tentar novamente
python -c "from utils.rag_helper import limpar_storage; limpar_storage()"
```

### Respostas muito genéricas

- Verificar se `memory=True` está configurado
- Verificar se `knowledge_sources` está na Crew
- Usar `verbose=True` para ver logs
- Ler seção "Troubleshooting RAG" no `GUIA_RAG.md`

## Recursos Adicionais

### Documentação

- `README.md` - Visão geral e conceitos
- `GUIA_RAG.md` - Guia detalhado
- `INSTRUCOES_EXECUCAO.md` - Este arquivo

### Código

- `exemplos/` - Exemplos progressivos
- `exercicios/` - Exercícios com gabaritos
- `utils/` - Funções auxiliares

### Dados

- `conhecimento_medico/` - Base de conhecimento médico

## Próximos Passos

Após dominar a Aula 11:

1. **Revisar Aula 10** - Integrar embeddings personalizados
2. **Criar seu próprio RAG** - Use seus documentos
3. **Explorar outros domínios** - Além de medicina
4. **Otimizar performance** - Cache, chunking, etc.
5. **Deploy em produção** - API, web app, etc.

## Contato e Suporte

- Dúvidas sobre código: Revisar `GUIA_RAG.md` seção Troubleshooting
- Issues com exemplos: Verificar logs com `verbose=True`
- Conceitos: Reler `README.md` e `GUIA_RAG.md`

---

**🎯 Bons estudos! Domine RAG com CrewAI!**
