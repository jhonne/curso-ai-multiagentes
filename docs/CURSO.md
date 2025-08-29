# Curso Básico de 20 Horas: Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI

**Nível:** Iniciante

**Carga Horária Total:** 20 horas

**Pré-requisitos:**

* Conhecimento básico de Python.
* Familiaridade com o conceito de APIs.
* Uma chave de API da OpenAI.

## Visão Geral do Curso:**

Este curso introdutório de 20 horas foi projetado para capacitar desenvolvedores a construir sistemas de chatbot sofisticados e inteligentes, aproveitando o poder da colaboração de múltiplos agentes de IA. Os alunos mergulharão no framework CrewAI para orquestrar equipes de agentes autônomos e utilizarão os modelos de linguagem da OpenAI para alimentar as capacidades de conversação e raciocínio desses agentes. Ao final do curso, os participantes terão o conhecimento prático para projetar, construir e implantar um chatbot com múltiplos agentes capaz de realizar tarefas complexas e interagir de forma dinâmica com os usuários.

---

### Módulo 1: Fundamentos do CrewAI (6 horas)

Este módulo introdutório foca nos conceitos centrais do CrewAI, estabelecendo a base para a construção de aplicações com múltiplos agentes.

#### Aula 1: Introdução à Inteligência Artificial de Agentes e ao CrewAI (2 horas)

* **Objetivos:**
  * Compreender o que são agentes de IA e o paradigma de sistemas de múltiplos agentes.
  * Conhecer a proposta e a arquitetura do CrewAI.
  * Configurar o ambiente de desenvolvimento.
* **Tópicos:**
  * O que é um Agente de IA?
  * Vantagens da abordagem multi-agente.
  * Apresentação do CrewAI: Agentes, Tarefas, Ferramentas e Processos.
  * Instalação do CrewAI e configuração das dependências.
  * Configurando sua chave de API da OpenAI no ambiente.
* **Exercício Prático:**
  * Instalar o CrewAI e bibliotecas associadas.
  * Configurar a chave de API da OpenAI como uma variável de ambiente.
  * Executar um script "Hello, World!" com um único agente CrewAI.

#### Aula 2: Construindo seu Primeiro Crew: Agentes e Tarefas (2 horas)**

* **Objetivos:**
  * Aprender a definir Agentes com papéis, objetivos e histórias de fundo (backstories).
  * Aprender a criar e atribuir Tarefas para os agentes.
* **Tópicos:**
  * A classe `Agent`: definindo `role`, `goal` e `backstory`.
  * A importância de "personalidades" para os agentes.
  * A classe `Task`: descrevendo a tarefa e o resultado esperado (`expected_output`).
  * Atribuindo tarefas a agentes específicos.
* **Exercício Prático:**
  * Criar um "Crew" simples com dois agentes: um pesquisador e um redator.
  * Definir uma tarefa de pesquisa para o primeiro agente e uma tarefa de resumo para o segundo.

#### Aula 3: Ferramentas (Tools) e Processos (Processes) no CrewAI (2 horas)**

* **Objetivos:**
  * Entender como equipar agentes com ferramentas para interagir com o mundo exterior.
  * Aprender sobre os diferentes tipos de processos de execução de tarefas.
* **Tópicos:**
  * O que são Ferramentas (Tools) no CrewAI?
  * Utilizando ferramentas pré-construídas (e.g., busca na web).
  * O conceito de Processos: Sequencial vs. Hierárquico.
  * Orquestrando o fluxo de trabalho do seu "Crew".
* **Exercício Prático:**
  * Adicionar uma ferramenta de busca à internet ao agente pesquisador.
  * Configurar um processo sequencial para que o redator utilize o resultado da pesquisa do primeiro agente.

---

### Módulo 2: Construindo um Chatbot com Múltiplos Agentes (10 horas)

Este módulo foca na aplicação prática dos conceitos do CrewAI para desenvolver um chatbot funcional.

#### Aula 4: Arquitetura de um Chatbot Multi-Agente (2 horas)**

* **Objetivos:**
  * Projetar a arquitetura de um chatbot com diferentes agentes especializados.
  * Definir os papéis e responsabilidades de cada agente no chatbot.
