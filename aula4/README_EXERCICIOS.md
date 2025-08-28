# 🎯 Exercícios Práticos - Aula 4: Cadeia de Agentes Especializados

Bem-vindos aos exercícios práticos da **Aula 4**! Aqui vocês irão implementar sistemas de **cadeia de agentes especializados**, aplicando todos os conceitos aprendidos sobre CrewAI com foco em **segurança**, **economia** e **especialização**.

## 📚 Conteúdo Disponível

### 📄 Arquivos Principais

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **`exercicios_alunos.md`** | Lista completa dos 4 exercícios com descrições | Visão geral dos exercícios |
| **`guia_implementacao.md`** | Guia detalhado de implementação | Implementação passo a passo |
| **`template_exercicios.py`** | Template base para começar | Ponto de partida para código |
| **`exemplo_exercicio1.py`** | Exemplo completo do Exercício 1 | Referência de implementação |

### 🎯 Os 4 Exercícios

1. **🟢 Análise de Currículo** (Fácil) - 3 agentes, 2-3 dias
2. **🟡 Planejamento de Viagem** (Médio) - 4 agentes, 4-5 dias  
3. **🟠 Criação de Conteúdo** (Avançado) - 5 agentes, 6-7 dias
4. **🔴 Suporte Técnico** (Expert) - 5+ agentes, 8-10 dias

## 🚀 Como Começar

### 1. **Escolha seu Exercício**

```bash
# Leia primeiro a descrição completa
cat exercicios_alunos.md

# Para implementação detalhada
cat guia_implementacao.md
```

### 2. **Use o Template Base**

```bash
# Copie o template para seu exercício
cp template_exercicios.py meu_exercicio1.py

# Edite e adapte para seu caso específico
```

### 3. **Veja o Exemplo Funcionando**

```bash
# Execute o exemplo completo do Exercício 1
python exemplo_exercicio1.py

# Escolha opção 1 para ver exemplos pré-definidos
```

## ⚡ Configuração Rápida

### Pré-requisitos

```bash
# 1. API Key configurada
$env:OPENAI_API_KEY="sua_chave_openai_aqui"

# 2. Dependências instaladas (já deve ter da aula)
uv sync

# 3. Testar conexão
uv run python ../teste_api.py
```

### Estrutura de Projeto Recomendada

```
seu_exercicio/
├── main.py              # Seu arquivo principal
├── config.py            # Configurações (LLM, custos)
├── agents.py            # Definições dos agentes
├── tasks.py             # Definições das tarefas
├── utils.py             # Utilitários (cache, validação)
├── data.py              # Base de dados simulada
└── README.md           # Sua documentação
```

## 💰 Práticas de Economia (OBRIGATÓRIAS)

### ✅ Configuração Básica

```python
# SEMPRE use gpt-4o-mini (85% mais barato)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=500  # Limite de custo
)

# SEMPRE monitore custos
monitor = MonitorCustos(orcamento=1.0)  # Orçamento baixo para testes
```

### ✅ Otimizações Avançadas

- **Cache inteligente**: Economiza 50% em queries similares
- **Backstories breves**: Máximo 200-300 caracteres
- **Expected outputs específicos**: Evita respostas longas
- **Verbose=False**: Reduz output desnecessário

## 🛡️ Práticas de Segurança (RECOMENDADAS)

### ✅ Validação de Entrada

```python
def validar_entrada(texto, max_chars=2000):
    if len(texto) > max_chars:
        raise ValueError("Entrada muito longa")
    # Adicione outras validações conforme necessário
```

### ✅ API de Moderação (Para Exercícios 3 e 4)

```python
def verificar_conteudo_seguro(texto):
    response = client.moderations.create(input=texto)
    return not response.results[0].flagged
```

## 📊 Expectativas de Custo

| Exercício | Custo por Execução | Custo 100 Execuções | Economia vs GPT-4o |
|-----------|-------------------|---------------------|-------------------|
| **1 - Currículo** | $0.005 - $0.015 | $0.50 - $1.50 | ~85% |
| **2 - Viagem** | $0.010 - $0.025 | $1.00 - $2.50 | ~85% |
| **3 - Conteúdo** | $0.015 - $0.035 | $1.50 - $3.50 | ~85% |
| **4 - Suporte** | $0.020 - $0.040 | $2.00 - $4.00 | ~85% |

*Custos com cache podem ser 50% menores*

## 🎯 Critérios de Avaliação

### ⭐ Básico (Nota 7-8)

- [ ] Sistema funciona sem erros
- [ ] Agentes comunicam corretamente
- [ ] Usa gpt-4o-mini
- [ ] Monitor de custos implementado

### ⭐⭐ Intermediário (Nota 8-9)

- [ ] Tudo do básico +
- [ ] Validação de entrada robusta
- [ ] Cache implementado
- [ ] Código bem organizado

### ⭐⭐⭐ Avançado (Nota 9-10)

- [ ] Tudo do intermediário +
- [ ] API de moderação (quando aplicável)
- [ ] Safety identifiers
- [ ] Testes automatizados
- [ ] Documentação completa

## 🔧 Troubleshooting Comum

### ❌ Problema: "API key not found"

