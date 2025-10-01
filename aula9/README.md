# 🎓 Aula 9: CrewAI + Múltiplos Agentes Especializados

## 🎯 Objetivo

**EVOLUÇÃO da Aula 8**: Implementar um sistema multi-agente inteligente com **3 agentes especializados** que trabalham em coordenação hierárquica, cada um com expertise específica, demonstrando o poder da colaboração entre agentes CrewAI.

## ✨ Principais Novidades (Evolução da Aula 8)

- 🤖 **Sistema Multi-Agente** - 3 agentes especializados trabalhando juntos
- 🧠 **Agente Analisador** (NOVO!) - Classifica automaticamente o tipo de consulta
- 🏥 **Especialista em Saúde** (evoluído) - Estabelecimentos, queixas e visão geral
- 📊 **Especialista Estatístico** (NOVO!) - Análises numéricas e distribuição geográfica  
- 🔄 **Processo Hierarchical** - Coordenação inteligente entre agentes
- 🎯 **Delegação Automática** - Sistema decide qual agente deve responder
- 🛠️ **Ferramentas Especializadas** - Cada agente tem ferramentas otimizadas

## 🆕 O que você vai aprender

- ✅ **Criar sistemas multi-agente** com especialização
- ✅ **Implementar processo hierarchical** para coordenação
- ✅ **Desenvolver agentes com diferentes expertise**
- ✅ **Usar delegação automática** baseada no tipo de consulta
- ✅ **Criar ferramentas especializadas** para cada agente
- ✅ **Coordenar múltiplos agentes** em uma única crew

## 🤖 Os 3 Agentes Especializados

### 1. 🧠 **Agente Analisador de Consultas** (NOVO!)

```python
Role: "Analisador de Consultas Especializado"
Goal: "Classificar perguntas e determinar qual agente deve responder"
Expertise: Processamento de linguagem natural
Tools: AnalisadorConsultaTool()
```

**Responsabilidades:**

- Analisar perguntas dos usuários
- Classificar tipo de consulta automaticamente
- Recomendar agente especializado apropriado
- Fornecer análise estruturada das perguntas

### 2. 🏥 **Especialista em Dados de Saúde** (Evoluído)

```python
Role: "Especialista em Dados de Saúde"  
Goal: "Informações sobre estabelecimentos, queixas e visão geral"
Expertise: Sistemas hospitalares e dados clínicos
Tools: ConsultaSaudeAvancadaTool()
```

**Responsabilidades:**

- Informações sobre hospitais, UPAs, postos
- Análise de queixas principais e sintomas
- Visão geral do sistema de saúde
- Dados clínicos e de atendimento

### 3. 📊 **Especialista em Estatísticas** (NOVO!)

```python
Role: "Especialista em Estatísticas de Saúde"
Goal: "Análises numéricas e relatórios quantitativos"  
Expertise: Estatísticas de saúde pública
Tools: ConsultaSaudeAvancadaTool()
```

**Responsabilidades:**

- Análises estatísticas avançadas
- Métricas e indicadores quantitativos
- Distribuição geográfica por bairros
- Rankings e comparações numéricas

## 🚀 Pré-requisitos

1. **Arquivo `db/curso.db`** ✅ (já disponível no projeto)
2. **OpenAI API Key** configurada no `.env`
3. **Dependências instaladas**: `uv sync`

## ⚡ Execução Rápida

```bash
# Executar sistema multi-agente
uv run aula9/main.py
```

**Modos disponíveis:**

1. **Sistema Multi-Agente Interativo** (NOVO!) - Converse com os 3 agentes
2. **Demonstração Multi-Agente** - Veja como cada agente trabalha
3. **Sair**

## 💬 Como Usar (Interface Multi-Agente)

### 🎯 Exemplos de Perguntas por Especialista

#### 🧠 **Para o Analisador** (automático)

- *Qualquer pergunta é automaticamente analisada*
- Sistema decide qual agente deve responder
- Processo transparente para o usuário

#### 🏥 **Para o Especialista em Saúde**

