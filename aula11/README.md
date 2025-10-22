# Aula 11: RAG (Retrieval-Augmented Generation) com CrewAI

## 🎯 Objetivos da Aula

Nesta aula você aprenderá a criar agentes inteligentes que **lembram de conversas** e **consultam documentos externos** para dar respostas mais precisas e contextualizadas. Você vai:

- Entender o que é RAG e por que é importante
- Usar **Memory** para agentes que lembram do histórico
- Usar **Knowledge Sources** para consultar documentos (PDFs, TXTs, etc.)
- Combinar Memory + Knowledge em sistemas completos
- Aplicar RAG em casos práticos (exemplo: triagem médica)

## 🧠 O Que é RAG?

**RAG** significa **Retrieval-Augmented Generation** (Geração Aumentada por Recuperação).

### Sem RAG

```text
Usuário: "Qual o protocolo de triagem para dor no peito?"
Agente: "Procure um médico." ❌ (resposta genérica)
```

### Com RAG

```text
Usuário: "Qual o protocolo de triagem para dor no peito?"
Sistema: [busca em protocolo_triagem.txt]
Agente: "Segundo o Protocolo Manchester, dor torácica é
         classificada como VERMELHO - atendimento imediato!" ✅
```

**Resultado**: Respostas fundamentadas em documentos reais!

## 📚 Componentes do RAG

### 1. Memory System (Memória)

Permite que agentes **lembrem** de conversas anteriores:

```python
# Agente SEM memory
Usuário: "Meu nome é João"
Agente: "Olá!"
Usuário: "Qual é meu nome?"
Agente: "Desculpe, não sei." ❌

# Agente COM memory
Usuário: "Meu nome é João"
Agente: "Prazer, João!"
Usuário: "Qual é meu nome?"
Agente: "Seu nome é João!" ✅
```

**Tipos de Memory:**

- **Short-term**: Memória da conversa atual
- **Long-term**: Memória persistente entre sessões
- **Entity**: Extrai e lembra informações específicas (nomes, datas, etc.)

### 2. Knowledge Sources (Fontes de Conhecimento)

Permite que agentes **consultem documentos** para buscar informações:

```python
# Tipos de documentos suportados
- PDFs (protocolos, manuais, relatórios)
- TXTs (guias, procedimentos)
- CSVs (tabelas, dados estruturados)
- JSONs (configurações, dados)
- Páginas Web (documentação online)
```

### 3. RAG Completo = Memory + Knowledge

Combina os dois para agentes que:

- Lembram do contexto do usuário (idade, histórico, preferências)
- Consultam documentos para dar respostas precisas
- Personalizam respostas baseadas no contexto

## 🏥 Exemplo Prático: Sistema de Triagem Médica

### Cenário

Um paciente liga para o hospital relatando sintomas. O sistema precisa:

1. Lembrar das informações do paciente (nome, idade, histórico)
2. Consultar protocolos médicos oficiais
3. Classificar o nível de urgência corretamente

### Implementação

```python
from crewai import Agent, Crew, Task, Process
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# Knowledge: Protocolo médico
protocolo = StringKnowledgeSource(
    content="""
    PROTOCOLO MANCHESTER - TRIAGEM
    
    Dor Torácica:
    - Paciente < 50 anos: AMARELO (urgente)
    - Paciente ≥ 50 anos: VERMELHO (emergência)
    - Com histórico cardíaco: VERMELHO (emergência)
    """,
    metadata={"tipo": "protocolo_triagem"}
)

# Agente com Memory + Knowledge
agente_triagem = Agent(
    role="Enfermeiro de Triagem",
    goal="Classificar pacientes segundo Protocolo Manchester",
    backstory="Enfermeiro experiente especializado em triagem de emergência.",
    memory=True,  # Lembra do paciente
    knowledge_sources=[protocolo],  # Consulta protocolo
    verbose=True
)

# Tarefa
tarefa = Task(
    description="Paciente João, 55 anos, relata dor no peito há 30 minutos.",
    expected_output="Classificação de urgência segundo protocolo",
    agent=agente_triagem
)

# Executar
crew = Crew(agents=[agente_triagem], tasks=[tarefa], process=Process.sequential)
resultado = crew.kickoff()
print(resultado)
```