```bash
# Solução
$env:OPENAI_API_KEY="sua_chave_aqui"
```

### ❌ Problema: "Agente não responde como esperado"

```python
# Solução: Revise backstory e expected_output
backstory="Descrição breve e específica"  # Máx 200 chars
expected_output="Output específico esperado"
```

### ❌ Problema: "Custo muito alto"

```python
# Solução: Verifique configurações
model="gpt-4o-mini"  # NÃO gpt-4o
max_tokens=500       # Limite baixo
verbose=False        # Reduz output
```

### ❌ Problema: "Context não funciona entre tarefas"

```python
# Solução: Use context corretamente
tarefa2 = Task(
    # ... configurações ...
    context=[tarefa1]  # Recebe output da tarefa1
)
```

## 📚 Recursos de Apoio

### 📖 Documentação Local

- `../docs/CREWAI_REFERENCE.md` - Referência completa do CrewAI
- `../docs/GUIA_SEGURANCA.md` - Práticas de segurança
- `../docs/RESUMO_OTIMIZACAO_OPENAI.md` - Otimização de custos

### 🌐 Documentação Online

- [CrewAI Official Docs](https://docs.crewai.com)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)

### 💻 Códigos de Referência

- `main.py` - Sistema completo de atendimento (da aula)
- `exemplo_simples.py` - Versão simplificada (da aula)
- `exemplo_exercicio1.py` - Exemplo do Exercício 1 (criado hoje)

## ⏰ Cronograma Sugerido

### 📅 Planejamento Individual

- **Semana 1**: Exercício 1 (Análise de Currículo)
- **Semana 2**: Exercício 2 (Planejamento de Viagem)  
- **Semana 3**: Exercício 3 (Criação de Conteúdo)
- **Semana 4**: Exercício 4 (Suporte Técnico)

### 📅 Planejamento Acelerado

- **Dia 1-2**: Exercício 1
- **Dia 3-4**: Exercício 2
- **Dia 5-7**: Exercício 3 ou 4 (escolha um)

## 🏆 Entrega dos Exercícios

### 📤 O que Entregar

Para cada exercício implementado:

1. **Código fonte** completo funcionando
2. **README.md** com instruções de execução
3. **Screenshots** de execuções bem-sucedidas
4. **Relatório de custos** (formato simples)
5. **Vídeo demonstração** (opcional, 2-3 min)

### 📊 Formato do Relatório de Custos

```markdown
# Relatório de Custos - [Nome do Exercício]

## Configuração
- Modelo: gpt-4o-mini
- Agentes: X agentes  
- Orçamento teste: $X.XX

## Resultados
- Execuções realizadas: X
- Custo total: $X.XXX
- Custo por execução: $X.XXX
- Economia vs GPT-4o: ~85%

## Otimizações Implementadas
- [x] Cache inteligente
- [x] Limites de output
- [x] Validação de entrada
- [x] Monitor de custos
```

## 🤝 Suporte e Colaboração

### 💬 Onde Pedir Ajuda

- **Erros de código**: Consulte os exemplos funcionando
- **Dúvidas conceituais**: Revise o conteúdo da aula 4
- **Problemas de API**: Verifique configuração da chave
- **Custos altos**: Revise configurações de economia

### 🔄 Iteração e Melhoria

1. **Comece simples**: Use o template base
2. **Teste constantemente**: Execute a cada mudança
3. **Itere gradualmente**: Adicione complexidade aos poucos
4. **Documente**: Registre o que funciona e o que não funciona

## 🎉 Dicas de Sucesso

### 💡 Para Melhor Qualidade

1. **Especialize os agentes**: Cada um deve ter uma função muito clara
2. **Context inteligente**: Passe apenas informações relevantes
3. **Expected outputs específicos**: Seja claro sobre o formato
4. **Teste casos extremos**: Entradas muito longas, muito curtas, inválidas

### 💰 Para Máxima Economia

1. **Sempre gpt-4o-mini**: Nunca use modelos mais caros para exercícios
2. **Cache agressivo**: Para queries similares (especialmente útil em testes)
3. **Limite outputs**: 500 tokens é suficiente para maioria dos casos
4. **Monitor ativo**: Pare se atingir 80% do orçamento

### 🛡️ Para Máxima Segurança  

1. **Valide tudo**: Nunca confie em entrada do usuário
2. **Limite tamanhos**: Evite inputs gigantescos
3. **Use moderação**: Especialmente em exercícios de conteúdo
4. **Trate erros**: Nunca deixe o sistema "quebrar"

---

## 🚀 Comece Agora

```bash
# 1. Execute o exemplo para ver como funciona
python exemplo_exercicio1.py

# 2. Copie o template e adapte para seu exercício
cp template_exercicios.py meu_exercicio.py

# 3. Consulte o guia detalhado conforme necessário
cat guia_implementacao.md

# 4. Implemente, teste e documente!
```

**🎯 Sucesso em seus exercícios! Lembrem-se: especialização + comunicação + economia = CrewAI eficiente!**

*Para dúvidas específicas, consultem os arquivos de referência ou executem os exemplos fornecidos. O foco é aprender fazendo!*
