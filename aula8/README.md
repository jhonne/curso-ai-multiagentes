# 🎓 Aula 8: CrewAI + SQLite - VERSÃO INTERATIVA

## 🎯 Objetivo

Evoluir da Aula 7 criando um **sistema interativo** onde usuários podem conversar naturalmente com agentes CrewAI conectados ao banco SQLite, usando dados reais de estabelecimentos de saúde.

## ✨ Principais Novidades (Evolução da Aula 7)

- 🗣️ **Prompt interativo** - Converse naturalmente com os agentes
- 🗄️ **SQLite ao invés de PostgreSQL** - Mais simples e prático  
- 📊 **Dados reais** - Base completa de estabelecimentos de saúde
- 🔄 **Interface amigável** - Sistema de linha de comando intuitivo
- 💬 **Múltiplas consultas** - Várias perguntas em uma sessão
- 🎬 **Modo demonstração** - Exemplos automáticos para aprendizado

## 🆕 O que você vai aprender

- ✅ **Criar sistema interativo** com agentes CrewAI
- ✅ **Usar banco SQLite** ao invés de PostgreSQL
- ✅ **Implementar prompt dinâmico** para conversação natural
- ✅ **Trabalhar com dados reais** de saúde pública
- ✅ **Criar interface de usuário** em linha de comando
- ✅ **Gerenciar múltiplas consultas** em uma sessão

## 🚀 Pré-requisitos (Simplificados!)

1. **Arquivo `db/curso.db`** ✅ (já disponível no projeto)
2. **OpenAI API Key** configurada no `.env`
3. **Dependências instaladas**: `uv sync`

**Sem PostgreSQL!** 🎉 - Agora usamos SQLite que já vem pronto

## ⚡ Execução Rápida

```bash
# Executar o sistema interativo
uv run aula8/main.py
```

**Escolha o modo:**

- **Modo Interativo** (recomendado) - Converse com o agente
- **Demonstração Automática** - Veja exemplos funcionando

## 🗄️ Dados Disponíveis (Banco SQLite)

O banco `db/curso.db` contém dados reais:

### 📊 Tabelas Principais

- **`ia_estabelecimento`** - Hospitais, UPAs, postos de saúde
- **`ia_queixa_principal`** - Queixas mais comuns dos pacientes  
- **`ia_sintoma`** - Sintomas catalogados
- **`ia_historico_atendimento_sintoma`** - Histórico de atendimentos

### 🏥 Exemplos de Estabelecimentos

```
• Hospital de Urgência de Teresina (HUT)
• UPA do Promorar  
• Posto de Saúde Saci
• Hospital Regional de São Raimundo Nonato
• ...e centenas de outros!
```

### 🏥 Exemplos de Queixas

```
• Cefaleia (dor de cabeça)
• Febre  
• Dor abdominal
• Tosse
• Dor nas costas
• ...e muitas outras!
```

## 💬 Como Usar (Interface Interativa)

### 🎯 Perguntas Sugeridas

```
💬 "Quais são os hospitais disponíveis?"
💬 "Mostre as queixas mais frequentes"
💬 "Quantos estabelecimentos existem por bairro?"
💬 "Quais são as estatísticas gerais?"
💬 "Hospitais na região central"
💬 "Sintomas mais relatados pelos pacientes"
```

### ⌨️ Comandos Especiais

```bash
'ajuda'  - Mostra menu de opções
'sair'   - Encerra o programa  
'limpar' - Limpa a tela
```

## 🧠 Como Funciona (Arquitetura)

### 📋 Fluxo Interativo

```
1. Usuário digita pergunta natural
   ↓
2. Sistema analisa tipo de consulta
   ↓  
3. Agente usa ferramenta SQLite
   ↓
4. Ferramenta executa query apropriada
   ↓
5. Dados são formatados e retornados
   ↓
6. Agente apresenta resposta amigável
   ↓
7. Sistema aguarda próxima pergunta
```

### 🛠️ Ferramenta SQLite Inteligente

