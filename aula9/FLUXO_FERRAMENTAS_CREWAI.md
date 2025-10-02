# 🔧 Como Funciona o Fluxo de Ferramentas no CrewAI

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura do Fluxo](#arquitetura-do-fluxo)
- [Componentes Detalhados](#componentes-detalhados)
- [Exemplos Práticos](#exemplos-práticos)
- [Como o LLM Decide os Parâmetros](#como-o-llm-decide-os-parâmetros)
- [Melhores Práticas](#melhores-práticas)
- [Perguntas Frequentes](#perguntas-frequentes)
- [Conclusão](#conclusão)

## Visão Geral

No CrewAI, **você não passa parâmetros manualmente** para as ferramentas. O **LLM
(GPT) faz isso automaticamente** baseado no contexto da tarefa e na definição da
ferramenta.

### 🎯 Conceito Principal

```text
Você define O QUÊ → LLM decide COMO → CrewAI executa
```

## Arquitetura do Fluxo

### 📊 Diagrama Visual

```mermaid
graph TB
    A[👤 Você cria Tool] -->|Define _run com parâmetros| B[🔧 Ferramenta]
    B -->|tools=[ferramenta]| C[🤖 Agente]
    C -->|Agent + description| D[📋 Task]
    D -->|Contexto da tarefa| E[🧠 LLM/GPT]
    
    E -->|Lê description da Tool| F{🔍 LLM Analisa}
    F -->|1. Preciso desta ferramenta?| G[✅ Sim]
    F -->|2. Quais parâmetros passar?| G
    
    G -->|Gera parâmetros automaticamente| H[⚙️ CrewAI]
    H -->|Chama ferramenta._run| I[🔧 Execução]
    I -->|Retorna resultado| E
    
    E -->|Usa resultado| J[📤 Resposta Final]
    
    style A fill:#e1f5ff
    style E fill:#fff4e1
    style H fill:#f0e1ff
    style I fill:#e1ffe1
    style J fill:#ffe1e1
```

### 🔄 Fluxo Passo a Passo

```text
PASSO 1: VOCÊ DEFINE A FERRAMENTA
├── class MinhaFerramenta(BaseTool):
│   ├── name = "nome_ferramenta"
│   ├── description = "O que a ferramenta faz"
│   └── def _run(self, parametro1: str, parametro2: int):
│       └── return "resultado"

PASSO 2: VOCÊ ASSOCIA AO AGENTE
├── ferramenta = MinhaFerramenta()
└── agente = Agent(
    ├── role="...",
    ├── goal="...",
    └── tools=[ferramenta]  ← Apenas isso!
    )

PASSO 3: LLM FAZ A MÁGICA
├── LLM lê a Task.description
├── LLM vê tools disponíveis
├── LLM decide: "Preciso desta ferramenta"
├── LLM gera: {"parametro1": "valor", "parametro2": 123}
└── CrewAI executa: ferramenta._run(parametro1="valor", parametro2=123)

PASSO 4: RESULTADO AUTOMÁTICO
└── Ferramenta retorna resultado → LLM usa na resposta final
```

### 📋 Exemplo Simples

```text
Usuário → Task(description="Analise: 'Quantos hospitais?'")
          ↓
CrewAI/LLM → Lê description + tools disponíveis
          ↓
LLM decide → "Vou usar analisador_consulta"
          ↓
LLM gera → {"pergunta": "Quantos hospitais?"}
          ↓
CrewAI chama → ferramenta._run(pergunta="Quantos hospitais?")
          ↓
Ferramenta → Retorna resultado JSON
          ↓
LLM → Usa resultado para responder ao usuário
```

## Componentes Detalhados

### 1️⃣ Definição da Ferramenta

```python
class AnalisadorConsultaTool(BaseTool):
    """
    🔑 IMPORTANTE: Estes 3 elementos são ESSENCIAIS
    """
    
    # 1. Nome da ferramenta (LLM usa para identificar)
    name: str = "analisador_consulta"
    
    # 2. Descrição (LLM usa para decidir QUANDO usar)
    description: str = (
        "Analisa perguntas dos usuários e classifica o tipo de consulta "
        "para determinar qual agente especializado deve responder."
    )
    
    # 3. Método _run com parâmetros tipados (LLM vê os tipos)
    def _run(self, pergunta: str = "") -> str:
        """
        Args:
            pergunta: Pergunta do usuário em linguagem natural
        
        Returns:
            str: Análise estruturada em JSON
        """
        
        # Sua lógica aqui
        resultado = f"Análise da pergunta: {pergunta}"
        return resultado
```

#### 🧠 O Que o LLM Vê

Quando você define uma ferramenta, o CrewAI automaticamente transforma isso em
informação que o LLM pode entender:

```json
{
  "name": "analisador_consulta",
  "description": "Analisa perguntas dos usuários...",
  "parameters": {
    "pergunta": {
      "type": "string",
      "description": "Pergunta do usuário em linguagem natural",
      "required": true
    }
  }
}
```

### 2️⃣ Associação ao Agente

```python
# Instanciar ferramenta
ferramenta_analisador = AnalisadorConsultaTool()

# Criar agente com a ferramenta
agente = Agent(
    role="Analisador de Consultas",
    goal="Classificar perguntas dos usuários",
    backstory="Especialista em análise de consultas...",
    tools=[ferramenta_analisador],  # ← APENAS ISSO!
    llm=llm
)
```

#### ⚠️ Você NÃO precisa fazer

```python
# ❌ ERRADO - Você não faz isso:
ferramenta_analisador._run(pergunta="Quantos hospitais?")

# ❌ ERRADO - Você não configura parâmetros:
tools=[{"ferramenta": ferramenta_analisador, "params": {"pergunta": "..."}}]

# ✅ CERTO - Apenas associe:
tools=[ferramenta_analisador]
```

### 3️⃣ Criação da Tarefa

```python
tarefa = Task(
    description="""
    Analise esta pergunta do usuário: "Quantos hospitais existem?"
    
    Use a ferramenta analisador_consulta para classificar o tipo
    de consulta e recomendar qual agente deve responder.
    """,
    agent=agente,
    expected_output="Análise estruturada com tipo e recomendação"
)
```

#### 🔍 O Que Acontece Internamente

```text
1. LLM recebe:
   ├── Task.description: "Analise esta pergunta..."
   ├── Agent.tools: [analisador_consulta]
   └── Ferramenta.description: "Analisa perguntas..."

2. LLM pensa:
   ├── "Preciso analisar uma pergunta"
   ├── "Tenho ferramenta 'analisador_consulta' que faz isso"
   ├── "Ela precisa do parâmetro 'pergunta' (tipo str)"
   └── "A pergunta é: 'Quantos hospitais existem?'"

3. LLM gera JSON interno:
   {
     "tool": "analisador_consulta",
     "arguments": {
       "pergunta": "Quantos hospitais existem?"
     }
   }

4. CrewAI executa:
   ferramenta._run(pergunta="Quantos hospitais existem?")
```

### 4️⃣ Execução Automática

```python
# Você apenas executa a crew
crew = Crew(agents=[agente], tasks=[tarefa])
resultado = crew.kickoff()

# O CrewAI + LLM fazem TUDO automaticamente:
# 1. Leem a tarefa
# 2. Decidem usar a ferramenta
# 3. Geram os parâmetros
# 4. Executam ferramenta._run(...)
# 5. Usam o resultado na resposta
```

## Exemplos Práticos

### Exemplo 1: Ferramenta Simples

```python
class CalculadoraTool(BaseTool):
    name: str = "calculadora"
    description: str = "Realiza operações matemáticas básicas"
    
    def _run(self, operacao: str, num1: float, num2: float) -> str:
        if operacao == "soma":
            resultado = num1 + num2
        elif operacao == "subtracao":
            resultado = num1 - num2
        else:
            resultado = "Operação inválida"
        
        return f"Resultado: {resultado}"

# Uso no agente
calc = CalculadoraTool()
agente = Agent(
    role="Matemático",
    goal="Resolver problemas matemáticos",
    tools=[calc]
)

# Tarefa
tarefa = Task(
    description="Calcule 15 + 27",
    agent=agente
)

# LLM automaticamente chamará:
# calc._run(operacao="soma", num1=15, num2=27)
```

### Exemplo 2: Ferramenta com Parâmetros Opcionais

```python
class ConsultaBancoDadosTool(BaseTool):
    name: str = "consulta_bd"
    description: str = "Consulta dados no banco de dados SQLite"
    
    def _run(self, tipo_consulta: str = "geral", limite: int = 10) -> str:
        """
        Args:
            tipo_consulta: Tipo específico (estabelecimentos, estatisticas, etc.)
            limite: Número máximo de resultados
        """
        
        query = f"SELECT * FROM tabela WHERE tipo = '{tipo_consulta}' LIMIT {limite}"
        # Executar query...
        return "Resultados da consulta..."

# Tarefa vaga - LLM decide os parâmetros
tarefa1 = Task(
    description="Mostre informações gerais",
    agent=agente
)
# LLM pode chamar: _run(tipo_consulta="geral", limite=10)

# Tarefa específica - LLM ajusta parâmetros
tarefa2 = Task(
    description="Liste os 5 principais estabelecimentos",
    agent=agente
)
# LLM pode chamar: _run(tipo_consulta="estabelecimentos", limite=5)
```

### Exemplo 3: Múltiplas Ferramentas

```python
class Ferramenta1(BaseTool):
    name: str = "buscar_dados"
    description: str = "Busca dados no banco"
    
    def _run(self, consulta: str) -> str:
        return f"Dados encontrados para: {consulta}"

class Ferramenta2(BaseTool):
    name: str = "analisar_dados"
    description: str = "Analisa dados estatísticos"
    
    def _run(self, dados: str) -> str:
        return f"Análise de: {dados}"

# Agente com múltiplas ferramentas
agente = Agent(
    role="Analista",
    goal="Buscar e analisar dados",
    tools=[Ferramenta1(), Ferramenta2()]
)

# Tarefa complexa
tarefa = Task(
    description="""
    Busque dados sobre hospitais e faça uma análise estatística.
    """,
    agent=agente
)

# LLM pode decidir:
# 1. Primeiro chamar: Ferramenta1._run(consulta="hospitais")
# 2. Depois chamar: Ferramenta2._run(dados="resultado da busca")
```

## Como o LLM Decide os Parâmetros

### 🧠 Processo de Decisão do LLM

```text
ENTRADA:
├── Task.description: "Analise a pergunta: 'Quantos hospitais?'"
├── Agent.tools: [analisador_consulta]
└── Tool.description: "Analisa perguntas dos usuários..."

ANÁLISE DO LLM:
├── 1. IDENTIFICA NECESSIDADE:
│   ├── Task menciona "Analise a pergunta"
│   └── Ferramenta pode "Analisa perguntas"
│   
├── 2. VERIFICA PARÂMETROS:
│   ├── Método _run aceita: pergunta (str)
│   └── Task contém: "Quantos hospitais?"
│   
├── 3. EXTRAI INFORMAÇÃO:
│   ├── Da description: "Quantos hospitais?"
│   └── É do tipo str (conforme esperado)
│   
└── 4. GERA CHAMADA:
    └── {"pergunta": "Quantos hospitais?"}

EXECUÇÃO:
└── ferramenta._run(pergunta="Quantos hospitais?")
```

### 📝 Exemplos de Como o LLM Extrai Valores

#### Exemplo A: Valor Explícito

```python
# Task
description = "Use a ferramenta para analisar: 'Mostre estatísticas'"

# LLM identifica:
# - Texto após "analisar:" é o valor do parâmetro
# - Extrai: "Mostre estatísticas"
# - Chama: _run(pergunta="Mostre estatísticas")
```

#### Exemplo B: Valor Implícito

```python
# Task
description = "O usuário quer saber sobre hospitais da região norte"

# LLM interpreta:
# - Toda a frase é o contexto
# - Reformula para ferramenta: "hospitais da região norte"
# - Chama: _run(pergunta="hospitais da região norte")
```

#### Exemplo C: Múltiplos Parâmetros

```python
# Tool
def _run(self, tipo: str, filtro: str, limite: int) -> str:
    pass

# Task
description = "Busque 5 estabelecimentos do tipo hospital no bairro centro"

# LLM extrai:
# - tipo: "hospital" (palavra-chave)
# - filtro: "bairro centro" (contexto de localização)
# - limite: 5 (número explícito)
# - Chama: _run(tipo="hospital", filtro="bairro centro", limite=5)
```

## Melhores Práticas

### ✅ DO (Faça)

#### 1. Descrições claras e específicas

```python
# ✅ BOM
description: str = (
    "Analisa perguntas de usuários sobre saúde e classifica em categorias: "
    "estabelecimentos, estatísticas, queixas, geográfico ou visão geral"
)

# ❌ RUIM
description: str = "Analisa coisas"
```

#### 2. Parâmetros com tipos explícitos

```python
# ✅ BOM
def _run(self, pergunta: str, limite: int = 10) -> str:
    pass

# ❌ RUIM
def _run(self, pergunta, limite=10):
    pass
```

#### 3. Docstrings completas

```python
# ✅ BOM
def _run(self, tipo_consulta: str, filtros: str = "") -> str:
    """
    Executa consulta no banco de dados
    
    Args:
        tipo_consulta: Tipo específico (estabelecimentos, estatisticas, etc.)
        filtros: Filtros adicionais opcionais
    
    Returns:
        str: Dados formatados como string
    """
    pass

# ❌ RUIM
def _run(self, tipo_consulta: str, filtros: str = "") -> str:
    pass
```

#### 4. Nomes descritivos

```python
# ✅ BOM
name: str = "analisador_consulta_saude"
name: str = "buscar_estabelecimentos_bd"

# ❌ RUIM
name: str = "tool1"
name: str = "buscar"
```

### ⚠️ DON'T (Não Faça)

#### 1. Não tente chamar ferramentas manualmente na tarefa

```python
# ❌ ERRADO
description = f"Use {ferramenta._run('teste')} para analisar"

# ✅ CERTO
description = "Use a ferramenta analisador_consulta para analisar"
```

#### 2. Não passe parâmetros fixos

```python
# ❌ ERRADO - Ferramenta com parâmetro fixo
class MinhaFerramenta(BaseTool):
    def __init__(self, pergunta_fixa):
        self.pergunta = pergunta_fixa
    
    def _run(self) -> str:
        return f"Analisando: {self.pergunta}"

# ✅ CERTO - Ferramenta flexível
class MinhaFerramenta(BaseTool):
    def _run(self, pergunta: str) -> str:
        return f"Analisando: {pergunta}"
```

#### 3. Não use descrições ambíguas

```python
# ❌ ERRADO
description: str = "Faz coisas com dados"

# ✅ CERTO
description: str = "Consulta banco SQLite de estabelecimentos de saúde"
```

## Perguntas Frequentes

### ❓ P: Como o LLM sabe quais parâmetros passar?

**R:** O LLM combina 3 fontes de informação:

1. **Assinatura do método `_run()`**: Nomes e tipos dos parâmetros
2. **Description da ferramenta**: O que ela faz
3. **Context da Task**: O que o usuário pediu

```python
# Exemplo completo
class MinhaFerramenta(BaseTool):
    name: str = "buscar_dados"
    description: str = "Busca dados no banco"
    
    def _run(self, tipo_dado: str, limite: int = 10) -> str:
        pass

# Task
description = "Busque 5 registros de hospitais"

# LLM conecta:
# - "hospitais" → tipo_dado: str
# - "5 registros" → limite: int
# Resultado: _run(tipo_dado="hospitais", limite=5)
```

### ❓ P: E se o LLM não encontrar o parâmetro na task?

**R:** O LLM usa o valor padrão (se definido) ou infere do contexto:

```python
def _run(self, consulta: str, limite: int = 10) -> str:
    pass

# Task vaga
description = "Busque dados gerais"

# LLM pode usar:
# - consulta: "dados gerais" (extrai da task)
# - limite: 10 (usa valor padrão)
```

### ❓ P: Posso ter múltiplas ferramentas com parâmetros diferentes?

**R:** Sim! O LLM escolhe qual ferramenta usar baseado na description:

```python
class FerramBusca(BaseTool):
    name: str = "buscar"
    description: str = "Busca dados no banco"
    def _run(self, query: str) -> str: pass

class FerramAnalise(BaseTool):
    name: str = "analisar"
    description: str = "Analisa estatisticamente os dados"
    def _run(self, dados: str, tipo_analise: str) -> str: pass

agente = Agent(tools=[FerramBusca(), FerramAnalise()])

# Task 1
description = "Busque informações sobre hospitais"
# LLM escolhe: FerramBusca._run(query="hospitais")

# Task 2
description = "Faça análise estatística descritiva dos dados"
# LLM escolhe: FerramAnalise._run(dados="...", tipo_analise="descritiva")
```

### ❓ P: Como debugar se o LLM não está passando os parâmetros corretos?

**R:** Use `verbose=True` e logs:

```python
# 1. Ative verbose no agente
agente = Agent(
    role="...",
    tools=[ferramenta],
    verbose=True  # ← Mostra todas as chamadas
)

# 2. Adicione logs na ferramenta
def _run(self, pergunta: str) -> str:
    print(f"🔍 Ferramenta recebeu: pergunta='{pergunta}'")
    # ... resto do código

# 3. Ative verbose na crew
crew = Crew(
    agents=[agente],
    tasks=[tarefa],
    verbose=True  # ← Mostra processo completo
)
```

### ❓ P: Posso forçar valores específicos para os parâmetros?

**R:** Sim, através da description da task:

```python
# Forçar valores específicos
tarefa = Task(
    description="""
    Use a ferramenta consulta_bd com estes parâmetros EXATOS:
    - tipo_consulta: "estabelecimentos"
    - limite: 5
    
    Não altere esses valores.
    """,
    agent=agente
)

# O LLM respeitará os valores especificados
```

### ❓ P: Como lidar com parâmetros complexos (dict, list)?

**R:** Use type hints e docstrings detalhadas:

```python
from typing import Dict, List

class FerramComplexaTool(BaseTool):
    name: str = "ferram_complexa"
    description: str = "Processa dados com filtros complexos"
    
    def _run(
        self,
        filtros: Dict[str, str],
        campos: List[str],
        limite: int = 10
    ) -> str:
        """
        Args:
            filtros: Dicionário com pares chave-valor para filtrar
                    Exemplo: {"tipo": "hospital", "bairro": "centro"}
            campos: Lista de campos a retornar
                    Exemplo: ["nome", "endereco", "telefone"]
            limite: Número máximo de resultados
        """
        print(f"Filtros: {filtros}")
        print(f"Campos: {campos}")
        return "Dados processados..."

# Task com estrutura clara
tarefa = Task(
    description="""
    Busque estabelecimentos com os seguintes critérios:
    - Filtros: tipo=hospital, bairro=centro
    - Campos: nome, endereco, telefone
    - Limite: 10 resultados
    """,
    agent=agente
)

# LLM interpretará e gerará:
# _run(
#     filtros={"tipo": "hospital", "bairro": "centro"},
#     campos=["nome", "endereco", "telefone"],
#     limite=10
# )
```

## Resumo Visual

```text
┌─────────────────────────────────────────────────────────────┐
│                   FLUXO CREWAI FERRAMENTAS                  │
└─────────────────────────────────────────────────────────────┘

1️⃣ VOCÊ DEFINE
   ├── class MinhaTool(BaseTool):
   │   ├── name = "nome_tool"
   │   ├── description = "O que faz"
   │   └── def _run(self, param: tipo):
   │       └── return resultado
   │
   └── agente = Agent(tools=[MinhaTool()])

2️⃣ VOCÊ CRIA TAREFA
   └── Task(description="Faça X com Y", agent=agente)

3️⃣ LLM ANALISA (Automático)
   ├── Lê Task.description
   ├── Vê Tool disponível
   ├── Extrai parâmetros do contexto
   └── Gera: {"param": "valor"}

4️⃣ CREWAI EXECUTA (Automático)
   └── Chama: ferramenta._run(param="valor")

5️⃣ RESULTADO
   └── Retorna para LLM usar na resposta

┌─────────────────────────────────────────────────────────────┐
│                  VOCÊ NÃO PRECISA FAZER:                    │
│  ❌ Passar parâmetros manualmente                           │
│  ❌ Chamar ferramenta._run() você mesmo                     │
│  ❌ Configurar mapeamento de parâmetros                     │
│                                                             │
│                  O LLM FAZ AUTOMATICAMENTE!                 │
└─────────────────────────────────────────────────────────────┘
```

## Conclusão

O CrewAI usa uma abordagem **declarativa** onde você:

- **Declara O QUE** a ferramenta faz (`description`)
- **Declara QUAIS** parâmetros ela aceita (`_run` signature)
- **Delega PARA O LLM** decidir quando e como usar

Isso torna o sistema:

- ✅ **Flexível**: LLM adapta aos diferentes contextos
- ✅ **Inteligente**: Interpreta intenções do usuário
- ✅ **Simples**: Você não gerencia parâmetros manualmente
- ✅ **Escalável**: Adicione ferramentas sem refatorar tasks

### 🎯 Conceito-Chave

**Lembre-se:** O LLM é o "cérebro" que conecta tasks, agentes e ferramentas. Você
apenas fornece os componentes, e ele orquestra tudo automaticamente!

### 📚 Recursos Relacionados

- [main.py](main.py) - Código completo da Aula 9
- [FLUXOGRAMA_AULA9.md](FLUXOGRAMA_AULA9.md) - Diagrama visual do sistema
- [RESUMO_AULA9.md](RESUMO_AULA9.md) - Resumo dos conceitos

---

**Documento gerado em:** 1 de outubro de 2025

**Curso:** CrewAI - Aula 9: Múltiplos Agentes Especializados
