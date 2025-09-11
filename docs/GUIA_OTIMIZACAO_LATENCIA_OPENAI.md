# Guia de Otimização de Latência OpenAI

## Visão Geral

Este guia aborda os princípios fundamentais para melhorar a latência em uma ampla variedade de casos de uso relacionados a LLMs. As técnicas apresentadas são baseadas em experiências com clientes e desenvolvedores em aplicações de produção.

## Os Sete Princípios de Otimização

### 1. Processar Tokens Mais Rapidamente

**Velocidade de Inferência** é provavelmente a primeira coisa que vem à mente ao abordar latência. Refere-se à taxa real em que o LLM processa tokens, frequentemente medida em TPM (tokens por minuto) ou TPS (tokens por segundo).

#### Estratégias

- **Usar modelos menores**: Modelos menores geralmente executam mais rápido e custam menos
- **Prompts mais detalhados**: Para manter qualidade com modelos menores
- **Exemplos few-shot**: Adicionar mais exemplos para melhorar performance
- **Fine-tuning/Destilação**: Personalizar modelos para casos específicos
- **Predicted Outputs**: Reduzir latência quando você conhece a maior parte da saída

```python
# Exemplo: Predicted Outputs para edição de código
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Adicione comentários a esta função"}
    ],
    prediction={
        "type": "content",
        "content": "def calcular_media(numeros):\n    return sum(numeros) / len(numeros)"
    }
)
```

### 2. Gerar Menos Tokens

Gerar tokens é quase sempre o passo de maior latência ao usar um LLM. **Cortar 50% dos tokens de saída pode reduzir ~50% da latência**.

#### Para Linguagem Natural

- Pedir ao modelo para ser mais conciso ("em menos de 20 palavras" ou "seja muito breve")
- Usar exemplos few-shot para ensinar respostas mais curtas
- Fine-tuning para respostas concisas

#### Para Saída Estruturada

- Minimizar sintaxe de saída: encurtar nomes de função, omitir argumentos nomeados
- Coalescer parâmetros onde possível

```python
# ❌ Verboso
{
    "message_is_conversation_continuation": "True",
    "number_of_messages_in_conversation_so_far": "1",
    "user_sentiment": "Aggravated"
}

# ✅ Otimizado
{
    "cont": "True",      # whether last message is a continuation
    "n_msg": "1",        # number of messages in conversation
    "tone_in": "Aggravated"  # sentiment of user query
}
```

### 3. Usar Menos Tokens de Entrada

Reduzir tokens de entrada resulta em menor latência, mas não é um fator significativo. **Cortar 50% do prompt pode resultar em apenas 1-5% de melhoria na latência**.

#### Técnicas para Contextos Massivos

- **Fine-tuning**: Substituir instruções longas
- **Filtrar contexto**: Podar resultados RAG, limpar HTML
- **Maximizar prefixo compartilhado**: Colocar partes dinâmicas no final do prompt

```python
# ✅ Otimizado para KV Cache
prompt = f"""
Instruções fixas aqui...
Exemplos fixos aqui...

# Contexto dinâmico (no final)
Resultados RAG: {rag_results}
Histórico: {conversation_history}
"""
```

### 4. Fazer Menos Requisições

Cada requisição incorre em latência de round-trip. Se você tem etapas sequenciais, considere **combiná-las em um único prompt**.

```python
# ❌ Múltiplas requisições
step1 = client.chat.completions.create(...)
step2 = client.chat.completions.create(...)
step3 = client.chat.completions.create(...)

# ✅ Requisição única
combined = client.chat.completions.create(
    messages=[{
        "role": "user", 
        "content": """
        Execute as seguintes etapas:
        1. Analise o sentimento
        2. Extraia entidades
        3. Gere resposta
        
        Retorne em JSON com campos: sentiment, entities, response
        """
    }]
)
```

### 5. Paralelizar

#### Para Etapas Não Sequenciais

```python
import asyncio

async def processar_paralelo():
    task1 = client.chat.completions.create(...)
    task2 = client.chat.completions.create(...)
    
    results = await asyncio.gather(task1, task2)
    return results
```

#### Execução Especulativa

Para etapas sequenciais onde um resultado é mais provável:

```python
# Iniciar moderação e geração simultaneamente
moderation_task = moderate_content(user_input)
generation_task = generate_response(user_input)

# Verificar moderação primeiro
if moderation_result.is_safe:
    return await generation_task
else:
    generation_task.cancel()
    return "Conteúdo não permitido"
```

### 6. Fazer os Usuários Esperarem Menos

Há uma grande diferença entre **esperar** e **ver o progresso acontecer**.

#### Técnicas

- **Streaming**: A abordagem mais eficaz
- **Chunking**: Processar em pedaços se precisar de pós-processamento
- **Mostrar etapas**: Superficializar o processo para o usuário
- **Estados de carregamento**: Spinners e barras de progresso

