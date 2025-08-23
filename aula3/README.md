# Aula 3: Ferramentas (Tools) e Processos (Processes) no CrewAI

## 🎯 Objetivos da Aula

Esta aula ensina como equipar agentes com ferramentas e comparar diferentes processos de execução. Você aprenderá a:

- Entender o conceito de ferramentas (Tools) no CrewAI
- Implementar simulações de ferramentas para demonstração
- Entender a diferença entre processos Sequencial e Hierárquico
- Implementar coordenação avançada com managers
- Saber quando usar cada tipo de processo

## 🔧 Ferramentas Demonstradas (Simuladas)

### 1. Simulação de Busca Web

- **Função**: Simula busca inteligente na web
- **Uso**: Demonstra como agentes fariam pesquisas online
- **Vantagem**: Não requer APIs externas

### 2. Simulação de Scraping

- **Função**: Simula extração de conteúdo de websites
- **Uso**: Demonstra análise de conteúdo de páginas
- **Vantagem**: Funciona offline para demonstração

### 3. Simulação de Leitura de Arquivos

- **Função**: Simula leitura de arquivos locais
- **Uso**: Demonstra processamento de documentos locais
- **Formato**: Simula suporte a texto, markdown, CSV, etc.

## 🤖 Agentes Implementados

### 1. Pesquisador Web Avançado

- **Papel**: Coletar informações usando ferramentas simuladas
- **Ferramentas**: Simulações de busca e scraping
- **Especialidade**: Pesquisa fundamentada com fontes simuladas

### 2. Redator Técnico Especializado

- **Papel**: Criar conteúdo técnico claro
- **Especialidade**: Transformar pesquisa em artigos
- **Foco**: Linguagem técnica mas acessível

### 3. Revisor Crítico e Analista

- **Papel**: Validar qualidade do conteúdo
- **Especialidade**: Análise crítica e feedback
- **Resultado**: Sugestões específicas de melhoria

### 4. Gerente de Projeto Editorial (Hierárquico)

- **Papel**: Coordenar equipe e delegar tarefas
- **Especialidade**: Otimização de fluxo de trabalho
- **Responsabilidade**: Garantir qualidade final

## 🔄 Processos Comparados

### Processo Sequencial

```text
1. Pesquisador → Coleta informações
         ↓
2. Redator → Cria artigo baseado na pesquisa
         ↓
3. Revisor → Analisa e sugere melhorias
```

**Características:**

- ✅ Execução linear e previsível
- ✅ Fácil de debugar e acompanhar
- ✅ Ideal para fluxos bem definidos
- ✅ Menor complexidade de coordenação
- ❌ Pode ser mais lento
- ❌ Menos flexibilidade

**Quando usar:**

- Projetos com fluxo claro e linear
- Aprendizado e prototipagem
- Quando previsibilidade é importante

### Processo Hierárquico

```text
      Manager (Coordenador)
           |
    ┌──────┼──────┐
    ↓      ↓      ↓
Pesquisador → Redator → Revisor
    ↑__________________|
    (Delegação otimizada)
```

**Características:**

- ✅ Execução otimizada e inteligente
- ✅ Delegação baseada em capacidades
- ✅ Pode executar tarefas em paralelo
- ✅ Ideal para projetos complexos
- ❌ Requer LLM adicional para manager
- ❌ Maior complexidade de setup

**Quando usar:**

- Projetos complexos com múltiplas dependências
- Quando otimização de tempo é crítica
- Equipes grandes com especialidades distintas

## 🚀 Como Executar

### Pré-requisitos

1. Chave OpenAI configurada no `.env`
2. CrewAI instalado: `uv add crewai`

### Executar o Script

```bash
uv run python aula3/main.py
```

### Opções de Execução

1. **Processo Sequencial** - Recomendado para iniciantes
2. **Processo Hierárquico** - Mais avançado
3. **Comparação Completa** - Executa ambos (demora mais)
4. **Apenas Conceitos** - Demonstração sem execução

## 💡 Conceitos Aprendidos

### Ferramentas (Tools)

- **Expansão de Capacidades**: Agentes ganham habilidades específicas
- **Integração Externa**: Conexão com APIs, web, arquivos
- **Configuração**: Cada ferramenta tem seus parâmetros
- **Combinação**: Agentes podem usar múltiplas ferramentas

### Processos (Processes)

- **Sequencial**: Execução linear, uma tarefa por vez
- **Hierárquico**: Coordenação inteligente com delegação
- **Escolha Estratégica**: Depende do tipo de projeto
- **Performance**: Hierárquico pode ser mais eficiente

### Coordenação

- **Managers**: Agentes especializados em coordenação
- **Delegação**: Atribuição inteligente de tarefas
- **Allow_delegation**: Parâmetro crucial para hierarchical
- **LLM do Manager**: Pode ser diferente dos outros agentes

## 🔧 Configuração Avançada

### Variáveis de Ambiente Necessárias

```bash
# .env
OPENAI_API_KEY=sua_chave_openai
SERPER_API_KEY=sua_chave_serper  # Opcional para busca web
```

### Obtendo Chave Serper

1. Acesse <https://serper.dev/>
2. Crie conta gratuita
3. Obtenha sua API key
4. Adicione no arquivo `.env`

### Configuração de Simulações

```python
# Simulação com configurações customizadas
def simular_busca_personalizada(query, country="BR", language="pt"):
    return f"Resultados simulados para '{query}' em {country} ({language})\n- Resultado localizado 1\n- Resultado localizado 2"
```

## 🔍 Troubleshooting

### Erro: "Serper API key not found"

- Configure `SERPER_API_KEY` no `.env`
- Ou execute no modo apenas conceitos (opção 4)

### Erro: "Manager LLM failed"

- Verifique se tem créditos OpenAI suficientes
- Consider usar `gpt-3.5-turbo` em vez de `gpt-4`

### Performance lenta

- Use processo sequencial para projetos simples
- Verifique conexão com internet para ferramentas web

### Erro de importação de ferramentas

```bash
pip install --upgrade crewai-tools
```

## 📊 Comparação Prática

| Aspecto | Sequencial | Hierárquico |
|---------|------------|-------------|
| **Velocidade** | Moderada | Otimizada |
| **Complexidade** | Baixa | Alta |
| **Previsibilidade** | Alta | Moderada |
| **Flexibilidade** | Baixa | Alta |
| **Debug** | Fácil | Complexo |
| **Custo LLM** | Menor | Maior |
| **Coordenação** | Simples | Avançada |
| **Paralelização** | Não | Possível |

## 🎓 Próximos Passos

Na próxima aula, aprenderemos sobre:

- Arquitetura de Chatbots Multi-Agente
- Design de fluxos conversacionais
- Gerenciamento de contexto e memória
- Integração com interfaces de usuário

## 💡 Dicas Importantes

1. **Comece Simples**: Use processo sequencial para aprender
2. **Teste Ferramentas**: Experimente diferentes combinações
3. **Monitor Custos**: Processo hierárquico usa mais tokens
4. **Backup Plans**: Sempre tenha fallbacks para APIs externas
5. **Documentação**: Anote quais ferramentas funcionam melhor para cada caso

---

**🚀 Ferramentas tornam agentes realmente poderosos! Experimente e descubra as possibilidades infinitas.**