**Resultado esperado:**

```text
"Paciente João, 55 anos, apresenta dor torácica.
Segundo Protocolo Manchester: idade ≥ 50 anos.
CLASSIFICAÇÃO: VERMELHO - EMERGÊNCIA
Recomendação: Atendimento médico imediato."
```

## 🚀 Como Executar os Exemplos

### 1. Executar Sistema Completo

```bash
cd aula11
uv run main.py
```

Este script interativo permite testar:

- Comparação: agente COM vs SEM memory
- Comparação: agente COM vs SEM knowledge
- Sistema RAG completo (Memory + Knowledge)

### 2. Executar Exemplos Individuais

```bash
# Exemplo 1: Memory básico
uv run exemplos/01_memory_basico.py

# Exemplo 2: Knowledge Sources
uv run exemplos/02_knowledge_sources.py

# Exemplo 3: RAG simples
uv run exemplos/03_rag_simples.py

# Exemplo 4: Sistema multi-agente
uv run exemplos/04_sistema_completo.py
```

### 3. Fazer Exercícios Práticos

```bash
# Exercício 1: Chatbot com memória
uv run exercicios/exercicio1_chatbot.py

# Exercício 2: Consulta a base de conhecimento
uv run exercicios/exercicio2_knowledge.py

# Exercício 3: Sistema RAG completo
uv run exercicios/exercicio3_rag_completo.py
```

## 📂 Estrutura de Arquivos

```text
aula11/
│
├── README.md                        # Este arquivo
├── main.py                          # Sistema interativo principal
│
├── exemplos/                        # Exemplos progressivos
│   ├── 01_memory_basico.py         # Memory: Com vs Sem
│   ├── 02_knowledge_sources.py     # Knowledge: Tipos de documentos
│   ├── 03_rag_simples.py           # RAG: Memory + Knowledge
│   └── 04_sistema_completo.py      # Sistema multi-agente
│
├── exercicios/                      # Exercícios com gabaritos
│   ├── exercicio1_chatbot.py       # Criar chatbot com memória
│   ├── exercicio2_knowledge.py     # Consultar documentos
│   └── exercicio3_rag_completo.py  # Sistema RAG completo
│
├── conhecimento_medico/             # Base de conhecimento exemplo
│   └── protocolos/
│       └── urgencia_emergencia.txt
│
├── docs/                            # Documentação avançada (opcional)
│   ├── REFERENCIA_COMPLETA.md      # Guia técnico detalhado
│   └── CASOS_DE_USO.md             # Mais exemplos práticos
│
└── TROUBLESHOOTING.md               # Solução de problemas comuns
```

## 💡 Conceitos Aprendidos

### Memory System

- **Short-term Memory**: Mantém contexto da conversa atual
- **Long-term Memory**: Persiste informações entre sessões
- **Entity Memory**: Extrai automaticamente entidades importantes
- **Configuração**: `Agent(memory=True)` ativa todos os tipos

### Knowledge Sources

- **StringKnowledgeSource**: Texto direto no código
- **TextFileKnowledgeSource**: Arquivos TXT
- **PDFKnowledgeSource**: Documentos PDF
- **CSVKnowledgeSource**: Planilhas e tabelas
- **Configuração**: `Agent(knowledge_sources=[fonte1, fonte2])`

### RAG Completo

- Combina Memory + Knowledge no mesmo agente
- Memory fornece contexto personalizado
- Knowledge fornece informações precisas
- Resultado: Respostas contextualizadas e fundamentadas

## 🔧 Configuração ChromaDB

Os exemplos usam **ChromaDB** para armazenar embeddings (representações vetoriais dos textos). A configuração é **automática**:

```python
# Configuração automática já incluída nos exemplos
# ChromaDB será criado em: .chromadb/
```

Se precisar limpar o cache:

