# 📚 Módulo 2: Knowledge Sources

**Tempo estimado:** 45-60 minutos

## O Que Você Vai Aprender

✅ Como conectar agentes a documentos  
✅ 7 tipos de Knowledge Sources  
✅ Diferença entre agentes com e sem knowledge  
✅ Quando usar cada tipo de fonte  

## Arquivos Deste Módulo

- `README.md` - Este arquivo
- `exemplo.py` - Demonstração prática
- `exercicio.py` - Exercício com gabarito

## Conceito: Knowledge Sources

### O Problema

```python
# SEM KNOWLEDGE ❌
User: "Qual o protocolo de 2024?"
LLM: "Baseado no meu treino até 2023..." ❌
```

### A Solução

```python
# COM KNOWLEDGE ✅
from crewai.knowledge.source.pdf_knowledge_source import (
    PDFKnowledgeSource
)

knowledge = PDFKnowledgeSource(
    file_paths=["protocolo_2024.pdf"]
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    knowledge_sources=[knowledge]  # 🔑 Acesso a docs!
)

User: "Qual o protocolo de 2024?"
LLM: "Segundo protocolo 2024 (pág. 5)..." ✅
```

## 7 Tipos de Knowledge Sources

### 1. StringKnowledgeSource 💬

**Quando usar:** Texto direto no código

```python
from crewai.knowledge.source.string_knowledge_source import (
    StringKnowledgeSource
)

knowledge = StringKnowledgeSource(
    content="Protocolo: Vermelho = emergência"
)
```

### 2. TextFileKnowledgeSource 📄

**Quando usar:** Arquivos `.txt`

```python
from crewai.knowledge.source.text_file_knowledge_source import (
    TextFileKnowledgeSource
)

knowledge = TextFileKnowledgeSource(
    file_paths=["protocolos/urgencia.txt"]
)
```

### 3. PDFKnowledgeSource 📕

**Quando usar:** Documentos PDF

```python
from crewai.knowledge.source.pdf_knowledge_source import (
    PDFKnowledgeSource
)

knowledge = PDFKnowledgeSource(
    file_paths=["manual.pdf", "guia.pdf"]
)
```

### 4. CSVKnowledgeSource 📊

**Quando usar:** Planilhas, dados tabulares

```python
from crewai.knowledge.source.csv_knowledge_source import (
    CSVKnowledgeSource
)

knowledge = CSVKnowledgeSource(
    file_paths=["medicamentos.csv"]
)
```

### 5. JSONKnowledgeSource 🗂️

**Quando usar:** Dados estruturados

```python
from crewai.knowledge.source.json_knowledge_source import (
    JSONKnowledgeSource
)

knowledge = JSONKnowledgeSource(
    file_paths=["config.json"]
)
```

### 6. ExcelKnowledgeSource 📈

**Quando usar:** Planilhas Excel

```python
knowledge = ExcelKnowledgeSource(
    file_paths=["dados.xlsx"]
)
```

### 7. WebKnowledgeSource 🌐

**Quando usar:** Páginas web, APIs

```python
knowledge = WebKnowledgeSource(
    urls=["https://docs.example.com"]
)
```

## Como Executar

### 1. Exemplo Prático

```bash
cd modulos/02_knowledge
uv run exemplo.py
```

**O que mostra:**
- Agente SEM knowledge (genérico)
- Agente COM knowledge (consulta protocolo)
- Múltiplos casos de teste

**Tempo:** ~15 minutos

### 2. Exercício

```bash
uv run exercicio.py
```

**Objetivo:** Criar agente que consulta protocolos médicos

**Gabarito:** Incluído no arquivo

**Tempo:** ~30 minutos

## Código Mínimo

```python
from crewai import Agent, Task, Crew, LLM
from crewai.knowledge.source.text_file_knowledge_source import (
    TextFileKnowledgeSource
)

# 1. Criar knowledge
knowledge = TextFileKnowledgeSource(
    file_paths=["../../conhecimento_medico/protocolos/urgencia_emergencia.txt"]
)

# 2. Criar agente
llm = LLM(model="gpt-4o-mini")
agent = Agent(
    role="Triagista",
    goal="Classificar usando protocolos",
    backstory="Consulta protocolos oficiais.",
    llm=llm
)

# 3. Criar crew com knowledge
crew = Crew(
    agents=[agent],
    tasks=[task],
    knowledge_sources=[knowledge]  # 🔑 KNOWLEDGE!
)

# Agente consultará protocolos automaticamente!
resultado = crew.kickoff(inputs={"sintomas": "dor no peito"})
```

## Boas Práticas

### ✅ DO (Faça)

**Organize arquivos:**

```text
conhecimento/
├── protocolos/
│   ├── triagem.txt
│   └── urgencia.pdf
├── medicamentos/
│   └── lista.csv
└── procedimentos/
    └── guia.json
```

**Use tipo apropriado:**

```python
# TXT para protocolos simples
# PDF para documentos oficiais
# CSV para dados tabulares
# JSON para configs
```

### ❌ DON'T (Evite)

**Não carregue tudo:**

```python
# ❌ RUIM
knowledge = PDFKnowledgeSource(
    file_paths=glob("**/*.pdf")  # Centenas de PDFs!
)

# ✅ BOM
knowledge = PDFKnowledgeSource(
    file_paths=["protocolo_triagem.pdf"]  # Apenas necessário
)
```

## Quando Usar Knowledge

### ✅ Use Knowledge Quando

- Precisa consultar documentos
- Informações atualizadas
- Protocolos/manuais
- Dados proprietários
- Citar fontes

### ❌ Não Use Knowledge Quando

- LLM já sabe
- Dados mudam constantemente
- Performance crítica
- Docs muito grandes (>10MB)

## Múltiplos Knowledge Sources

```python
# Pode combinar vários!
crew = Crew(
    knowledge_sources=[
        protocolos_txt,
        medicamentos_csv,
        procedimentos_pdf
    ]
)
```

## Próximos Passos

Após dominar Knowledge:

1. **Módulo 3:** RAG Avançado (combina Memory + Knowledge)
2. **Integração:** Aula 10 (Embeddings customizados)

## Troubleshooting

**Problema:** Agente não consulta knowledge  
**Solução:** Backstory deve mencionar "consultar protocolos"

**Problema:** Arquivo não encontrado  
**Solução:** Usar caminho absoluto ou relativo correto

**Problema:** Respostas genéricas  
**Solução:** Task deve pedir para "consultar e citar fonte"

---

**📚 Ver também:**
- [GUIA_COMPLETO.md](../../docs/GUIA_COMPLETO.md)
- [Módulo 1: Memory](../01_memory/README.md)
