# Guia de Boas Práticas para Prompts no CrewAI

## Sumário

1. [Introdução](#introdução)
2. [Por Que Personalizar Prompts?](#por-que-personalizar-prompts)
3. [Entendendo o Sistema de Prompts do CrewAI](#entendendo-o-sistema-de-prompts-do-crewai)
4. [Transparência: O Que o CrewAI Injeta Automaticamente](#transparência-o-que-o-crewai-injeta-automaticamente)
5. [Boas Práticas Fundamentais](#boas-práticas-fundamentais)
6. [Métodos de Personalização](#métodos-de-personalização)
7. [Otimização para Modelos Específicos](#otimização-para-modelos-específicos)
8. [Gerenciamento de Arquivos de Prompt](#gerenciamento-de-arquivos-de-prompt)
9. [Depuração e Monitoramento](#depuração-e-monitoramento)
10. [Exemplos Práticos](#exemplos-práticos)
11. [Checklist de Produção](#checklist-de-produção)

## Introdução

Este guia apresenta as melhores práticas para personalização de prompts no CrewAI, permitindo controle granular sobre o comportamento dos agentes e otimização para diferentes casos de uso, modelos de linguagem e idiomas.

## Por Que Personalizar Prompts?

A personalização de prompts oferece vantagens significativas:

### 🎯 **Otimização para LLMs Específicos**

- Diferentes modelos (GPT-4, Claude, Llama) respondem melhor a formatos específicos
- Aproveita as arquiteturas únicas de cada modelo

### 🌍 **Suporte Multilíngue**

- Construa agentes que operam exclusivamente em idiomas específicos
- Lida com nuances culturais e linguísticas com precisão

### 🏢 **Especialização por Domínio**

- Adapte prompts para setores especializados (saúde, finanças, jurídico)
- Incorpore terminologias e protocolos específicos do setor

### 🎭 **Controle de Tom e Estilo**

- Ajuste para ser formal, casual, criativo ou analítico
- Mantenha consistência na personalidade do agente

### ⚡ **Casos de Uso Avançados**

- Estruturas e formatações complexas de prompt
- Requisitos específicos e detalhados do projeto

## Entendendo o Sistema de Prompts do CrewAI

O CrewAI usa um sistema modular composto por:

### 📋 **Templates de Agente**

- Determinam como cada agente aborda seu papel
- Controlam a personalidade e comportamento base

### 🧩 **Prompt Slices**

- Comportamentos especializados (tarefas, ferramentas, saída)
- Componentes modulares que podem ser sobrescritos

### 🚨 **Tratamento de Erros**

- Como agentes respondem a falhas e timeouts
- Estratégias de recuperação e retry

### 🔧 **Prompts Específicos de Ferramentas**

- Instruções detalhadas para uso de ferramentas
- Formatação de entrada e saída de ferramentas

## Transparência: O Que o CrewAI Injeta Automaticamente

> **⚠️ Importante para Produção**: O CrewAI adiciona instruções automáticas que você precisa conhecer para ter controle total.

### Para Agentes Sem Ferramentas

```text
"I MUST use these formats, my job depends on it!"
```

### Para Agentes Com Ferramentas

```text
"IMPORTANT: Use the following format in your response: 
Thought: you should always think about what to do 
Action: the action to take, only one name of [tool_names] 
Action Input: the input to the action, just a simple JSON object..."
```

### Para Saídas Estruturadas (JSON/Pydantic)

```text
"Ensure your final answer contains only the content in the following format: {output_format} 
Ensure the final output does not include any code block markers like ```json or ```python."
```

## Boas Práticas Fundamentais

### 1. 🔍 **Transparência Primeiro**

```python
# Sempre inspecione prompts antes de produção
from crewai.utilities.prompts import Prompts

prompt_generator = Prompts(
    agent=agent,
    has_tools=len(agent.tools) > 0,
    use_system_prompt=agent.use_system_prompt
)

generated_prompt = prompt_generator.task_execution()
print("=== SYSTEM PROMPT ===")
print(generated_prompt["system"])
```

### 2. 📝 **Documentação Completa**

- Documente todas as customizações
- Mantenha histórico de mudanças
- Explique o propósito de cada alteração

### 3. 🧪 **Teste com Múltiplos Modelos**

- Instruções padrão se comportam diferente em cada modelo
- Valide performance em modelos de produção

### 4. 📊 **Monitoramento Contínuo**

- Use ferramentas de observabilidade
- Monitore prompts em tempo real
- Detecte degradação de performance

### 5. 🎯 **Alterações Mínimas e Precisas**

- Sobrescreva apenas o necessário
- Mantenha funcionalidade padrão quando possível
- Evite mudanças desnecessárias

## Métodos de Personalização

### Método 1: Templates Personalizados (Recomendado)

```python
from crewai import Agent

# Template customizado sem instruções padrão
custom_system_template = """You are {role}. {backstory}

Your goal is: {goal}

Respond naturally and conversationally. Focus on providing helpful, accurate information."""

custom_prompt_template = """Task: {input}

Please complete this task thoughtfully."""

agent = Agent(
    role="Research Assistant",
    goal="Help users find accurate information",
    backstory="You are a helpful research assistant.",
    system_template=custom_system_template,
    prompt_template=custom_prompt_template,
    use_system_prompt=True
)
```

### Método 2: Arquivo JSON Personalizado

#### Arquivo JSON Personalizado

```json
{
    "slices": {
        "no_tools": "\nProvide your best answer in a natural, conversational way.",
        "tools": "\nYou have access to these tools: {tools}\n\nUse them when helpful, but respond naturally.",
        "formatted_task_instructions": "Format your response as: {output_format}"
    }
}
```

**Implementação:**

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    prompt_file="custom_prompts.json",
    verbose=True
)
```

### Método 3: Desabilitar Prompts de Sistema

```python
# Para modelos como o1 que não suportam system prompts
agent = Agent(
    role="Analyst",
    goal="Analyze data",
    backstory="Expert analyst",
    use_system_prompt=False
)
```

## Otimização para Modelos Específicos

### Exemplo: Llama 3.3

```python
from crewai import Agent, Crew, Task

# Templates específicos do Llama 3.3
system_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>"""
prompt_template = """<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>"""
response_template = """<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>"""

principal_engineer = Agent(
    role="Principal Engineer",
    goal="Oversee AI architecture and make high-level decisions",
    backstory="You are the lead engineer responsible for critical AI systems",
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    system_template=system_template,
    prompt_template=prompt_template,
    response_template=response_template
)
```

### Diretrizes por Modelo

#### GPT-4/GPT-4o

- Use system prompts claros e estruturados
- Aproveite capacidades de reasoning step-by-step
- Formato JSON bem estruturado para saídas

#### Claude (Anthropic)

- Prompts mais conversacionais
- Use exemplos e analogias
- Estruture com marcadores XML quando necessário

#### Llama

- Siga formato de templates específicos
- Use tokens especiais corretos
- Otimize para context length

## Gerenciamento de Arquivos de Prompt

### 📁 **Estrutura Organizacional**

```text
prompts/
├── models/
│   ├── gpt4_prompts.json
│   ├── claude_prompts.json
│   └── llama_prompts.json
├── languages/
│   ├── pt_br_prompts.json
│   ├── en_prompts.json
│   └── es_prompts.json
└── domains/
    ├── finance_prompts.json
    ├── healthcare_prompts.json
    └── legal_prompts.json
```

### 📋 **Convenções de Nomenclatura**

- `{modelo}_{versao}_prompts.json`
- `{idioma}_prompts.json`
- `{dominio}_{especialidade}_prompts.json`

### 📚 **Documentação de Arquivos**

```json
{
    "_metadata": {
        "version": "1.2.0",
        "description": "Prompts otimizados para análise financeira",
        "last_updated": "2025-01-15",
        "author": "equipe-ia",
        "model_compatibility": ["gpt-4", "claude-3"]
    },
    "slices": {
        "format": "..."
    }
}
```

## Depuração e Monitoramento

### 🔍 **Inspeção de Prompts**

```python
def inspect_prompt(agent, task):
    """Utilitário para inspecionar prompts gerados"""
    from crewai.utilities.prompts import Prompts
    
    prompt_generator = Prompts(
        agent=agent,
        has_tools=len(agent.tools) > 0,
        use_system_prompt=agent.use_system_prompt
    )
    
    generated_prompt = prompt_generator.task_execution()
    
    print("=== PROMPT INSPECTION ===")
    print(f"Agent: {agent.role}")
    print(f"Task: {task.description}")
    print(f"Has Tools: {len(agent.tools) > 0}")
    print(f"Use System Prompt: {agent.use_system_prompt}")
    print("\n=== SYSTEM PROMPT ===")
    print(generated_prompt.get("system", "N/A"))
    print("\n=== USER PROMPT ===")
    print(generated_prompt.get("user", "N/A"))
    
    return generated_prompt
```

### 📊 **Integração com Observabilidade**

```python
# Configuração para Langfuse
import os
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)
```

## Exemplos Práticos

### Exemplo 1: Agente de Atendimento ao Cliente

```python
# custom_support_prompts.json
{
    "slices": {
        "format": """Quando responder a clientes, sempre siga esta estrutura:

COMPREENSÃO: Resumo do problema do cliente
SOLUÇÃO: Passos específicos para resolver
ACOMPANHAMENTO: Como o cliente pode obter mais ajuda

Mantenha tom empático e profissional."""
    }
}
```

```python
support_agent = Agent(
    role="Especialista em Atendimento ao Cliente",
    goal="Resolver problemas dos clientes com eficiência e empatia",
    backstory="Você é um especialista experiente em atendimento, conhecido por resolver problemas complexos com paciência e clareza.",
    verbose=True
)

crew = Crew(
    agents=[support_agent],
    tasks=[support_task],
    prompt_file="custom_support_prompts.json"
)
```

### Exemplo 2: Agente Multilíngue (Português)

```python
# pt_br_prompts.json
{
    "slices": {
        "no_tools": "\nResponda de forma natural em português brasileiro, usando linguagem clara e objetiva.",
        "tools": "\nVocê tem acesso às seguintes ferramentas: {tools}\n\nUse-as quando necessário para fornecer informações precisas.",
        "format": """Ao responder, siga esta estrutura em português:

ANÁLISE: Sua compreensão da questão
AÇÃO: Passos que você tomará
RESULTADO: Sua resposta final

Use linguagem profissional mas acessível."""
    }
}
```

### Exemplo 3: Agente de Análise Financeira

```python
finance_system_template = """Você é {role}. {backstory}

Seu objetivo: {goal}

DIRETRIZES ESPECÍFICAS PARA ANÁLISE FINANCEIRA:
- Sempre cite fontes de dados
- Use métricas financeiras padronizadas
- Apresente riscos e limitações
- Forneça recomendações acionáveis
- Mantenha conformidade regulatória

Responda com precisão técnica e clareza comercial."""

finance_agent = Agent(
    role="Analista Financeiro Sênior",
    goal="Fornecer análises financeiras precisas e acionáveis",
    backstory="Você é um CFA com 15 anos de experiência em mercados financeiros.",
    system_template=finance_system_template,
    use_system_prompt=True
)
```

## Checklist de Produção

### ✅ **Antes do Deploy**

- [ ] Inspecionar todos os prompts gerados
- [ ] Testar com modelos de produção
- [ ] Validar comportamento em cenários edge case
- [ ] Documentar todas as customizações
- [ ] Configurar monitoramento/observabilidade
- [ ] Revisar conformidade e segurança

### ✅ **Durante Produção**

- [ ] Monitorar performance de prompts
- [ ] Coletar feedback de usuários
- [ ] Acompanhar métricas de qualidade
- [ ] Detectar anomalias comportamentais
- [ ] Manter logs de prompt para auditoria

### ✅ **Manutenção Contínua**

- [ ] Revisar prompts periodicamente
- [ ] Atualizar para novos modelos
- [ ] Otimizar com base em dados de uso
- [ ] Manter compatibilidade com atualizações do CrewAI
- [ ] Treinar equipe em melhores práticas

## Dicas Avançadas

### 🎯 **Otimização de Performance**

```python
# Use caching para prompts frequentes
@lru_cache(maxsize=128)
def get_optimized_prompt(model_type, domain, language):
    return load_prompt_template(model_type, domain, language)
```

### 🔄 **Versionamento de Prompts**

```python
# Mantenha versões de prompts para rollback
PROMPT_VERSIONS = {
    "v1.0": "prompts/v1/agent_prompts.json",
    "v1.1": "prompts/v1.1/agent_prompts.json",
    "v2.0": "prompts/v2/agent_prompts.json"
}
```

### 🧪 **A/B Testing de Prompts**

```python
# Teste diferentes versões de prompts
import random

def get_prompt_variant():
    variants = ["prompt_v1.json", "prompt_v2.json"]
    return random.choice(variants)
```

## Recursos Adicionais

- [Documentação Oficial do CrewAI](https://docs.crewai.com/pt-BR/guides/advanced/customizing-prompts)
- [Templates de Prompt no GitHub](https://github.com/crewAIInc/crewAI/tree/main/src/crewai/utilities/prompts)
- [Guia de Observabilidade](./OBSERVABILIDADE.md)
- [Exemplos de Integração](../aula4/main.py)

---

## Conclusão

A personalização de prompts no CrewAI é uma ferramenta poderosa que permite criar agentes altamente especializados e eficientes. Seguindo as práticas descritas neste guia, você pode:

- Obter controle total sobre o comportamento dos agentes
- Otimizar para diferentes modelos e casos de uso
- Manter transparência e qualidade em produção
- Escalar soluções de forma sustentável

Lembre-se: **transparência, documentação e monitoramento** são fundamentais para o sucesso em produção.

---

*Guia criado com base na documentação oficial do CrewAI v0.80.0+*
*Última atualização: Janeiro 2025*