* **Tópicos:**
  * Por que usar múltiplos agentes para um chatbot?
  * Definindo os agentes necessários:
    * **Agente de Saudação e Triagem:** Recebe a primeira mensagem do usuário.
    * **Agente de Extração de Intenção:** Identifica o que o usuário deseja.
    * **Agente de Busca de Informação:** Coleta dados relevantes (de uma base de conhecimento ou da web).
    * **Agente de Geração de Resposta:** Formula a resposta final para o usuário.
  * Desenhando o fluxo de conversação entre os agentes.

#### Aula 5: Otimização e Configuração Avançada dos Agentes (3 horas)**

* **Objetivos:**
  * Otimizar o desempenho individual de cada agente através de prompts refinados.
  * Configurar parâmetros avançados dos modelos OpenAI para diferentes tipos de agentes.
  * Implementar testes unitários e debugging para agentes individuais.
  * Estabelecer métricas de qualidade e monitoramento de custos.
* **Tópicos:**
  * **Engenharia de Prompts Avançada:**
    * Técnicas de prompt engineering específicas para cada tipo de agente
    * Utilizando few-shot learning e chain-of-thought prompting
    * Otimização de prompts para reduzir tokens e melhorar precisão
  * **Configuração de Modelos OpenAI:**
    * Ajuste de parâmetros: temperature, max_tokens, top_p
    * Escolha do modelo ideal para cada agente (GPT-3.5 vs GPT-4)
    * Implementação de fallbacks entre modelos
  * **Testes e Debugging:**
    * Criando casos de teste para cada agente
    * Utilizando o modo `verbose=True` para debugging
    * Logs estruturados para monitoramento de desempenho
  * **Monitoramento de Custos e Performance:**
    * Tracking de uso de tokens por agente
    * Implementação de cache para respostas similares
    * Métricas de latência e qualidade de resposta
* **Exercício Prático:**
  * Criar uma suite de testes unitários para cada agente definido na Aula 4
  * Otimizar os prompts de cada agente usando técnicas avançadas
  * Implementar um sistema de monitoramento de custos e performance
  * Configurar diferentes parâmetros de modelo para cada tipo de agente

#### Aula 6: Gerenciando o Fluxo da Conversa e as Tarefas (3 horas)**

* **Objetivos:**
  * Orquestrar a interação entre os agentes do chatbot.
  * Gerenciar o estado da conversa.
* **Tópicos:**
  * Criando as Tarefas para cada agente com base na entrada do usuário.
  * Utilizando o processo sequencial para garantir a ordem correta de execução.
  * Passando a saída de uma tarefa como entrada para a próxima.
  * Como lidar com a entrada do usuário de forma dinâmica.
* **Exercício Prático:**
  * Implementar a lógica principal do chatbot que recebe a entrada do usuário e inicia o "Crew".
  * Conectar as tarefas em uma sequência lógica.

#### Aula 7: Criando uma Interface de Chat Simples (2 horas)**

* **Objetivos:**
  * Integrar o "Crew" do chatbot a uma interface de linha de comando (CLI) ou a uma interface web simples.
* **Tópicos:**
  * Construindo um loop `while` para manter a conversa ativa no terminal.
  * (Opcional) Introdução ao Streamlit ou Flask para criar uma interface web básica.
  * Exibindo a resposta final do "Crew" para o usuário.
* **Exercício Prático:**
  * Desenvolver uma aplicação de console que permita ao usuário conversar com o chatbot.

---

### Módulo 3: Tópicos Avançados e Próximos Passos (4 horas)

Este módulo final explora funcionalidades mais avançadas e aponta direções para o aprimoramento contínuo do chatbot.

#### Aula 8: Adicionando Memória e Ferramentas Personalizadas (2 horas)**

* **Objetivos:**
  * Entender a importância da memória em conversas de chatbot.
  * Aprender a criar ferramentas personalizadas para estender as capacidades dos agentes.
* **Tópicos:**
  * Conceitos de memória de curto e longo prazo para chatbots.
  * Estratégias para passar o histórico da conversa para o "Crew".
  * Desenvolvendo uma ferramenta personalizada em Python (e.g., para consultar um banco de dados interno).
  * Atribuindo a nova ferramenta a um agente específico.
* **Exercício Prático:**
  * Modificar o chatbot para que ele se lembre do nome do usuário e o utilize em conversas futuras.
  * Criar uma ferramenta simples que retorna a data e hora atuais.

#### Aula 9: Debugging, Avaliação e Próximos Passos (2 horas)

* **Objetivos:**
  * Aprender a depurar e avaliar o desempenho do "Crew" de agentes.
  * Explorar tópicos avançados e como continuar aprendendo.
