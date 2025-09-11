# 📚 Exercícios Práticos - Aula 5: Otimização e Configuração Avançada

## 🎯 Objetivos dos Exercícios

Estes exercícios foram projetados para consolidar o aprendizado da Aula 5, cobrindo:

- Engenharia de prompts avançada
- Configuração otimizada de modelos OpenAI
- Implementação de testes e monitoramento
- Aplicação prática dos conceitos em cenários reais

---

## 🏋️ BLOCO 1: Engenharia de Prompts Avançada

### Exercício 1.1: Prompt Básico vs Otimizado ⭐

**Dificuldade:** Iniciante  
**Tempo estimado:** 20 minutos

**Cenário:** Você precisa criar um agente para analisar feedback de produtos de e-commerce.

**Tarefas:**

1. Crie um agente com prompt básico (exemplo: "Analise este feedback")
2. Crie outro agente com prompt otimizado usando:
   - Contexto específico
   - Formato estruturado de resposta
   - Exemplo prático (few-shot learning)
3. Teste ambos com o feedback: *"Produto chegou rápido mas veio com defeito, atendimento foi prestativo para resolver"*
4. Compare os resultados e documente as diferenças

**Critérios de avaliação:**

- ✅ Prompt otimizado é mais específico e estruturado
- ✅ Resposta do agente otimizado é mais consistente
- ✅ Documentação clara das diferenças observadas

### Exercício 1.2: Chain-of-Thought Prompting ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 30 minutos

**Cenário:** Criar um agente analista que precisa tomar decisões baseadas em múltiplos fatores.

**Tarefas:**

1. Implemente um agente que usa chain-of-thought para analisar viabilidade de projetos
2. O agente deve seguir estes passos:
   - **Passo 1:** Analisar investimento necessário
   - **Passo 2:** Avaliar retorno esperado
   - **Passo 3:** Considerar riscos envolvidos
   - **Passo 4:** Dar recomendação final (APROVADO/REJEITADO/REVISAR)
3. Teste com: *"Projeto: App de delivery. Investimento: R$ 50mil. Retorno estimado: R$ 15mil/mês. Mercado saturado, alta concorrência."*

**Critérios de avaliação:**

- ✅ Agente segue todos os 4 passos sequencialmente
- ✅ Cada passo é claramente identificado na resposta
- ✅ Recomendação final é justificada pelos passos anteriores

### Exercício 1.3: Otimização para Redução de Tokens ⭐⭐⭐

**Dificuldade:** Avançado  
**Tempo estimado:** 40 minutos

**Cenário:** Reduzir custos de operação otimizando prompts para usar menos tokens.

**Tarefas:**

1. Crie um agente para classificação de urgência de tickets de suporte
2. Otimize o prompt para gerar respostas ultra-concisas
3. Configure `max_tokens=50` e mantenha qualidade da resposta
4. Teste com diferentes tipos de tickets:
   - *"Sistema fora do ar há 3 horas, perdendo vendas"*
   - *"Como alterar minha senha?"*
   - *"Sugestão: adicionar modo escuro no app"*
5. Calcule tokens economizados comparado com prompt verboso

**Critérios de avaliação:**

- ✅ Respostas consistem em formato ultra-conciso (ex: "🔴 ALTA | Sistema crítico | Ação: Escalar para DevOps")
- ✅ Classificação de urgência está correta
- ✅ Economia de tokens de pelo menos 60% comparado com versão verbosa

---

## ⚙️ BLOCO 2: Configuração de Modelos OpenAI

### Exercício 2.1: Agentes Especializados por Cenário ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 45 minutos

**Cenário:** Configurar agentes com parâmetros específicos para diferentes tarefas de uma empresa.

**Tarefas:**

1. **Agente Criativo (Marketing):**
   - Configure para alta criatividade (temperature=0.9)
   - Use GPT-4 para qualidade superior
   - Teste gerando campanha para "lançamento de tênis esportivo sustentável"

2. **Agente Analítico (Financeiro):**
   - Configure para precisão (temperature=0.1)
   - Use GPT-3.5-turbo para economia
   - Teste analisando: "Receita: R$ 120k, Custos: R$ 95k, Meta: 30% margem"

3. **Agente Conversacional (Atendimento):**
   - Configure balanceado (temperature=0.7)
   - Limite max_tokens=300 para agilidade
   - Teste respondendo: "Cliente reclama que produto não chegou"

**Critérios de avaliação:**

- ✅ Cada agente tem configuração apropriada para sua função
- ✅ Respostas refletem o perfil configurado (criativo/analítico/conversacional)
- ✅ Documentação justifica escolha de parâmetros

### Exercício 2.2: Sistema de Fallback Robusto ⭐⭐⭐

**Dificuldade:** Avançado  
**Tempo estimado:** 50 minutos

**Cenário:** Implementar sistema que garante disponibilidade mesmo com falhas de API.

**Tarefas:**

1. Implemente função que tenta modelos em ordem:
   - **Primário:** GPT-4 (qualidade alta)
   - **Fallback 1:** GPT-3.5-turbo (economia)
   - **Fallback 2:** Resposta pré-definida (disponibilidade)
