# Aula 6 - Exercícios Práticos

## 🎯 Objetivo dos Exercícios

Estes exercícios vão te ajudar a dominar os conceitos de orquestração de agentes e gerenciamento de fluxo de conversa.

⚠️ **IMPORTANTE**: Execute sempre usando `uv run` a partir da raiz do projeto.

## 📋 Lista de Exercícios

### Exercício 1: Executar e Entender (Básico)

**Objetivo:** Familiarizar-se com o sistema básico

**Passos:**

1. Execute `uv run aula6/exemplo_basico.py`
2. Observe como os agentes se comunicam
3. Teste com estas perguntas:
   - "Como funciona uma rede neural?"
   - "Preciso de ajuda com programação"
   - "Qual é a melhor linguagem para iniciantes?"

**O que observar:**

- Como cada agente processa a informação
- Como o contexto passa de um agente para outro
- Diferenças nas respostas para diferentes tipos de pergunta

---

### Exercício 2: Modificar Personalidades (Intermediário)

**Objetivo:** Aprender como agentes especializados afetam o resultado

**Tarefa:**

1. Abra `agentes.py`
2. Modifique a personalidade do agente de resposta para ser:
   - Mais técnico e detalhado
   - OU mais casual e amigável
   - OU focado em exemplos práticos

3. Teste a mesma pergunta antes e depois da modificação

**Perguntas para teste:**

- "O que é machine learning?"

**Reflexão:**

- Como a mudança afetou a resposta?
- Qual versão você prefere e por quê?

---

### Exercício 3: Adicionar Novo Agente (Avançado)

**Objetivo:** Criar um agente especializado adicional

**Tarefa:**

1. Crie um novo agente "Validador" em `agentes.py`:

   ```python
   def criar_agente_validador():
       return Agent(
           role="Validador de Qualidade",
           goal="Verificar se a resposta atende aos padrões de qualidade",
           backstory="Você é um especialista em controle de qualidade...",
           verbose=True
       )
   ```

2. Adicione uma tarefa de validação em `tarefas.py`
3. Integre no fluxo do `orquestrador.py`

**Resultado esperado:**

- Sistema com 5 agentes em vez de 4
- Resposta final validada antes de ser entregue

---

### Exercício 4: Chatbot Especializado (Criativo)

**Objetivo:** Criar um chatbot para domínio específico

**Tarefa:**
Modifique o sistema para criar um chatbot especializado em UM dos temas:

- 🏥 Saúde e bem-estar
- 💰 Finanças pessoais  
- 🎓 Educação e estudos
- 🏠 Dicas domésticas

**Modificações necessárias:**

1. Ajustar as personalidades dos agentes para o domínio
2. Modificar as tarefas para focar no tema
3. Testar com perguntas relevantes

**Exemplo - Chatbot de Saúde:**

- Agente Triagem: Especialista em sintomas
- Agente Intenção: Psicólogo da saúde
- Agente Busca: Pesquisador médico
- Agente Resposta: Comunicador de saúde

---

### Exercício 5: Sistema de Histórico (Técnico)

**Objetivo:** Implementar memória entre conversas

**Tarefa:**

1. Modifique `orquestrador.py` para salvar conversas em arquivo
2. Implemente função para carregar histórico anterior
3. Adicione comando para consultar conversas passadas

**Funcionalidades:**

- Salvar cada conversa com timestamp
- Carregar conversas anteriores
- Buscar por palavra-chave no histórico

---

## 🎓 Exercícios de Reflexão

### Pergunta 1: Análise de Fluxo

**Questão:** Por que usamos 4 agentes em vez de apenas 1?

**Pontos para considerar:**

- Especialização vs generalização
- Qualidade da resposta
- Facilidade de manutenção
- Possibilidade de reutilização

### Pergunta 2: Ordem das Tarefas

**Questão:** O que aconteceria se mudássemos a ordem das tarefas?

**Experimento:**

1. Troque a ordem: Busca → Triagem → Intenção → Resposta
2. Execute e compare os resultados
3. Analise os problemas que surgem

### Pergunta 3: Escalabilidade

**Questão:** Como este sistema se comportaria com 100 usuários simultâneos?

**Considere:**

- Uso de recursos (CPU, memória)
- Tempo de resposta
- Custos de API
- Possíveis melhorias

---

## 🏆 Desafio Extra: Mini-Projeto

### Chatbot para E-commerce

**Objetivo:** Criar sistema completo para loja online

**Agentes necessários:**

1. **Atendente**: Recebe e classifica pedidos
2. **Consultor de Produtos**: Ajuda a escolher produtos
3. **Especialista em Pagamento**: Tira dúvidas sobre compras
4. **Pós-vendas**: Suporte após a compra

**Funcionalidades:**

- Responder dúvidas sobre produtos
- Ajudar no processo de compra
- Suporte pós-venda
- Direcionamento para humanos quando necessário

**Entregáveis:**

- Código funcional
- Exemplos de conversas
- Documentação de como usar
- Reflexão sobre melhorias

---

## 🔧 Dicas para Todos os Exercícios

### Debugging

- Use `verbose=True` para ver o que está acontecendo
- Teste com mensagens simples primeiro
- Verifique se as chaves de API estão configuradas

### Boas Práticas

- Mantenha os prompts claros e específicos
- Teste com diferentes tipos de entrada
- Documente suas modificações
- Faça backup antes de grandes mudanças

### Recursos Úteis

- Documentação oficial do CrewAI
- Exemplos das aulas anteriores
- Fórum da comunidade para dúvidas

---

## 📝 Entrega dos Exercícios

### O que entregar

1. **Código modificado** (quando aplicável)
2. **Screenshots** dos testes executados
3. **Relatório de reflexão** (1-2 páginas) contendo:
   - O que você aprendeu
   - Dificuldades encontradas
   - Ideias para melhorias
   - Aplicações práticas que você imagina

### Formato

- Crie uma pasta `meus_exercicios_aula6/`
- Organize os arquivos por exercício
- Inclua um `README.md` com suas reflexões

### Avaliação

- ✅ Execução correta dos exercícios básicos (60%)
- ✅ Qualidade das modificações (20%)
- ✅ Reflexões e análises (20%)

---

## 🎯 Próximos Passos

Após completar estes exercícios, você estará pronto para:

- **Aula 7**: Criar interfaces de usuário
- **Aula 8**: Implementar memória persistente  
- **Aula 9**: Debugging e otimização avançada

**Boa sorte com os exercícios! 🚀**
