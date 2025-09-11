# Referência CrewAI

Este arquivo contém informações de referência sobre o CrewAI framework para consultas durante o desenvolvimento.

## Repositório Oficial

- **GitHub**: <https://github.com/crewAIInc/crewAI>
- **Documentação**: <https://docs.crewai.com>
- **Website**: <https://crewai.com>

## Visão Geral do CrewAI

CrewAI é um framework Python lean e ultrarrápido construído completamente do zero, independente do LangChain ou outros frameworks de agentes. Ele capacita desenvolvedores com simplicidade de alto nível e controle preciso de baixo nível, ideal para criar agentes de IA autônomos.

### Componentes Principais

#### 1. **Crews** - Equipes de Agentes Colaborativos

- Otimizados para autonomia e inteligência colaborativa
- Agentes com papéis específicos, ferramentas e objetivos
- Colaboração natural entre agentes
- Ideal para tarefas criativas e exploratórias

#### 2. **Flows** - Workflows Estruturados

- Controle granular e orientado por eventos
- Chamadas LLM únicas para orquestração precisa
- Suporte nativo para Crews
- Ideal para processos determinísticos e auditáveis

### Arquitetura Framework

| Componente | Descrição | Características Principais |
|------------|-----------|----------------------------|
| **Crew** | Organização de nível superior | • Gerencia equipes de agentes IA • Supervisiona workflows • Garante colaboração • Entrega resultados |
| **AI Agents** | Membros especializados da equipe | • Têm papéis específicos • Usam ferramentas designadas • Podem delegar tarefas • Tomam decisões autônomas |
| **Process** | Sistema de gerenciamento de workflow | • Define padrões de colaboração • Controla atribuições de tarefas • Gerencia interações • Garante execução eficiente |
| **Tasks** | Atribuições individuais | • Têm objetivos claros • Usam ferramentas específicas • Alimentam processos maiores • Produzem resultados acionáveis |

### Quando Usar Crews vs Flows

| Caso de Uso | Abordagem Recomendada | Por quê? |
|-------------|----------------------|----------|
| Pesquisa aberta | Crews | Tarefas requerem pensamento criativo e adaptação |
| Geração de conteúdo | Crews | Criação colaborativa de artigos, relatórios, materiais de marketing |
| Workflows de decisão | Flows | Necessidade de caminhos de decisão previsíveis e auditáveis |
| Orquestração de API | Flows | Integração confiável com múltiplos serviços externos |
| Aplicações híbridas | Abordagem combinada | Flows para processo geral com Crews para subtarefas complexas |

## Instalação e Configuração

### Requisitos

- Python >=3.10 <3.14
- UV para gerenciamento de dependências

### Instalação Básica

```bash
pip install crewai
```

### Instalação com Ferramentas Extras

```bash
pip install 'crewai[tools]'
```

### Criando um Novo Projeto

```bash
crewai create crew <nome_do_projeto>
```

### Estrutura do Projeto

```text
meu_projeto/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── meu_projeto/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

## Características Principais

### ✨ Recursos Únicos

- **Framework Independente**: Construído do zero, independente do LangChain
- **Alto Desempenho**: Otimizado para velocidade e uso mínimo de recursos
- **Customização Flexível**: Liberdade completa para customizar em níveis altos e baixos
- **Pronto para Produção**: Construído para confiabilidade e escalabilidade
- **Foco em Segurança**: Projetado com requisitos de segurança empresarial
- **Custo-Eficiente**: Otimizado para minimizar uso de tokens e chamadas de API

### 🧠 Operação Autônoma

- Agentes tomam decisões inteligentes baseadas em seus papéis
- Comunicação e colaboração natural entre agentes
- Design extensível para adicionar novas ferramentas e capacidades

### 📚 Recursos de Aprendizado

- **Mais de 100.000 desenvolvedores certificados**
- Cursos abrangentes em learn.crewai.com:
  - Multi AI Agent Systems with CrewAI
  - Practical Multi AI Agents and Advanced Use Cases

## Integração com MCP (Model Context Protocol)

O CrewAI suporta integração com servidores MCP através de diferentes transportes:

- Stdio Transport
- SSE Transport
- Streamable HTTP Transport
- Conexão com múltiplos servidores MCP
- Considerações de segurança MCP

## Observabilidade e Monitoramento

Integrações disponíveis:

- Arize Phoenix
- LangDB, Langfuse, Langtrace
- MLflow, Maxim
- OpenLIT, Opik
- Portkey, Weave
- TrueFoundry
- E muitas outras

## Casos de Uso Comuns

### Crews (Equipes Autônomas)

- Análise de pesquisa aberta
- Geração colaborativa de conteúdo
- Resolução criativa de problemas
- Tomada de decisão adaptativa

### Flows (Workflows Estruturados)

- Processos de aprovação
- Orquestração de API
- Pipelines de dados
- Automações determinísticas

### Combinação (Crews + Flows)

- Aplicações empresariais complexas
- Sistemas híbridos que requerem tanto autonomia quanto controle
- Processos que alternam entre estrutura rígida e criatividade

## Links Úteis

- **GitHub**: <https://github.com/crewAIInc/crewAI>
- **Documentação**: <https://docs.crewai.com>
- **Website Oficial**: <https://crewai.com>
- **Fórum**: Forum CrewAI
- **Crew GPT**: Crew GPT
- **Releases**: GitHub Releases
- **Cursos**: learn.crewai.com

---

*Este arquivo será usado como referência durante o desenvolvimento e pode ser atualizado conforme necessário.*
