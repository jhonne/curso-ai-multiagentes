# Curso Avançado: Sistema de Atendimento Médico com CrewAI e WhatsApp Business

**Nível:** Iniciante a Intermediário

**Carga Horária Total:** 24 horas

**Pré-requisitos:**

* Conhecimento básico de Python.
* Familiaridade com o conceito de APIs.
* Uma chave de API da OpenAI.
* Noções básicas de banco de dados (SQL).

## Visão Geral do Curso:**

Este curso prático de 24 horas capacita desenvolvedores a construir um **sistema completo de atendimento médico** usando CrewAI com dados reais. Os alunos aprenderão a integrar múltiplos agentes de IA com banco de dados PostgreSQL, implementar busca semântica com embeddings, e criar uma API completa integrada ao WhatsApp Business.

**Projeto Final:** Sistema de triagem médica inteligente que recebe sintomas via WhatsApp e recomenda estabelecimentos de saúde próximos baseado em dados reais do Piauí com 3.284 estabelecimentos, 65 queixas principais e 22 sintomas catalogados.

---

## 🏥 **Contexto do Projeto: Sistema de Atendimento Médico**

O curso utilizará dados reais de saúde do Piauí para construir um sistema prático de triagem médica:

* **3.284 estabelecimentos de saúde** com geolocalização
* **65 queixas principais** catalogadas (ex: "ALERGIA", "CEFALEIA", "CONVULSÕES")
* **22 sintomas médicos** (ex: "RESPIRAÇÃO INADEQUADA", "CHOQUE", "DOR INTENSA")
* **25 relacionamentos** queixa-sintoma para algoritmos de recomendação

---

### Módulo 1: Fundamentos do CrewAI (6 horas)

#### Aula 1: Introdução à Inteligência Artificial de Agentes e ao CrewAI (2 horas)

* **Objetivos:**
  * Compreender sistemas multi-agentes aplicados à saúde
  * Configurar ambiente de desenvolvimento com UV
  * Entender o contexto médico do projeto
* **Tópicos:**
  * Vantagens de agentes especializados em triagem médica
  * Apresentação do CrewAI: Agentes, Tarefas, Ferramentas
  * Setup com UV (gerenciador moderno de pacotes)
  * Visão geral do banco de dados médico
* **Exercício Prático:**
  * Setup completo do ambiente com `uv sync`
  * Primeiro agente médico: "Agente de Triagem Básica"
  * Exploração inicial dos dados médicos reais

#### Aula 2: Construindo seu Primeiro Crew Médico (2 horas)

* **Objetivos:**
  * Criar agentes especializados em contexto médico
  * Definir personalidades apropriadas para saúde
* **Tópicos:**
  * Agente Triagem: role, goal, backstory médico
  * Agente Busca Sintomas: especialista em catalogação
  * Ética e responsabilidade em sistemas de saúde automatizados
* **Exercício Prático:**
  * Crew com "Enfermeiro de Triagem" e "Especialista em Sintomas"
  * Primeiras interações com dados médicos estruturados

#### Aula 3: Ferramentas Médicas e Processos (2 horas)

* **Objetivos:**
  * Ferramentas específicas para dados médicos
  * Processos hierárquicos para tomada de decisão médica
* **Tópicos:**
  * Tools personalizadas para busca de sintomas
  * Processo Sequential vs Hierarchical em contexto médico
  * Priorização baseada em criticidade de sintomas
* **Exercício Prático:**
  * Ferramenta de busca em base de sintomas
  * Processo que escala casos críticos automaticamente

---

### Módulo 2: Integração com Banco de Dados e Busca Semântica (8 horas)

#### Aula 4: Arquitetura do Sistema Médico Multi-Agente (2 horas)

* **Objetivos:**
  * Projetar arquitetura completa de triagem médica
  * Definir fluxo de decisão baseado em dados reais
* **Tópicos:**
  * **Agente de Triagem Inicial:** Classifica urgência
  * **Agente de Análise Sintomas:** Correlaciona com base médica
  * **Agente Geográfico:** Localiza estabelecimentos próximos
  * **Agente de Recomendação:** Formula orientação final
* **Exercício Prático:**
  * Desenho completo do fluxo de atendimento
  * Definição de critérios de priorização médica

#### Aula 5: Otimização para Contexto Médico (3 horas)

* **Objetivos:**
  * Prompts otimizados para precisão médica
  * Configurações específicas para saúde
  * Testes com casos reais de urgência/emergência
