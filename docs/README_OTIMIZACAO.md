# 💰 Guia de Otimização OpenAI para CrewAI

Este repositório contém um guia completo de boas práticas para otimizar custos ao usar OpenAI com CrewAI, baseado no excelente guia da [Holori](https://holori.com/openai-pricing-guide/).

## 📁 Arquivos do Guia

### 📚 Documentação Completa

- **`GUIA_OTIMIZACAO_OPENAI.md`** - Guia completo com todas as estratégias e preços detalhados
- **`RESUMO_OTIMIZACAO_OPENAI.md`** - Resumo executivo com as principais práticas (⭐ **LEIA PRIMEIRO**)

### 💻 Código Prático

- **`exemplo_otimizacao_openai.py`** - Implementação prática de todas as boas práticas
- **Script executável**: `uv run exemplo-otimizacao`

## 🚀 Como Usar

### 1. Leia o Resumo (5 minutos)

```bash
# Abra o arquivo de resumo para ver as práticas essenciais
code RESUMO_OTIMIZACAO_OPENAI.md
```

### 2. Execute o Exemplo Prático

```bash
# Configure sua API key se ainda não fez
uv run configurar-crewai

# Execute o exemplo de otimização
uv run exemplo_otimizacao_openai.py
```

### 3. Explore o Guia Completo

```bash
# Para informações detalhadas e comparações
code GUIA_OTIMIZACAO_OPENAI.md
```

## 🎯 Principais Estratégias de Economia

### 1. **Escolha do Modelo** (85% de economia)

```python
# ✅ Use GPT-4o Mini como padrão
llm = ChatOpenAI(model="gpt-4o-mini")  # $0.15/$0.60 por 1M tokens

# ❌ Evite GPT-4o desnecessariamente  
llm = ChatOpenAI(model="gpt-4o")       # $2.50/$10 por 1M tokens
```

### 2. **Cache Inteligente** (50% de economia adicional)

```python
# Implementação automática no exemplo
cached_response = cache.get(prompt)
if cached_response:
    return cached_response  # $0.00 - Sem custo!
```

### 3. **Limite de Output** (20-30% de economia)

```python
# Sempre especifique limites
"Responda em no máximo 200 palavras"
"Liste apenas os 3 pontos principais"
```

### 4. **Monitoramento de Custos**

```python
# Sistema automático de alertas
if current_cost > budget * 0.8:
    send_alert("80% do orçamento usado")
```

## 📊 Resultados Esperados

### Economia Típica com Todas as Otimizações

- **Sem otimização**: $10.00/dia
- **Com GPT-4o Mini**: $1.50/dia (-85%)
- **Com Cache (50% hit)**: $0.75/dia (-92.5%)
- **Com Batch API**: $0.375/dia (-96.25%)

### ⚡ Exemplo Real de Execução

```
🎯 Agência de Marketing - 2 Agentes, 2 Tarefas
💰 Custo: $0.000145 (menos de $0.01)
⏱️  Tempo: 9.63 segundos
📝 Resultado: 1252 caracteres de conteúdo profissional
```

## 🤖 Configuração Otimizada para CrewAI

### Template de Agente Econômico

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# LLM otimizado
llm = ChatOpenAI(
    model="gpt-4o-mini",    # Modelo econômico
    temperature=0.1,        # Determinístico
    max_tokens=500          # Limite de resposta
)

# Agente otimizado
agente = Agent(
    role="Papel Específico",
    goal="Objetivo claro e mensurável",
    backstory="Resumo conciso (máx 300 chars)",
    llm=llm,
    verbose=False           # Reduz logs
)
```

### Template de Tarefa Econômica

```python
tarefa = Task(
    description="""
    Descrição específica da tarefa.
    LIMITE: Responda em máximo 150 palavras.
    """,
    agent=agente,
    expected_output="Output específico em 2-3 frases"
)
```

## 📈 Monitoramento Automático

O exemplo inclui uma classe `CrewAIOptimizer` que:

- ✅ **Monitora custos** em tempo real
- ✅ **Implementa cache** automático
- ✅ **Alerta sobre orçamento** (80% do limite)
- ✅ **Escolhe modelo** baseado na complexidade
- ✅ **Gera relatórios** de uso detalhados

## 🔧 Configuração Rápida

### 1. Instale Dependências

```bash
uv sync  # Instala todas as dependências
```

### 2. Configure API Key

```bash
uv run configurar-crewai  # Configura automaticamente
```

### 3. Execute Exemplo

```bash
uv run exemplo-otimizacao  # Demonstra todas as práticas
```

## 📚 Recursos Adicionais

### Comparação de Preços (por 1M tokens)

| Modelo | Input | Output | Uso Recomendado |
|--------|-------|--------|-----------------|
| **GPT-4o Mini** | $0.15 | $0.60 | ⭐ Padrão CrewAI |
| GPT-4o | $2.50 | $10.00 | Tarefas complexas |
| Claude Haiku | $0.25 | $1.25 | Alternativa |

### Links Úteis

- [Preços OpenAI Oficiais](https://openai.com/pricing)
- [Documentação CrewAI](https://docs.crewai.com/)
- [Guia Original Holori](https://holori.com/openai-pricing-guide/)

## 💡 Dicas Rápidas

1. **Use GPT-4o Mini** para 90% dos casos
2. **Implemente cache** para queries repetitivas
3. **Limite sempre** o tamanho das respostas
4. **Monitore gastos** semanalmente
5. **Use Batch API** quando possível (50% desconto)

## 🎯 Meta de Economia

**Objetivo: 90%+ de economia mantendo 95% da qualidade**

Com as práticas deste guia, você pode reduzir drasticamente os custos da OpenAI sem sacrificar a qualidade dos resultados do seu sistema CrewAI.

---

**⚡ Comece agora**: Execute `uv run exemplo_otimizacao_openai.py` e veja a economia em ação!