```python
class ConsultaSaudeTool(BaseTool):
    name = "consulta_saude"
    
    def _run(self, consulta: str):
        # Analisa tipo de consulta
        if "estabelecimento" in consulta:
            return self._buscar_estabelecimentos()
        elif "queixa" in consulta:
            return self._buscar_queixas_sintomas()  
        # ... mais tipos de consulta
```

### 🤖 Agente Especialista

```python
agente = Agent(
    role="Especialista em Dados de Saúde",
    goal="Ajudar usuários a encontrar informações de saúde",
    backstory="""Especialista em análise de dados de saúde 
                 pública com acesso a base completa...""",
    tools=[ConsultaSaudeTool()]
)
```

## 🎬 Exemplo de Sessão Interativa

```
🏥 SISTEMA INTERATIVO DE DADOS DE SAÚDE
💬 Sua pergunta: Quantos hospitais existem?

🤔 Analisando: 'Quantos hospitais existem?'
⏳ Agente trabalhando...

📋 RESPOSTA DO AGENTE:
📊 ESTATÍSTICAS DO SISTEMA DE SAÚDE:

🏥 **Estabelecimentos**: 2,847
🏥 **Queixas cadastradas**: 156  
💊 **Sintomas únicos**: 891
📋 **Total de atendimentos**: 125,394
🏘️ **Bairros atendidos**: 312

💬 Sua pergunta: Mostre as queixas mais comuns

🤔 Analisando: 'Mostre as queixas mais comuns'
⏳ Agente trabalhando...

📋 RESPOSTA DO AGENTE:  
🏥 QUEIXAS PRINCIPAIS MAIS FREQUENTES:

1. **CEFALEIA**
   📊 8,234 atendimentos (6.57% do total)

2. **FEBRE**  
   📊 7,891 atendimentos (6.29% do total)
   
3. **DOR ABDOMINAL**
   📊 6,547 atendimentos (5.22% do total)
...
```

## 🆚 Comparação: Aula 7 vs Aula 8

| Aspecto | 🎓 Aula 7 | 🚀 Aula 8 |
|---------|----------|----------|
| **Banco** | PostgreSQL | SQLite |
| **Interação** | Script único | Sistema interativo |
| **Dados** | Poucos exemplos | Base completa real |
| **Consultas** | Uma por execução | Múltiplas por sessão |
| **Interface** | Terminal básico | Menu e comandos |
| **Complexidade** | Iniciante | Intermediário |
| **Setup** | PostgreSQL + config | Apenas SQLite |

## 🔧 Arquitetura Técnica

### 📁 Estrutura de Arquivos

```
aula8/
├── main.py              # Sistema principal interativo
├── README.md            # Esta documentação  
├── exercicios/          # Exercícios práticos
└── exemplos/            # Exemplos adicionais

db/
└── curso.db            # Banco SQLite (dados reais)
```

### 🏗️ Componentes Principais

```python
# 1. Ferramenta SQLite
ConsultaSaudeTool()
├── _buscar_estabelecimentos()
├── _buscar_queixas_sintomas()  
├── _buscar_por_bairro()
├── _buscar_estatisticas()
└── _buscar_overview_geral()

# 2. Sistema Interativo  
sistema_interativo()
├── mostrar_menu_inicial()
├── processar_comando_especial()
├── executar_consulta_interativa()
└── loop_principal_interacao()

# 3. Agente Especializado
criar_agente_saude()
└── Agent(tools=[ConsultaSaudeTool])
```

## 📊 Tipos de Consultas Suportadas

### 🏥 **Estabelecimentos:**

- Lista de hospitais e UPAs
- Busca por nome ou região
- Informações de contato
- Distribuição por bairro

### 🏥 **Queixas e Sintomas:**  

- Queixas mais frequentes
- Sintomas por tipo
- Estatísticas de atendimento
- Correlações entre sintomas

### 📈 **Estatísticas:**

- Números gerais do sistema
- Ranking de estabelecimentos  
- Distribuição geográfica
- Análises temporais

### 🔍 **Visão Geral:**

- Overview completo do banco
- Top estabelecimentos
- Principais indicadores
- Resumo executivo

## 🎯 Conceitos-Chave Aprendidos