* **Tópicos:**
  * **Prompts Médicos Especializados:**
    * Chain-of-thought para diagnóstico diferencial
    * Few-shot com casos médicos reais
    * Terminologia médica consistente
  * **Configuração OpenAI para Saúde:**
    * Temperature baixa para consistência (0.1-0.3)
    * Max_tokens otimizado para respostas médicas
    * Fallbacks para casos críticos
  * **Validação Médica:**
    * Casos de teste baseados em protocolos reais
    * Métricas de precisão para sintomas críticos
    * Compliance com normas de saúde
* **Exercício Prático:**
  * Suite de testes com casos médicos variados
  * Otimização de prompts para precisão diagnóstica
  * Sistema de alertas para sintomas críticos

#### Aula 6: Gerenciamento de Fluxo Médico (3 horas)

* **Objetivos:**
  * Orquestrar decisões médicas complexas
  * Implementar protocolos de escalação
* **Tópicos:**
  * Tasks médicas com contexto de urgência
  * Passagem de dados entre especialistas
  * Protocolos de escalação automática
* **Exercício Prático:**
  * Sistema completo de triagem com escalação
  * Integração de todos os agentes médicos

---

### Módulo 3: Sistema Avançado com Banco de Dados e WhatsApp (10 horas)

#### Aula 7: Integração PostgreSQL e MCP (2 horas)

* **Objetivos:**
  * Conectar agentes CrewAI ao banco de dados real
  * Queries otimizadas para dados médicos
* **Tópicos:**
  * **Configuração PostgreSQL:**
    * Conexão via MCP (Model Context Protocol)
    * Estrutura das tabelas médicas
    * Índices otimizados para performance
  * **Agentes com Dados Reais:**
    * Consultas aos estabelecimentos
    * Busca por queixas principais
    * Correlação sintoma-estabelecimento
* **Exercício Prático:**
  * Agente que consulta estabelecimentos próximos por coordenadas
  * Busca de sintomas relacionados a queixas específicas
  * Sistema de cache para queries frequentes
* **Código de Exemplo:**

```python
# Agente especializado em dados geográficos
agente_geografico = Agent(
    role="Especialista em Geolocalização Médica",
    goal="Encontrar estabelecimentos de saúde próximos com base na localização do paciente",
    backstory="Especialista em sistemas de geolocalização médica com conhecimento da rede de saúde do Piauí",
    tools=[postgresql_tool, distancia_tool],
    llm=llm_otimizado
)
```

#### Aula 8: Embeddings e pgvector para Busca Semântica (2 horas)

* **Objetivos:**
  * Implementar busca semântica nos sintomas
  * Usar OpenAI Embeddings + pgvector
* **Tópicos:**
  * **Setup pgvector:**
    * Extensão PostgreSQL para vetores
    * Criação de índices vetoriais
    * Configuração de similarity search
  * **Embeddings Médicos:**
    * Vetorização de sintomas e queixas
    * Similaridade semântica para diagnóstico
    * Cache inteligente de embeddings
* **Exercício Prático:**
  * Embedding de todos os 22 sintomas catalogados
  * Busca por sintomas similares com threshold de confiança
  * Sistema de recomendação baseado em similaridade
* **Código de Exemplo:**

```python
# Sistema de embeddings para sintomas
def buscar_sintomas_similares(sintoma_input, threshold=0.8):
    embedding = openai.embeddings.create(
        input=sintoma_input,
        model="text-embedding-ada-002"
    )
    
    # Busca por similaridade no pgvector
    query = """
    SELECT nome, 1 - (embedding <=> %s) as similarity 
    FROM sintomas_embeddings 
    WHERE 1 - (embedding <=> %s) > %s 
    ORDER BY similarity DESC
    """
    return execute_query(query, [embedding.data[0].embedding, embedding.data[0].embedding, threshold])
```

#### Aula 9: Sistema de Recomendação Médica Completo (2 horas)

* **Objetivos:**
  * Integrar todos os agentes com dados reais
  * Algoritmo de recomendação médica baseado em IA
* **Tópicos:**
  * **Agente de Triagem Avançada:**
    * Análise de sintomas com embeddings
    * Classificação de urgência automática
    * Integração com protocolos médicos
  * **Agente de Recomendação Geográfica:**
    * Cálculo de distância real (lat/lng)
    * Filtro por tipo de estabelecimento
    * Consideração de horário de funcionamento
  * **Agente de Protocolo Médico:**
    * Aplicação de guidelines médicos
    * Recomendações baseadas em evidências
    * Alertas para casos críticos
