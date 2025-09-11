# Aula 6: Gerenciando o Fluxo da Conversa e as Tarefas

## 🎯 Objetivos da Aula

- Aprender a orquestrar a interação entre múltiplos agentes
- Gerenciar o estado da conversa de forma simples
- Criar um chatbot funcional que conecta todos os agentes

## 📚 O Que Vamos Aprender

### 1. Conceitos Fundamentais

- **Orquestração de Agentes**: Como coordenar múltiplos agentes trabalhando juntos
- **Estado da Conversa**: Manter informações entre diferentes execuções
- **Fluxo de Tarefas**: Passar dados de um agente para outro de forma eficiente

### 2. Implementação Prática

- Criar um sistema que recebe entrada do usuário
- Processar a entrada através de múltiplos agentes especializados
- Retornar uma resposta coordenada e coerente

## 🏗️ Arquitetura do Sistema

```
Usuário → [Agente Triagem] → [Agente Intenção] → [Agente Busca] → [Agente Resposta] → Usuário
```

### Agentes Utilizados

1. **Agente de Triagem**: Recebe e classifica a mensagem do usuário
2. **Agente de Intenção**: Identifica o que o usuário realmente quer
3. **Agente de Busca**: Busca informações relevantes quando necessário
4. **Agente de Resposta**: Formula a resposta final

## 📁 Estrutura dos Arquivos

- `main.py` - Arquivo principal com exemplo completo
- `chatbot_simples.py` - Versão simplificada para aprendizado
- `agentes.py` - Definição dos agentes especializados
- `tarefas.py` - Definição das tarefas para cada agente
- `orquestrador.py` - Lógica de coordenação dos agentes
- `exemplo_basico.py` - Exemplo mínimo para começar

## 🚀 Como Executar

⚠️ **IMPORTANTE**: Este projeto usa UV para gerenciamento de dependências.
Execute os arquivos a partir da raiz do projeto usando `uv run`.

1. **Exemplo Básico** (recomendado para começar):

   ```bash
   uv run aula6/exemplo_basico.py
   ```

2. **Chatbot Simples**:

   ```bash
   uv run aula6/chatbot_simples.py
   ```

3. **Sistema Completo**:

   ```bash
   uv run aula6/main.py
   ```

## 📝 Exercícios Práticos

### Exercício 1: Executar o Exemplo Básico

- Execute `uv run aula6/exemplo_basico.py`
- Observe como os agentes se comunicam
- Teste com diferentes tipos de perguntas

### Exercício 2: Modificar Agentes

- Edite as personalidades dos agentes em `agentes.py`
- Teste como as mudanças afetam as respostas

### Exercício 3: Criar Novo Agente

- Adicione um novo agente especializado
- Integre ele ao fluxo de tarefas

## 🎓 Conceitos-Chave Para Entender

### 1. **Crew (Equipe)**

- Conjunto de agentes trabalhando juntos
- Cada agente tem uma função específica
- Coordenação através de tarefas sequenciais

### 2. **Task (Tarefa)**

- Unidade de trabalho atribuída a um agente
- Contém descrição, resultado esperado e contexto
- Pode usar resultados de tarefas anteriores

### 3. **Context (Contexto)**

- Informações compartilhadas entre agentes
- Mantém consistência na conversa
- Permite continuidade entre interações

## ⚠️ Pontos de Atenção

1. **Ordem das Tarefas**: A sequência importa muito
2. **Contexto Claro**: Cada tarefa deve ter contexto suficiente
3. **Resultados Bem Definidos**: Especifique claramente o que espera de cada agente
4. **Tratamento de Erros**: Sempre considere o que pode dar errado

## 🔄 Próximos Passos

Após dominar esta aula, você estará pronto para:

- **Aula 7**: Criar interfaces de usuário
- **Aula 8**: Adicionar memória persistente
- **Aula 9**: Debugging e otimização avançada

## 💡 Dicas de Boas Práticas

1. **Comece Simples**: Use o exemplo básico primeiro
2. **Teste Incrementalmente**: Adicione complexidade gradualmente
3. **Debug com Verbose**: Use `verbose=True` para ver o que acontece
4. **Monitore Custos**: Acompanhe o uso de tokens
5. **Use UV**: Execute sempre com `uv run` para garantir ambiente correto

---

**💡 Nota sobre UV**: Este projeto utiliza UV para gerenciamento de dependências moderno e eficiente.
Todos os comandos devem ser executados a partir da raiz do projeto usando `uv run`.