```
💬 "Quais hospitais atendem mais pacientes?"
💬 "Quais são as principais queixas médicas?"
💬 "Mostre uma visão geral do sistema"
💬 "Informações sobre UPAs disponíveis"
```

#### 📊 **Para o Especialista Estatístico**

```  
💬 "Mostre estatísticas por bairro"
💬 "Qual a média de atendimentos por estabelecimento?"
💬 "Ranking dos bairros com mais atendimentos"
💬 "Quantos estabelecimentos existem no total?"
```

### ⌨️ Comandos Especiais Novos

```bash
'ajuda'   - Menu multi-agente
'agentes' - Informações detalhadas dos 3 agentes
'demo'    - Demonstração automática multi-agente  
'sair'    - Encerra o programa
```

## 🧠 Como Funciona (Arquitetura Multi-Agente)

### 📋 Fluxo Coordenado

```
1. Usuário faz pergunta
   ↓
2. 🧠 Agente Analisador classifica automaticamente
   ↓  
3. Sistema direciona para agente especializado:
   • 🏥 Especialista em Saúde (estabelecimentos, queixas)
   • 📊 Especialista Estatístico (números, geografia)
   ↓
4. Agente especializado consulta banco com ferramenta otimizada
   ↓
5. Resposta coordenada e especializada
   ↓
6. Sistema apresenta resultado ao usuário
```

### 🔄 Processo Hierarchical

```python
crew = Crew(
    agents=[agente_analisador, agente_saude, agente_estatistico],
    process=Process.hierarchical,  # COORDENAÇÃO INTELIGENTE
    manager_llm=ChatOpenAI(model="gpt-4o-mini"),
    verbose=False
)
```

**Vantagens do Processo Hierarchical:**

- ✅ Coordenação automática entre agentes
- ✅ Delegação baseada na expertise
- ✅ Evita redundância e confusão
- ✅ Respostas mais precisas e especializadas

## 🛠️ Ferramentas Especializadas

### 🧠 **AnalisadorConsultaTool** (NOVA)

```python
name: "analisador_consulta"
função: Classificar automaticamente o tipo de pergunta
output: JSON estruturado com análise e recomendação
```

**Tipos identificados:**

- `estabelecimentos` → Especialista em Saúde
- `estatisticas` → Especialista Estatístico  
- `queixas_sintomas` → Especialista em Saúde
- `geografico` → Especialista Estatístico
- `visao_geral` → Especialista em Saúde

### 🏥 **ConsultaSaudeAvancadaTool** (EVOLUÍDA)

```python
name: "consulta_saude_avancada"  
função: Consultas direcionadas por tipo e agente
parâmetros: tipo_consulta, filtros, limite
```

**Métodos especializados:**

- `_consulta_estabelecimentos_detalhada()`
- `_consulta_queixas_detalhada()`  
- `_consulta_geografica_detalhada()`
- `_consulta_estatisticas_avancadas()`
- `_consulta_overview_completa()`

## 🎬 Exemplo de Sessão Multi-Agente

```
🤖 SISTEMA MULTI-AGENTE INTELIGENTE DE DADOS DE SAÚDE
💬 Sua pergunta: Quantos hospitais existem por bairro?

🧠 Analisando pergunta: 'Quantos hospitais existem por bairro?'
🔄 Iniciando processo multi-agente...
🎯 Direcionando para: Agente Estatístico

📋 RESPOSTA DO SISTEMA MULTI-AGENTE:
🏘️ ANÁLISE GEOGRÁFICA DETALHADA:

📍 **Centro**
   🏥 Estabelecimentos: 3
   📊 Total de atendimentos: 12,547
   🏥 Tipos de queixas diferentes: 89

📍 **Zona Norte**  
   🏥 Estabelecimentos: 2
   📊 Total de atendimentos: 8,234
   🏥 Tipos de queixas diferentes: 76
...

💬 Sua pergunta: Quais são as principais queixas médicas?

🧠 Analisando pergunta: 'Quais são as principais queixas médicas?'
🎯 Direcionando para: Especialista em Dados de Saúde

📋 RESPOSTA DO SISTEMA MULTI-AGENTE:
🏥 ANÁLISE DETALHADA DE QUEIXAS PRINCIPAIS:

1. **CEFALEIA**
   📊 Total de atendimentos: 8,234
   📈 Percentual do total: 6.57%
   🏥 Estabelecimentos que atendem: 8

2. **FEBRE**
   📊 Total de atendimentos: 7,891  
   📈 Percentual do total: 6.29%
   🏥 Estabelecimentos que atendem: 8
...
```