* **Exercício Prático:**
  * Sistema completo que recebe sintomas e retorna:
    * Nível de urgência (1-5)
    * 3 estabelecimentos mais adequados
    * Orientações iniciais baseadas em protocolos
* **Exemplo de Uso:**

```bash
Input: "Dor no peito intensa, falta de ar, sudorese"
Output: 
- 🚨 URGÊNCIA MÁXIMA (5/5)
- 🏥 Hospital de Urgência de Teresina - 2.3km
- 🚑 UPA Promorar - 5.7km  
- ⚕️ PROTOCOLO: Procure atendimento IMEDIATAMENTE
```

#### Aula 10: API REST com FastAPI (2 horas)

* **Objetivos:**
  * Criar API profissional para os agentes
  * Documentação automática e autenticação
* **Tópicos:**
  * **Estrutura da API:**
    * Endpoints RESTful para cada agente
    * Modelos Pydantic para validação
    * Middleware de logging e monitoramento
  * **Endpoints Principais:**
    * `POST /triagem` - Análise inicial de sintomas
    * `GET /estabelecimentos` - Busca por localização
    * `POST /recomendacao` - Recomendação completa
    * `GET /sintomas/similares` - Busca semântica
* **Exercício Prático:**
  * API completa com 8 endpoints
  * Documentação automática no Swagger
  * Testes automatizados com pytest
* **Estrutura da API:**

```python
@app.post("/triagem")
async def triagem_medica(
    sintomas: List[str],
    localizacao: Optional[Coordenadas] = None,
    urgencia_percebida: Optional[int] = None
) -> TriagemResponse:
    # Processa com agentes CrewAI
    resultado = crew_triagem.kickoff({
        'sintomas': sintomas,
        'localizacao': localizacao
    })
    return TriagemResponse.parse_obj(resultado)
```

#### Aula 11: Integração WhatsApp Business API (2 horas)

* **Objetivos:**
  * Conectar sistema médico ao WhatsApp
  * Bot de atendimento médico via mensagens
* **Tópicos:**
  * **Setup WhatsApp Business:**
    * Configuração do webhook
    * Autenticação com Meta API
    * Gestão de templates de mensagem
  * **Bot Médico WhatsApp:**
    * Recepção de sintomas via texto/áudio
    * Processamento com agentes CrewAI
    * Respostas formatadas para mobile
  * **Fluxo de Atendimento:**
    * Saudação e coleta de sintomas
    * Análise automática com IA
    * Recomendação de estabelecimentos
    * Follow-up opcional
* **Exercício Prático:**
  * Bot completo integrado ao WhatsApp
  * Teste com números reais (sandbox)
  * Fluxo de atendimento médico automatizado
* **Exemplo de Conversa:**

```
👨‍⚕️ Bot: Olá! Sou seu assistente de saúde. Descreva seus sintomas.

👤 Usuário: Estou com febre, dor de cabeça e enjoo

👨‍⚕️ Bot: Analisando... 
🔍 Sintomas identificados: FEBRE, CEFALEIA, NÁUSEAS
⚠️ Nível de urgência: 3/5 (Moderado)

🏥 Recomendações próximas:
1. UPA Promorar - 2.1km - ⭐⭐⭐⭐
2. Hospital Municipal - 4.3km - ⭐⭐⭐

💊 Orientação: Hidrate-se e monitore a febre. Se piorar, procure atendimento.
```

#### Aula 12: Deploy, Monitoramento e Produção (2 horas)

* **Objetivos:**
  * Deploy profissional do sistema completo
  * Monitoramento e logs para produção
* **Tópicos:**
  * **Containerização:**
    * Dockerfile otimizado para CrewAI
    * Docker-compose com PostgreSQL + pgvector
    * Variáveis de ambiente para produção
  * **Monitoramento:**
    * Logs estruturados com loguru
    * Métricas de performance dos agentes
    * Alertas para casos críticos não resolvidos
  * **Deploy em Produção:**
    * Deploy no Railway/Heroku/DigitalOcean
    * SSL e domínio personalizado
    * Backup automatizado do banco
* **Exercício Prático:**
  * Sistema completo rodando em produção
  * Dashboard de monitoramento funcionando
  * Testes end-to-end via WhatsApp