2. Simule falhas de API e teste a recuperação
3. Registre qual método foi usado em cada execução
4. Calcule economia de custos com o sistema de fallback

**Critérios de avaliação:**

- ✅ Sistema recupera graciosamente de falhas
- ✅ Logs indicam claramente qual modelo foi usado
- ✅ Resposta pré-definida é acionada como último recurso
- ✅ Cálculo de economia é documentado

### Exercício 2.3: Análise de Custo-Benefício ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 35 minutos

**Cenário:** Otimizar custos sem comprometer qualidade para um chatbot de e-commerce.

**Tarefas:**

1. Compare custos GPT-4 vs GPT-3.5-turbo para:
   - 1000 consultas simples (FAQ)
   - 500 consultas complexas (análise de problemas)
   - 200 consultas criativas (recomendações personalizadas)
2. Teste qualidade de ambos os modelos
3. Proponha estratégia híbrida otimizada
4. Projete economia mensal para volume de 10.000 consultas

**Critérios de avaliação:**

- ✅ Cálculos de custo estão corretos
- ✅ Estratégia híbrida é bem justificada
- ✅ Projeção considera qualidade vs custo
- ✅ Recomendação é prática e implementável

---

## 🧪 BLOCO 3: Testes e Debugging

### Exercício 3.1: Suite de Testes Unitários ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 40 minutos

**Cenário:** Criar testes robustos para um agente classificador de sentimentos.

**Tarefas:**

1. Crie agente que classifica sentimento como POSITIVO/NEGATIVO/NEUTRO
2. Implemente pelo menos 8 casos de teste:
   - 3 feedbacks claramente positivos
   - 3 feedbacks claramente negativos  
   - 2 feedbacks neutros/ambíguos
3. Adicione testes de:
   - Tempo de resposta (< 30 segundos)
   - Consistência (mesmo input, mesmo output)
   - Configuração correta do agente
4. Execute com pytest e alcance 100% de sucesso

**Critérios de avaliação:**

- ✅ Todos os testes passam
- ✅ Casos de teste cobrem cenários diversos
- ✅ Testes de performance e consistência incluídos
- ✅ Código de teste é bem estruturado

### Exercício 3.2: Debugging com Verbose Mode ⭐

**Dificuldade:** Iniciante  
**Tempo estimado:** 25 minutos

**Cenário:** Diagnosticar por que um agente está dando respostas inconsistentes.

**Tarefas:**

1. Crie agente para calcular desconto em vendas
2. Configure `verbose=True` para ver processo de raciocínio
3. Teste com: *"Cliente VIP comprou R$ 500 em produtos, aplique desconto apropriado"*
4. Analise logs e identifique pontos de melhoria
5. Otimize o prompt baseado nos insights do debugging

**Critérios de avaliação:**

- ✅ Usa verbose mode efetivamente
- ✅ Identifica problemas específicos nos logs
- ✅ Implementa melhorias baseadas no debugging
- ✅ Documenta o processo de otimização

### Exercício 3.3: Validação de Qualidade Automática ⭐⭐⭐

**Dificuldade:** Avançado  
**Tempo estimado:** 55 minutos

**Cenário:** Implementar sistema que avalia automaticamente qualidade das respostas.

**Tarefas:**

1. Crie função que avalia respostas baseada em critérios:
   - **Completude:** Resposta aborda todos os pontos solicitados
   - **Clareza:** Linguagem é clara e compreensível
   - **Precisão:** Informações estão corretas
   - **Formato:** Segue estrutura solicitada
2. Implemente sistema de pontuação (0-100)
3. Teste com 10 respostas diferentes
4. Crie alertas para respostas com pontuação < 70

**Critérios de avaliação:**

- ✅ Sistema de avaliação é objetivo e consistente
- ✅ Critérios são claramente definidos e mensuráveis
- ✅ Pontuação reflete qualidade real das respostas
- ✅ Sistema de alertas funciona corretamente

---

## 📊 BLOCO 4: Monitoramento e Métricas

### Exercício 4.1: Dashboard de Monitoramento ⭐⭐⭐

**Dificuldade:** Avançado  
**Tempo estimado:** 60 minutos

**Cenário:** Criar sistema completo de monitoramento para múltiplos agentes em produção.

**Tarefas:**

1. Implemente classe `MonitorDashboard` que rastreie:
   - Número de execuções por agente
   - Tempo médio de resposta
   - Taxa de sucesso/falha
   - Uso total de tokens
   - Custo acumulado
2. Adicione alertas automáticos para:
   - Tempo de resposta > 30s
   - Taxa de falha > 10%
   - Custo diário > $10
3. Gere relatório executivo com gráficos ASCII
4. Teste com simulação de 50 execuções

**Critérios de avaliação:**

- ✅ Sistema captura todas as métricas solicitadas
- ✅ Alertas são acionados corretamente
- ✅ Relatório é claro e informativo
- ✅ Código é bem estruturado e documentado