## 🆚 Comparação: Aula 8 vs Aula 9

| Aspecto | 🎓 Aula 8 | 🚀 Aula 9 |
|---------|----------|----------|
| **Agentes** | 1 especialista | 3 agentes especializados |
| **Processo** | Sequential | Hierarchical |
| **Análise** | Manual na ferramenta | Agente analisador automático |
| **Especialização** | Geral | Cada agente tem expertise |
| **Coordenação** | Não aplicável | Delegação inteligente |
| **Ferramentas** | 1 ferramenta | 2 ferramentas especializadas |
| **Complexidade** | Intermediário | Avançado |
| **Precisão** | Boa | Excelente (especializada) |

## 🏗️ Arquitetura Técnica

### 📁 Estrutura de Arquivos

```
aula9/
├── main.py                    # Sistema multi-agente principal
├── README.md                  # Esta documentação
├── FLUXOGRAMA_AULA9.md       # Fluxograma detalhado
├── exercicios/               # Exercícios práticos
│   ├── exercicio1_agente_personalizado.py
│   ├── exercicio2_ferramenta_especializada.py
│   └── README_EXERCICIOS.md
└── exemplos/                 # Exemplos adicionais
    ├── exemplo_agente_simples.py
    └── exemplo_processo_hierarchical.py
```

### 🏗️ Componentes Multi-Agente

```python
# 1. Ferramentas Especializadas
AnalisadorConsultaTool()         # Classificação automática
ConsultaSaudeAvancadaTool()      # Consultas direcionadas

# 2. Agentes Especializados  
criar_agente_analisador()        # 🧠 Análise de consultas
criar_agente_especialista_saude() # 🏥 Dados de saúde
criar_agente_estatistico()       # 📊 Análises numéricas

# 3. Sistema Coordenado
criar_crew_multiagente()        # Crew com Process.hierarchical
executar_consulta_multiagente()  # Execução coordenada
```

## 📊 Tipos de Consultas Especializadas

### 🧠 **Classificação Automática:**

- **Palavras-chave analisadas** automaticamente
- **Confiança percentual** na classificação
- **Agente recomendado** baseado na análise
- **Justificativa detalhada** da decisão

### 🏥 **Especialista em Saúde atende:**

- Estabelecimentos (hospitais, UPAs, postos)
- Queixas principais e sintomas  
- Visão geral do sistema
- Informações clínicas

### 📊 **Especialista Estatístico atende:**

- Estatísticas gerais e métricas
- Distribuição geográfica
- Rankings e comparações
- Análises quantitativas

## 🎯 Conceitos-Chave Aprendidos

### 1. 🤖 **Sistemas Multi-Agente**

- Múltiplos agentes com especialização
- Coordenação entre agentes diferentes
- Delegação automática de tarefas
- Processo hierarchical para organização

### 2. 🧠 **Classificação Automática**

- Análise de linguagem natural
- Identificação de tipos de consulta
- Roteamento inteligente para especialistas
- Confidence scoring

### 3. 🔄 **Processo Hierarchical**

- Manager LLM coordenando agentes
- Delegação baseada em expertise
- Fluxo organizado de trabalho
- Evita conflitos entre agentes

### 4. 🛠️ **Ferramentas Especializadas**

- Ferramentas otimizadas por tipo de consulta
- Parâmetros específicos para cada uso
- Resultados formatados para cada especialista
- Melhor performance e precisão

### 5. 📊 **Expertise Distribuída**