### 1. 🔄 **Sistema Interativo**

- Loop principal de interação
- Processamento de comandos
- Gestão de estado da sessão
- Interface amigável ao usuário

### 2. 🗄️ **SQLite vs PostgreSQL**

- Simplicidade de setup
- Portabilidade dos dados
- Queries compatíveis
- Performance adequada

### 3. 🧠 **Inteligência Conversacional**

- Análise de linguagem natural
- Classificação de intenções
- Respostas contextualizadas  
- Feedback amigável

### 4. 📊 **Dados Reais de Saúde**

- Estrutura de sistema de saúde
- Relacionamentos entre entidades
- Padrões de atendimento
- Análise estatística

## 💡 Exercícios Práticos

### 🟢 **Exercício 1: Consultas Básicas**

Modifique o sistema para aceitar novos tipos de consulta:

```python
# Adicionar busca por tipo de estabelecimento
"Mostre apenas as UPAs"
"Hospitais com mais de 1000 atendimentos"
```

### 🟡 **Exercício 2: Interface Melhorada**  

Implemente melhorias na interface:

```python
# Histórico de consultas
# Favoritos do usuário
# Exportação de resultados
```

### 🔴 **Exercício 3: Agente Especializado**

Crie um segundo agente com especialidade diferente:

```python
# Agente Geográfico - foco em localização
# Agente Estatístico - foco em análises
# Agente Médico - foco em triagem
```

## 🚀 Próximos Passos

### 🎓 **Para Aula 9:**

- Múltiplos agentes especializados
- Embeddings e busca semântica
- Interface web com Streamlit
- API REST para integração

### 📚 **Aprofundamento:**

- Otimização de queries SQLite
- Cache inteligente de respostas
- Logs de auditoria de consultas
- Integração com APIs externas

## 🔧 Solução de Problemas

### ❌ **Banco não encontrado**

```bash
# Verificar se arquivo existe
ls -la db/curso.db

# Se não existir, verificar migração
ls -la db/
```

### ❌ **OpenAI API Key**

```bash
# Configurar no .env
echo "OPENAI_API_KEY=sua_chave" >> .env

# Ou usar configurador
uv run configurar.py
```

### ❌ **Dependências**

```bash
# Instalar todas as dependências
uv sync

# Verificar versões
uv tree
```

## 📈 Métricas de Sucesso

Ao final da aula, você deve conseguir:

- ✅ Executar sistema interativo completo
- ✅ Fazer consultas naturais aos dados
- ✅ Navegar entre diferentes tipos de informação
- ✅ Entender a arquitetura de sistema conversacional
- ✅ Modificar consultas e adicionar funcionalidades

## 🏆 Diferenciais desta Aula

### 🎯 **Foco na Experiência do Usuário:**

- Interface intuitiva e amigável
- Feedback claro e útil
- Comandos naturais
- Respostas bem formatadas

### 🔧 **Facilidade de Setup:**

- SQLite elimina configuração complexa
- Dados já prontos para uso
- Menos dependências externas
- Execução em qualquer sistema

### 📊 **Dados Realistas:**

- Base de dados real do sistema de saúde
- Casos de uso práticos
- Padrões reais de atendimento
- Estatísticas significativas

## 📚 Recursos de Referência

- [Documentação SQLite](https://www.sqlite.org/docs.html)
- [CrewAI Tools](https://docs.crewai.com/tools)  
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [OpenAI API](https://platform.openai.com/docs)

## 🤝 Suporte

- 💬 **Dúvidas**: Use o Discord do curso
- 🐛 **Problemas técnicos**: Crie issue no GitHub  
- 📖 **Documentação**: Veja arquivos `/docs/`
- 🚀 **Execução**: `uv run aula8/main.py`

---

**🎯 Missão Cumprida**: Você criou um sistema interativo completo onde usuários podem conversar naturalmente com agentes CrewAI conectados a dados reais!

**🚀 Próximo Nível**: Aula 9 explorará múltiplos agentes especializados trabalhando em conjunto.

---

**⚡ Comando Rápido**: `uv run aula8/main.py` e comece a conversar com seu agente especialista!
