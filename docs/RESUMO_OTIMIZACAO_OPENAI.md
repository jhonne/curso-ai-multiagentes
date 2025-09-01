# 💰 Resumo: Boas Práticas OpenAI - Guia Rápido

> **Baseado no guia da Holori** - Principais estratégias para otimizar custos OpenAI

## 🎯 Escolha do Modelo Certo

### Por Custo (mais barato → mais caro)

1. **GPT-4o Mini** ($0.15/$0.60 por 1M tokens) - **RECOMENDADO** para CrewAI
2. **GPT-4o** ($2.50/$10 por 1M tokens) - Apenas para tarefas complexas
3. **GPT-4.5 Preview** ($75/$150 por 1M tokens) - Casos muito específicos

### Por Caso de Uso

- **Tarefas simples**: GPT-4o Mini (classificação, resumos, chat básico)
- **Raciocínio complexo**: GPT-4o (análise profunda, código avançado)
- **Análise de imagens**: GPT-4o Vision
- **Transcrição**: Whisper ($0.006/minuto)

## ⚡ 5 Otimizações Essenciais

### 1. Prompts Eficientes

```python
# ✅ BOM: Específico e conciso
"Resuma em 3 pontos principais:"

# ❌ RUIM: Prolixo e redundante  
"Por favor, você poderia fazer o favor de resumir..."
```

### 2. Cache Inteligente

```python
# Implemente cache para queries repetitivas
# Pode economizar até 50% dos custos
cache_response = check_cache(prompt)
if cache_response:
    return cache_response  # Sem custo!
```

### 3. Limite Output

```python
# Sempre limite a resposta
"Responda em no máximo 200 palavras"
"Liste apenas os 3 principais pontos"
```

### 4. Use Batch API

```python
# 50% de desconto para processamento em lote
# Ideal para múltiplas tarefas similares
batch_requests = [req1, req2, req3]  # Processe junto
```

### 5. Monitore Gastos

```python
# Configure alertas e limites
if current_cost > budget * 0.8:
    send_alert("80% do orçamento usado")
```

## 🤖 Configuração Otimizada para CrewAI

### Agentes Econômicos

```python
from crewai import Agent
from langchain_openai import ChatOpenAI

# LLM otimizado para custo
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Modelo mais econômico
    temperature=0.1,      # Menos variabilidade
    max_tokens=500        # Limite de resposta
)

# Agente otimizado
agente = Agent(
    role="Analista",
    goal="Objetivo específico e claro",
    backstory="Resumo conciso do background",  # Máximo 300 chars
    llm=llm,
    verbose=False  # Reduz logs desnecessários
)
```

### Tarefas Otimizadas

```python
tarefa = Task(
    description="""
    Tarefa específica e clara.
    LIMITE: Responda em máximo 150 palavras.
    """,
    agent=agente,
    expected_output="Output específico em 2-3 frases"
)
```

### Crew Econômica

```python
crew = Crew(
    agents=[agente1, agente2],
    tasks=[tarefa1, tarefa2],
    process=Process.sequential,
    verbose=False,    # Reduz output
    memory=False,     # Desative se não precisar
    planning=False    # Desative se não precisar
)
```

## 📊 Monitoramento de Custos

### Script de Monitoramento

```python
class CostMonitor:
    def __init__(self, budget=10.0):
        self.budget = budget
        self.spent = 0.0
    
    def track_execution(self, result):
        # Estima custo baseado no tamanho da resposta
        estimated_tokens = len(str(result)) * 0.25
        cost = estimated_tokens * 0.60 / 1000000  # GPT-4o Mini
        self.spent += cost
        
        print(f"💰 Custo: ${cost:.6f}")
        print(f"💸 Total: ${self.spent:.4f}")
        print(f"💳 Restante: ${self.budget - self.spent:.4f}")
```

## 🚀 Economia Máxima com Cache

### Implementação Simples

```python
import hashlib
import time

cache = {}

def cached_api_call(prompt, model="gpt-4o-mini", ttl=3600):
    # Gera chave única
    key = hashlib.md5(f"{prompt}|{model}".encode()).hexdigest()
    
    # Verifica cache
    if key in cache:
        timestamp, response = cache[key]
        if time.time() - timestamp < ttl:
            print("✅ Cache HIT - $0.00")
            return response
    
    # Chama API apenas se necessário
    response = api_call(prompt, model)
    cache[key] = (time.time(), response)
    return response
```

## 💡 Dicas de Economia Imediata

### 1. Substitua GPT-4o por GPT-4o Mini

- **Economia**: ~85% dos custos
- **Trade-off**: Capacidade ligeiramente menor
- **Ideal para**: 90% dos casos de uso

### 2. Use Temperature Baixa

```python
temperature=0.1  # Mais determinístico, menos re-tentativas
```

### 3. Limite Sempre o Output

```python
max_tokens=500  # Evita respostas muito longas
```

### 4. Batch Similar Tasks

```python
# Em vez de 10 chamadas separadas, faça 1 batch
batch_process(["task1", "task2", "task3"])  # 50% desconto
```

### 5. Cache Agressivo

```python
# Cache por 1 hora para queries similares
ttl = 3600  # Pode economizar 50%+ dos custos
```

## 🏆 Comparação de Preços

| Modelo | Input/1M | Output/1M | Uso Recomendado |
|--------|----------|-----------|-----------------|
| GPT-4o Mini | $0.15 | $0.60 | **CrewAI padrão** |
| GPT-4o | $2.50 | $10.00 | Tarefas complexas |
| Claude Haiku | $0.25 | $1.25 | Alternativa |
| Mistral Small | $2.00 | - | Europeu |

## 🎯 Resultado Esperado

### Economia Típica com Otimizações

- **Sem otimização**: $10/dia
- **Com GPT-4o Mini**: $1.5/dia (-85%)
- **Com Cache (50% hit)**: $0.75/dia (-92.5%)
- **Com Batch API**: $0.375/dia (-96.25%)

### ROI das Otimizações

1. **Troca de modelo**: 85% economia imediata
2. **Cache**: 50% economia adicional
3. **Batch API**: 50% economia adicional
4. **Prompts otimizados**: 20-30% economia adicional

## 🚀 Próximos Passos

1. **Implemente monitoramento** de custos
2. **Configure cache** para queries repetitivas  
3. **Use GPT-4o Mini** como padrão
4. **Limite outputs** em todas as tarefas
5. **Revise gastos** semanalmente

---

**💰 Meta de economia: 90%+ dos custos mantendo 95% da qualidade**

*Execute: `uv run exemplo_otimizacao_openai.py` para ver na prática*