```bash
rm -rf .chromadb/
```

## 🎯 Comparação com Aulas Anteriores

| Aula | Técnica | Capacidade | Limitação |
|------|---------|------------|-----------|
| **Aula 6** | Chatbot básico | Responder perguntas | ❌ Não lembra conversas |
| **Aula 10** | Embeddings | Buscar documentos similares | ❌ Não integra com agentes |
| **Aula 11** | RAG completo | Memory + Knowledge | ✅ Solução completa! |

## 📊 Quando Usar RAG?

### ✅ Use RAG quando:

- Precisa que agentes lembrem do contexto do usuário
- Agentes devem consultar documentos específicos (manuais, protocolos)
- Informações mudam frequentemente (adicionar documentos é mais fácil que retreinar)
- Precisa rastrear a fonte das informações (transparência)

### ❌ Não precisa de RAG quando:

- Tarefa não depende de documentos externos
- Conhecimento do LLM base é suficiente
- Não há necessidade de memória entre interações

## 🎓 Exercícios Práticos

### Exercício 1: Chatbot com Memória (Básico)

**Objetivo**: Criar chatbot que lembra informações do usuário.

**Desafio**: O chatbot deve lembrar nome, idade e preferências do usuário mesmo após várias interações.

**Gabarito**: Incluído em `exercicios/exercicio1_chatbot.py`

### Exercício 2: Consulta a Documentos (Intermediário)

**Objetivo**: Criar agente que consulta base de conhecimento médico.

**Desafio**: Dado um sintoma, o agente deve buscar no protocolo e retornar a classificação correta.

**Gabarito**: Incluído em `exercicios/exercicio2_knowledge.py`

### Exercício 3: Sistema RAG Completo (Avançado)

**Objetivo**: Combinar Memory + Knowledge em sistema de atendimento.

**Desafio**: Sistema deve lembrar do paciente E consultar protocolos para dar diagnóstico personalizado.

**Gabarito**: Incluído em `exercicios/exercicio3_rag_completo.py`

## 🔍 Observações Importantes

- **Memory consome recursos**: Use apenas quando necessário
- **Knowledge Sources precisam de embeddings**: Primeira execução pode ser lenta
- **ChromaDB persiste dados**: Limpe cache se precisar reprocessar documentos
- **Verbose=True**: Ajuda a entender o que o agente está fazendo

## ⚠️ Troubleshooting

### Problema: "ChromaDB not found"

**Solução**: ChromaDB é instalado automaticamente. Se der erro:

```bash
uv sync  # Reinstalar dependências
```

### Problema: Memory não está funcionando

**Solução**: Certifique-se de que `memory=True` está definido no agente:

```python
agent = Agent(
    role="...",
    memory=True,  # ← Essencial!
    verbose=True
)
```

### Problema: Knowledge Source não encontra informações

**Solução**: Verifique o caminho do arquivo e conteúdo:

```python
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

source = TextFileKnowledgeSource(
    file_path="./conhecimento_medico/protocolos/urgencia_emergencia.txt"
)

# Verificar se arquivo existe
import os
print(os.path.exists(source.file_path))
```

**Mais problemas?** Consulte `TROUBLESHOOTING.md` na raiz da aula.

## 🚀 Próximos Passos

Após dominar esta aula:

1. **Integre com Aula 10**: Use embeddings customizados
2. **Crie sua base de conhecimento**: Adicione documentos do seu domínio
3. **Experimente multi-agente**: Combine vários agentes com RAG
4. **Deploy em produção**: Crie API ou webapp com seu sistema RAG

## 📚 Documentação Adicional

- **docs/REFERENCIA_COMPLETA.md**: Guia técnico detalhado sobre todas as funcionalidades
- **docs/CASOS_DE_USO.md**: Mais exemplos práticos em diferentes domínios
- **TROUBLESHOOTING.md**: Soluções para problemas comuns

---

**Dica**: Comece executando `uv run main.py` para ver todos os conceitos em ação antes de explorar exemplos individuais!

**Bom aprendizado! 🚀**