```python
# Exemplo de streaming
def stream_response():
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Explique IA"}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

### 7. Não Use LLM por Padrão

LLMs são poderosos, mas às vezes um **método clássico mais rápido** seria mais apropriado.

#### Alternativas

- **Hard-coding**: Para saídas altamente restritivas
- **Pré-computação**: Para entradas restritas
- **UI tradicional**: Para métricas e relatórios
- **Técnicas de otimização tradicionais**: Cache, hash maps, busca binária

```python
# ❌ Usando LLM desnecessariamente
def confirm_action(action):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Confirme a ação: {action}"}]
    )
    return response.choices[0].message.content

# ✅ Hard-coded
def confirm_action(action):
    confirmations = [
        f"Ação '{action}' executada com sucesso!",
        f"Confirmado: {action} foi realizada.",
        f"✓ {action} concluída."
    ]
    return random.choice(confirmations)
```

## Exemplo Prático: Bot de Atendimento ao Cliente

### Arquitetura Inicial

```text
Usuário → Contextualização → Verificação Retrieval → Retrieval → Assistente → Resposta
```

### Otimizações Implementadas

#### 1. Combinar Etapas (Fazer Menos Requisições)

```python
# ❌ Antes: Duas requisições separadas
def contextualizar_query(query, history):
    # GPT-4 call
    pass

def verificar_retrieval(query):
    # GPT-4 call
    pass

# ✅ Depois: Uma requisição combinada
def contextualizar_e_verificar(query, history):
    prompt = """
    Dado a conversa anterior, reescreva a última query para conter todo contexto necessário.
    Então, determine se requer lookup em tempo real.
    
    Responda no formato:
    {
        "query": "[query contextualizada]",
        "retrieval": "[true/false]"
    }
    """
    # Uma única chamada GPT-3.5
```

#### 2. Usar Modelos Menores (Processar Tokens Mais Rápido)

```python
# Mudança de GPT-4 para GPT-3.5 fine-tuned para tarefas específicas
model_config = {
    "contextualization": "gpt-3.5-turbo-fine-tuned",
    "reasoning": "gpt-3.5-turbo-fine-tuned", 
    "response": "gpt-4"  # Manter GPT-4 para resposta final
}
```

#### 3. Paralelização

```python
async def processar_request(user_input):
    # Executar em paralelo
    reasoning_task = get_reasoning_fields(user_input)
    retrieval_task = get_retrieval_context(user_input)
    
    reasoning, context = await asyncio.gather(reasoning_task, retrieval_task)
    
    # Usar ambos para resposta final
    response = await generate_final_response(reasoning, context)
    return response
```

#### 4. Otimizar Tokens de Saída

```python
# ❌ Campos verbosos (19 tokens extras)
{
    "message_is_conversation_continuation": "True",
    "number_of_messages_in_conversation_so_far": "1",
    "user_sentiment": "Aggravated"
}

# ✅ Campos otimizados
{
    "cont": "True",     # whether continuation
    "n_msg": "1",       # message count
    "tone_in": "Aggravated"  # user sentiment
}
```

## Checklist de Otimização

### 🚀 Alto Impacto

- [ ] Implementar streaming
- [ ] Usar modelos menores para tarefas específicas
- [ ] Combinar múltiplas etapas em uma requisição
- [ ] Otimizar tokens de saída (especialmente para structured output)

### ⚡ Médio Impacto

- [ ] Paralelizar chamadas independentes
- [ ] Implementar cache/pré-computação
- [ ] Usar predicted outputs quando aplicável
- [ ] Otimizar prompt structure para KV cache

### 🔧 Baixo Impacto (mas vale a pena)

- [ ] Reduzir tokens de entrada para contextos massivos
- [ ] Implementar estados de carregamento
- [ ] Hard-code respostas simples
- [ ] Fine-tuning para casos específicos

## Ferramentas de Monitoramento

```python
import time
from functools import wraps

def monitor_latency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        
        print(f"{func.__name__}: {(end - start) * 1000:.2f}ms")
        return result
    return wrapper

@monitor_latency
def call_openai_api():
    # Sua chamada para API
    pass
```

## Considerações Finais

1. **Teste sempre**: O impacto das otimizações varia por caso de uso
2. **Meça antes e depois**: Use métricas objetivas
3. **Considere trade-offs**: Latência vs qualidade vs custo
4. **Implemente gradualmente**: Uma otimização de cada vez
5. **Monitore em produção**: Comportamento pode diferir em produção

## Recursos Adicionais

- [Prompt Engineering Guide](./GUIA_BOAS_PRATICAS_PROMPTS.md)
- [Predicted Outputs Documentation](https://platform.openai.com/docs/guides/predicted-outputs)
- [Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Streaming Documentation](https://platform.openai.com/docs/api-reference/streaming)