* **Arquitetura Final:**

```
WhatsApp → Webhook → FastAPI → CrewAI Agents → PostgreSQL
                                      ↓
                              OpenAI API + Embeddings
                                      ↓
                              Sistema de Logs + Métricas
```

---

## 🎯 **Projeto Final: Sistema Médico Completo**

Ao final do curso, cada aluno terá construído um **sistema de atendimento médico real** com as seguintes capacidades:

### ✅ **Funcionalidades Implementadas:**

* **🤖 Bot WhatsApp** para coleta de sintomas
* **🧠 4 Agentes Especializados** (Triagem, Sintomas, Geográfico, Protocolo)
* **🗃️ Banco PostgreSQL** com dados reais de 3.284 estabelecimentos
* **🔍 Busca Semântica** com OpenAI Embeddings + pgvector
* **🚀 API REST** completa com documentação Swagger
* **📊 Dashboard** de monitoramento e métricas
* **🐳 Deploy** containerizado em produção

### 📱 **Demo Final - Fluxo Completo:**

```text
[WhatsApp] → [Webhook] → [FastAPI] → [CrewAI Agents] → [PostgreSQL + Embeddings] → [Resposta Médica]
```

**Exemplo de interação real:**

1. Usuário envia: *"Estou com dor no peito e falta de ar"*
2. Sistema responde em **<5 segundos**:
   * 🚨 Urgência: **ALTA (4/5)**
   * 🏥 Hospital mais próximo: **2.3km**
   * ⚕️ Orientação: **"Procure atendimento imediatamente"**

---

## 🛠️ **Stack Tecnológico Completo**

### **Dependências Principais (pyproject.toml)**

```toml
dependencies = [
    "crewai>=0.95.0",           # Framework principal
    "openai>=1.12.0",           # LLM + Embeddings
    "fastapi>=0.104.0",         # API REST
    "uvicorn>=0.24.0",          # ASGI server
    "psycopg2-binary>=2.9.0",   # PostgreSQL driver
    "pgvector>=0.2.0",          # Extensão vetorial
    "pydantic>=2.5.0",          # Validação de dados
    "python-dotenv>=1.0.0",     # Variáveis de ambiente
    "loguru>=0.7.0",            # Logging avançado
    "pytest>=7.4.0",            # Testes automatizados
    "httpx>=0.25.0",            # Cliente HTTP assíncrono
    "python-multipart>=0.0.6"   # Upload de arquivos
]

[project.optional-dependencies]
whatsapp = ["requests>=2.31.0", "flask>=2.3.0"]
monitoring = ["prometheus-client>=0.17.0", "grafana-api>=1.0.3"]
deploy = ["docker>=6.1.0", "gunicorn>=21.2.0"]
```

### **Estrutura do Projeto Final**

```text
sistema-medico-crewai/
├── 🐳 docker-compose.yml          # Orquestração completa
├── 🚀 api/
│   ├── main.py                   # FastAPI principal
│   ├── endpoints/                # Endpoints REST
│   ├── models.py                 # Modelos Pydantic
│   └── middleware.py             # Logging, CORS, etc
├── 🤖 agents/
│   ├── triagem.py               # Agente de Triagem
│   ├── sintomas.py              # Especialista em Sintomas
│   ├── geografico.py            # Busca Geográfica
│   └── protocolo.py             # Protocolos Médicos
├── 🗃️ database/
│   ├── models.py                # SQLAlchemy models
│   ├── migrations/              # Alembic migrations
│   └── seeds/                   # Dados iniciais
├── 📱 whatsapp/
│   ├── webhook.py               # Receptor de mensagens
│   ├── sender.py                # Envio de respostas
│   └── templates/               # Templates de mensagem
├── 🔍 embeddings/
│   ├── generator.py             # Geração de embeddings
│   ├── similarity.py            # Busca por similaridade
│   └── cache.py                 # Cache inteligente
├── 📊 monitoring/
│   ├── metrics.py               # Métricas customizadas
│   ├── alerts.py                # Sistema de alertas
│   └── dashboard/               # Dashboard Grafana
└── 🧪 tests/
    ├── unit/                    # Testes unitários
    ├── integration/             # Testes de integração
    └── e2e/                     # Testes end-to-end
```

---

## 📊 **Métricas e KPIs do Sistema**

### **Performance Esperada:**