* **Tópicos:**
  * Utilizando o modo `verbose=True` para entender o processo de pensamento dos agentes.
  * Estratégias para avaliar a qualidade das respostas do chatbot.
  * Introdução a conceitos como RAG (Retrieval-Augmented Generation) com CrewAI.
  * Ideias para projetos futuros e como contribuir para a comunidade CrewAI.
* **Projeto Final (sugestão):**
  * Aprimorar o chatbot para um caso de uso específico (e.g., um chatbot de atendimento ao cliente para um e-commerce fictício, um assistente de pesquisa pessoal).
  * Apresentar o chatbot e o fluxo de trabalho dos agentes.

---

## Sugestões de Melhoria e Tópicos Complementares

### Aula 10: Boas Práticas, Segurança e Tratamento de Erros (2 horas) - **ADICIONAL**

* **Objetivos:**
  * Implementar práticas de segurança e robustez no chatbot.
  * Aprender a lidar com falhas e erros de forma elegante.
* **Tópicos:**
  * **Tratamento de Erros:**
    * Lidando com falhas de API da OpenAI (timeouts, rate limits)
    * Implementando retry logic e fallbacks
    * Tratamento de exceções em agentes e tarefas
  * **Segurança:**
    * Sanitização de inputs do usuário
    * Implementação de rate limiting
    * Práticas de segurança para chaves de API
  * **Gerenciamento de Custos:**
    * Monitoramento de uso de tokens
    * Estratégias para otimizar custos com OpenAI
    * Implementação de cache para respostas similares
* **Exercício Prático:**
  * Adicionar tratamento de erros robusto ao chatbot
  * Implementar um sistema simples de cache de respostas

### Recursos Complementares Recomendados

#### **Materiais de Apoio:**

* **Repositório GitHub:** Código completo dos exercícios e soluções
* **Documentação Oficial:** Links para CrewAI e OpenAI documentation
* **Vídeos Complementares:** Demonstrações práticas de cada aula
* **Templates de Código:** Estruturas base para acelerar o desenvolvimento

#### **Tópicos para Aprofundamento:**

* **Performance e Otimização:**
  * Implementação de cache inteligente
  * Otimização de prompts para reduzir tokens
  * Paralelização de tarefas quando possível
* **Deploy em Produção:**
  * Containerização com Docker
  * Deploy em cloud (AWS, GCP, Azure)
  * Monitoramento e logging em produção
* **Casos de Uso Avançados:**
  * Integração com RAG (Retrieval-Augmented Generation)
  * Chatbots especializados por domínio
  * Sistemas híbridos (humano + IA)

#### **Comparação com Outras Ferramentas:**

* **LangChain vs CrewAI:** Quando usar cada framework
* **AutoGen vs CrewAI:** Diferenças na arquitetura multi-agente
* **Análise de custo-benefício** de diferentes abordagens

#### **Sistema de Avaliação Sugerido:**

* **Quizzes teóricos** ao final de cada módulo
* **Projetos práticos** com critérios de avaliação claros
* **Peer review** entre alunos dos projetos finais
* **Certificado de conclusão** mediante aprovação

#### **Comunidade e Suporte:**

* **Fórum de discussão** para dúvidas e compartilhamento
* **Sessões de Q&A** semanais com instrutor
* **Showcase de projetos** dos alunos
* **Grupo no Discord/Slack** para networking

#### **Próximos Passos após o Curso:**

* **Projetos sugeridos** para portfolio
* **Contribuições open-source** para a comunidade CrewAI
* **Especializações avançadas** (MLOps, AI Ethics, etc.)
* **Roadmap de carreira** em AI Engineering

### Versionamento e Dependências Recomendadas

```python
# requirements.txt sugerido
crewai>=0.28.0
openai>=1.12.0
python-dotenv>=1.0.0
streamlit>=1.28.0  # para interface web
flask>=2.3.0       # alternativa para interface web
requests>=2.31.0
pydantic>=2.5.0
```

### Estimativa de Custos com OpenAI

| Modelo | Custo por 1K tokens | Uso estimado/aula | Custo estimado |
|--------|-------------------|------------------|----------------|
| GPT-3.5-turbo | $0.0015 input / $0.002 output | 10K tokens | $0.035 |
| GPT-4 | $0.03 input / $0.06 output | 5K tokens | $0.45 |

**Custo total estimado do curso:** $15-30 USD (dependendo do modelo escolhido)