- Cada agente com conhecimento específico
- Backstories especializadas
- Tools apropriadas para cada função
- Temperatura otimizada por tipo de tarefa

## 💡 Exercícios Práticos

### 🟢 **Exercício 1: Agente Personalizado**

Crie um 4º agente especializado:

```python
# Agente Geográfico - especialista em localização
# Foco em mapear estabelecimentos por região
# Ferramenta customizada para dados geográficos
```

### 🟡 **Exercício 2: Ferramenta Especializada**

Desenvolva uma nova ferramenta:

```python
# AnaliseTemporalTool - análises por período
# Trends temporais de atendimentos
# Sazonalidade de queixas
```

### 🔴 **Exercício 3: Processo Customizado**

Implemente variação do processo:

```python
# Processo Sequential com ordem específica
# Análise → Estatística → Saúde → Relatório final
# Cada agente contribui para resultado final
```

## 🚀 Próximos Passos

### 🎓 **Para Próximas Aulas:**

- Embeddings e busca semântica
- API REST multi-agente
- Interface web com múltiplos chat-bots
- Integração com dados externos

### 📚 **Aprofundamento:**

- Custom tools mais sofisticadas
- Agentes com memória compartilhada
- Workflows complexos entre agentes
- Monitoramento de performance multi-agente

## 🔧 Solução de Problemas

### ❌ **Agentes não coordenam**

```bash
# Verificar Process.hierarchical
# Confirmar manager_llm configurado
# Validar allow_delegation nos agentes
```

### ❌ **Classificação imprecisa**

```bash
# Ajustar palavras-chave no AnalisadorConsultaTool
# Modificar lógica de confiança
# Treinar com mais exemplos
```

### ❌ **Performance lenta**

```bash
# Reduzir verbose para False
# Otimizar queries SQL
# Usar cache para classificações repetidas
```

## 📈 Métricas de Sucesso Multi-Agente

Ao final da aula, você deve conseguir:

- ✅ Executar sistema com 3 agentes coordenados
- ✅ Ver classificação automática funcionando
- ✅ Observar delegação baseada na expertise
- ✅ Receber respostas mais precisas e especializadas
- ✅ Entender processo hierarchical na prática
- ✅ Criar agentes e ferramentas customizadas

## 🏆 Diferenciais desta Aula

### 🎯 **Especialização Inteligente:**

- Cada agente tem expertise bem definida
- Classificação automática de consultas
- Delegação precisa baseada no conteúdo
- Respostas mais especializadas e úteis

### 🔄 **Coordenação Avançada:**

- Process.hierarchical para organização
- Manager LLM coordenando decisões
- Fluxo inteligente entre agentes
- Evita redundância e confusão

### 🧠 **Análise Automática:**

- Sistema analisa perguntas automaticamente
- Classificação com confidence scoring
- Roteamento inteligente para especialistas
- Processo transparente para usuário

## 📚 Recursos de Referência

- [CrewAI Process Types](https://docs.crewai.com/core-concepts/processes)
- [Multi-Agent Systems](https://docs.crewai.com/how-to/custom-agent-roles)
- [Hierarchical Process](https://docs.crewai.com/core-concepts/manager-delegation)
- [Custom Tools](https://docs.crewai.com/tools/custom-tools)

## 🤝 Suporte

- 💬 **Dúvidas**: Use o Discord do curso
- 🐛 **Problemas técnicos**: Crie issue no GitHub  
- 📖 **Documentação**: Veja arquivos `/docs/`
- 🚀 **Execução**: `uv run aula9/main.py`

---

**🎯 Missão Cumprida**: Você criou um sistema multi-agente inteligente com 3 especialistas coordenados, demonstrando o poder da colaboração entre agentes CrewAI!

**🚀 Próximo Nível**: Próximas aulas explorarão busca semântica, APIs REST e interfaces web avançadas.

---

**⚡ Comando Rápido**: `uv run aula9/main.py` e experimente conversar com seus 3 agentes especializados trabalhando em equipe!
