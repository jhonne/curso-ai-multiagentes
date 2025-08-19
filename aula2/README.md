# Aula 2: Construindo seu Primeiro Crew - Agentes e Tarefas

## 🎯 Objetivos da Aula

Esta aula ensina como criar e organizar um **Crew** completo com múltiplos agentes colaborando em tarefas sequenciais. Você aprenderá a:

- Definir agentes com papéis específicos e complementares
- Criar tarefas com descrições claras e resultados esperados
- Organizar um fluxo de trabalho sequencial
- Ver agentes colaborando em um projeto complexo

## 🤖 Agentes Implementados

### 1. Pesquisador Especialista

- **Papel**: Coletar informações detalhadas e precisas
- **Especialidade**: Análise e organização de dados
- **Comportamento**: Busca múltiplas perspectivas antes de concluir

### 2. Redator e Editor Criativo

- **Papel**: Transformar informações brutas em conteúdo envolvente
- **Especialidade**: Narrativas claras e bem estruturadas
- **Comportamento**: Adapta tom e estilo para o público-alvo

## 📋 Tarefas Definidas

### Tarefa 1: Pesquisa sobre IA na Educação

- Coleta informações sobre benefícios, ferramentas, desafios e tendências
- Organiza dados de forma estruturada
- Fornece base sólida para o trabalho do redator

### Tarefa 2: Criação de Artigo

- Transforma a pesquisa em artigo envolvente (800-1000 palavras)
- Organiza conteúdo em seções lógicas
- Usa linguagem acessível para educadores

### Tarefa 3: Resumo Executivo

- Cria versão concisa para gestores ocupados
- Destaca pontos-chave em bullet points
- Máximo de 200 palavras

## 🔄 Fluxo de Trabalho

```text
1. PESQUISADOR → Coleta informações sobre IA na educação
           ↓
2. REDATOR → Cria artigo baseado na pesquisa
           ↓
3. REDATOR → Produz resumo executivo do artigo
```

## 🚀 Como Executar

1. Certifique-se de que sua chave OpenAI está configurada no arquivo `.env`
2. Execute o script:

   ```bash
   python aula2/main.py
   ```

## 💡 Conceitos Aprendidos

- **Agentes Especializados**: Cada agente tem um papel bem definido
- **Colaboração Sequencial**: Saída de um agente alimenta o próximo
- **Descrições Detalhadas**: Tarefas com contexto rico para melhor performance
- **Resultados Esperados**: Definição clara do que cada tarefa deve produzir

## 🔍 Observações Importantes

- Use `verbose=True` para acompanhar o processo de pensamento dos agentes
- Defina `backstories` ricas para guiar o comportamento dos agentes
- Especifique `expected_output` detalhado para melhor qualidade dos resultados
- O processo sequencial garante que cada agente tenha acesso ao trabalho anterior

## 🎓 Próximos Passos

Na próxima aula, aprenderemos sobre:

- Ferramentas (Tools) para agentes
- Processos mais complexos
- Integração com APIs externas
- Otimização de performance

---

**Dica**: Experimente modificar as descrições das tarefas ou os backstories dos agentes para ver como isso afeta o resultado final!