* **⚡ Latência:** <5s para respostas completas
* **🎯 Precisão:** >85% na classificação de urgência
* **💰 Custo:** <$0.10 por consulta completa
* **📈 Throughput:** 1000+ consultas/hora
* **✅ Uptime:** 99.5% de disponibilidade

### **Monitoramento em Tempo Real:**

* Dashboard com métricas de uso dos agentes
* Alertas automáticos para casos críticos não resolvidos
* Análise de sentiment das interações WhatsApp
* Tracking de custos OpenAI por agente

---

## 🌟 **Diferenciais do Curso**

### **Por que este curso é único:**

1. **📊 Dados Reais:** Trabalha com dados governamentais reais de saúde
2. **🏥 Aplicação Prática:** Resolve problema real de acesso à saúde
3. **🚀 Stack Moderno:** CrewAI + FastAPI + pgvector + WhatsApp
4. **💼 Portfolio:** Projeto completo para portfólio profissional
5. **🔄 Deploy Real:** Sistema funcionando em produção
6. **📱 Integração WhatsApp:** Acessibilidade via app mais usado no Brasil

### **Skills Desenvolvidas:**

* ✅ **Arquitetura Multi-Agentes** para problemas complexos
* ✅ **Integração de Banco de Dados** com IA
* ✅ **Busca Semântica** com embeddings
* ✅ **APIs REST** profissionais com FastAPI
* ✅ **Integração WhatsApp Business**
* ✅ **Deploy e Monitoramento** em produção
* ✅ **Ética em IA** aplicada à saúde

---

## 📈 **Próximos Passos Após o Curso**

### **Expansões Sugeridas:**

1. **🔊 Processamento de Áudio:** Integrar Whisper para mensagens de voz
2. **📸 Análise de Imagens:** GPT-4 Vision para análise de ferimentos
3. **🌐 Multi-idiomas:** Suporte a inglês e espanhol
4. **📱 App Mobile:** Interface nativa iOS/Android
5. **🤖 IA Generativa:** Gerar relatórios médicos automáticos
6. **🔗 Integração SUS:** Conectar com sistemas oficiais de saúde

### **Oportunidades de Carreira:**

* **🏥 Healthtech:** Startups de tecnologia em saúde
* **🤖 AI Engineer:** Especialista em sistemas multi-agentes
* **🚀 Product Manager:** Produtos de IA para saúde
* **📊 Data Science:** Análise de dados médicos com IA
* **🏢 Consultoria:** Implementação de IA em hospitais/clínicas

---

## 💰 **Investimento e ROI**

### **Custo Estimado do Curso:**

| Recurso | Custo Mensal | Custo Total |
|---------|--------------|-------------|
| **OpenAI API** | $25-50 | $25-50 |
| **PostgreSQL** (Railway) | $5 | $5 |
| **WhatsApp Business** | Gratuito | $0 |
| **Deploy** (Railway/Heroku) | $10 | $10 |
| **Total** | | **$40-65** |

### **ROI Esperado:**

* **Portfolio:** Projeto real para apresentar em entrevistas
* **Skills Valiosas:** Stack moderno valorizado pelo mercado
* **Network:** Conexões com outros devs AI
* **Certificação:** Certificado de conclusão
* **Mentoria:** Acompanhamento durante todo o desenvolvimento

---

## 🎓 **Certificação e Avaliação**

### **Critérios de Aprovação:**

* ✅ **90% de Presença** nas aulas práticas
* ✅ **Sistema Funcionando** com todos os componentes
* ✅ **Deploy em Produção** com URL funcionando
* ✅ **Apresentação Final** de 10 minutos
* ✅ **Código no GitHub** com documentação completa

### **Entregáveis Finais:**

1. **🔗 URL do Sistema** funcionando em produção
2. **📱 Número WhatsApp** do bot funcionando
3. **📊 Dashboard** com métricas em tempo real
4. **📚 Documentação** técnica completa
5. **🎥 Video Demo** de 3 minutos
6. **💻 Código Fonte** no GitHub

---

## 🤝 **Suporte e Comunidade**

* **💬 Discord Exclusivo** para alunos
* **📅 Office Hours** semanais com instrutor
* **🔄 Code Review** dos projetos
* **🎯 Mentoria** para próximos passos profissionais
* **📢 Showcase** dos melhores projetos
* **💼 Conexões** com recrutadores de healthtechs

---

**🚀 Pronto para construir o futuro da saúde digital com IA?**
