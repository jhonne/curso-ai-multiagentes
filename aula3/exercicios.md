# Exercícios Práticos - Aula 3: Ferramentas e Processos

## 🎯 Exercícios para Praticar

### Exercício 1: Comparação de Simulações de Ferramentas

**Objetivo:** Testar diferentes simulações de ferramentas e comparar seus resultados

```python
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# Simulações de ferramentas
def simular_pesquisa_web(query):
    return f"Resultados de pesquisa simulados para: {query}\n- Resultado 1\n- Resultado 2"

def simular_leitura_arquivo(file_path):
    return f"Conteúdo simulado do arquivo {file_path}\nInformações relevantes aqui..."

# Crie um agente que:
# 1. Use simulação de pesquisa para buscar "Python FastAPI tutorial"
# 2. Use simulação de leitura para o README.md do projeto
# 3. Compare as informações obtidas
# 4. Crie um relatório comparativo

# SEU CÓDIGO AQUI
```

### Exercício 2: Processo Sequencial com Simulações

**Objetivo:** Criar sua própria sequência de agentes com simulações de ferramentas

**Desafio:**

- Agente 1: Pesquisador que busca informações sobre uma tecnologia usando simulação
- Agente 2: Analista que examina vantagens e desvantagens  
- Agente 3: Consultor que cria recomendações práticas

```python
# Implemente:
# 1. Três agentes especializados
# 2. Tarefas bem definidas para cada um
# 3. Processo sequencial
# 4. Use pelo menos 2 simulações de ferramentas diferentes

# SEU CÓDIGO AQUI
```

### Exercício 3: Experimento com Processo Hierárquico

**Objetivo:** Implementar e testar processo hierárquico

**Requisitos:**

- Um manager que coordena a equipe
- Pelo menos 3 agentes especialistas
- Tarefa complexa que se beneficia de delegação
- Comparar tempo de execução com processo sequencial

```python
# Dicas:
# - Use allow_delegation=True no manager
# - Defina tarefas genéricas para o manager
# - Compare com versão sequencial

# SEU CÓDIGO AQUI
```

### Exercício 4: Simulações Personalizadas

**Objetivo:** Criar simulações de ferramentas personalizadas

```python
# Exemplo de simulação personalizada
def minha_simulacao_personalizada(argumento):
    """Simulação de ferramenta personalizada"""
    return f"Resultado processado para: {argumento}\nDados simulados específicos aqui..."

def simular_api_externa(endpoint, params):
    """Simula chamada para API externa"""
    return {
        "status": "success",
        "data": f"Dados simulados da API {endpoint} com parâmetros {params}",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Use suas simulações personalizadas em um agente
# SEU CÓDIGO AQUI
```

## 💡 Desafios Avançados

### Desafio 1: Sistema de Pesquisa Inteligente com Simulações

Crie um sistema que:

1. Simule pesquisa de um tópico na web
2. Simule extração de conteúdo de 3 sites diferentes
3. Compare as informações simuladas
4. Crie um relatório consolidado
5. Identifique contradições ou lacunas nas simulações

### Desafio 2: Pipeline de Conteúdo com Simulações

Implemente um pipeline completo:

1. Simulação de pesquisa de mercado
2. Análise de tendências (agente analista)
3. Criação de conteúdo (agente redator)
4. Revisão técnica (agente revisor)
5. Formatação final (agente formatador)

### Desafio 3: Otimização de Performance

Compare performance entre:

- Processo sequencial vs hierárquico
- Uso de simulações vs sem simulações
- Diferentes configurações de agentes
- Medições de tempo de execução

## 🔧 Soluções dos Exercícios

### Solução Exercício 1

```python
# Exemplo de solução - adapte conforme necessário

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# Simulações de ferramentas
def simular_pesquisa_web(query):
    return f"Resultados simulados para: {query}\n- Tutorial FastAPI oficial\n- Documentação atualizada"

def simular_leitura_arquivo(file_path):
    return f"Conteúdo simulado de {file_path}:\n# FastAPI Project\n\nDescrição do projeto..."

# Agente comparador
agente_comparador = Agent(
    role='Analista Comparativo',
    goal='Comparar informações de diferentes fontes usando simulações',
    backstory='Especialista em análise comparativa de informações simuladas',
    verbose=True
)

# Tarefa de comparação
tarefa_comparacao = Task(
    description="""Compare informações sobre Python FastAPI:
    1. Pesquise na web sobre FastAPI tutorial
    2. Leia documentação local (se disponível)
    3. Compare as fontes
    4. Identifique diferenças e semelhanças""",
    expected_output="Relatório comparativo detalhado",
    agent=agente_comparador
)

# Crew
crew = Crew(
    agents=[agente_comparador],
    tasks=[tarefa_comparacao],
    process=Process.sequential
)

# Executar
resultado = crew.kickoff()
print(resultado)
```

## 📝 Checklist de Aprendizado

Após completar os exercícios, você deve ser capaz de:

- [ ] Configurar diferentes ferramentas do CrewAI
- [ ] Equipar agentes com múltiplas ferramentas
- [ ] Implementar processo sequencial
- [ ] Implementar processo hierárquico
- [ ] Comparar performance entre processos
- [ ] Identificar quando usar cada tipo de processo
- [ ] Criar ferramentas personalizadas básicas
- [ ] Debugar problemas com ferramentas
- [ ] Otimizar uso de recursos e custos

## 🎓 Próximos Passos

1. **Pratique** os exercícios básicos
2. **Experimente** os desafios avançados  
3. **Documente** suas descobertas
4. **Compare** diferentes abordagens
5. **Prepare-se** para a próxima aula sobre Chatbots Multi-Agente

---

**💡 Lembre-se:** A prática leva à perfeição. Experimente diferentes combinações e descubra o que funciona melhor para seus casos de uso!