### Exercício 4.2: Cache Inteligente com TTL ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 45 minutos

**Cenário:** Implementar cache que otimiza custos reutilizando respostas similares.

**Tarefas:**

1. Crie sistema de cache com:
   - TTL (Time To Live) configurável
   - Hash inteligente para prompts similares
   - Limpeza automática de entradas expiradas
2. Configure TTL de 1 hora para testes
3. Implemente métricas: hit rate, miss rate, economia estimada
4. Teste com 20 prompts (alguns repetidos) e documente economia

**Critérios de avaliação:**

- ✅ Cache funciona corretamente com TTL
- ✅ Sistema de hash detecta prompts similares
- ✅ Métricas são precisas e informativas
- ✅ Economia real de tokens é demonstrada

### Exercício 4.3: Sistema de Alertas Proativos ⭐⭐

**Dificuldade:** Intermediário  
**Tempo estimado:** 40 minutos

**Cenário:** Criar alertas que detectam problemas antes que afetem usuários.

**Tarefas:**

1. Implemente diferentes tipos de alerta:
   - **🚨 CRÍTICO:** Sistema fora do ar
   - **⚠️ AVISO:** Performance degradada
   - **💰 CUSTO:** Gastos acima do orçamento
   - **🔄 INFO:** Uso normal do sistema
2. Configure limites para cada tipo
3. Teste com cenários simulados
4. Implemente histórico de alertas com timestamp

**Critérios de avaliação:**

- ✅ Diferentes níveis de alerta funcionam corretamente
- ✅ Limites são configuráveis e apropriados
- ✅ Histórico de alertas é mantido
- ✅ Sistema é proativo, não apenas reativo

---

## 🚀 PROJETO FINAL: Sistema Completo de Chatbot Otimizado

### Desafio Integrado ⭐⭐⭐⭐

**Dificuldade:** Expert  
**Tempo estimado:** 3-4 horas

**Cenário:** Desenvolver chatbot completo para loja online com todos os conceitos da Aula 5.

**Especificações:**

1. **Agentes especializados:**
   - Triagem (classifica tipo de consulta)
   - Vendas (recomendações de produtos)
   - Suporte (resolve problemas técnicos)
   - Satisfação (coleta feedback)

2. **Otimizações obrigatórias:**
   - Prompts otimizados com few-shot learning
   - Configurações específicas por agente
   - Sistema de fallback completo
   - Cache inteligente para consultas repetidas

3. **Monitoramento completo:**
   - Dashboard em tempo real
   - Alertas proativos
   - Métricas de qualidade
   - Controle de custos

4. **Testes robustos:**
   - Suite de testes para cada agente
   - Testes de integração
   - Validação de performance
   - Monitoramento de qualidade

**Entregáveis:**

- ✅ Código fonte completo e documentado
- ✅ Relatório de testes com 95%+ de sucesso
- ✅ Dashboard de monitoramento funcionando
- ✅ Documentação de economia de custos
- ✅ Plano de deployment em produção

---

## 📋 Lista de Verificação Final

### Para cada exercício, certifique-se de

- [ ] **Código funciona** sem erros
- [ ] **Documentação** explica decisões tomadas
- [ ] **Testes** validam funcionamento
- [ ] **Métricas** são coletadas e analisadas
- [ ] **Otimizações** são mensuráveis

### Critérios de qualidade

- [ ] **Legibilidade:** Código limpo e bem comentado
- [ ] **Robustez:** Trata erros graciosamente
- [ ] **Performance:** Tempos de resposta aceitáveis
- [ ] **Economia:** Uso eficiente de tokens
- [ ] **Escalabilidade:** Design permite crescimento

---

## 🎯 Objetivos de Aprendizado

Ao completar estes exercícios, você será capaz de:

1. ✅ **Criar prompts otimizados** que reduzem custos e melhoram qualidade
2. ✅ **Configurar modelos** apropriadamente para diferentes cenários
3. ✅ **Implementar testes robustos** que garantem qualidade
4. ✅ **Monitorar sistemas** proativamente em produção
5. ✅ **Otimizar custos** sem comprometer funcionalidade
6. ✅ **Debuggar problemas** eficientemente usando ferramentas adequadas

---

## 💡 Dicas de Sucesso

### 🎯 **Planejamento:**

- Leia todo o exercício antes de começar
- Estime tempo necessário e organize seu cronograma
- Prepare ambiente de desenvolvimento antes de começar

### 🔧 **Execução:**

- Teste incrementalmente (não espere até o final)
- Documente decisões e aprendizados
- Use `verbose=True` para debugging quando necessário

### 📊 **Validação:**

- Execute todos os testes antes de considerar concluído
- Verifique se métricas fazem sentido
- Compare resultados com objetivos esperados

### 🚀 **Otimização:**

- Meça antes de otimizar
- Foque no que gera maior impacto
- Mantenha qualidade enquanto reduz custos

---

**🎓 Boa sorte com os exercícios! Lembre-se: a otimização é um processo iterativo. Teste, monitore, aprenda e melhore continuamente!**
