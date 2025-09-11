# Aula 5: Otimização e Configuração Avançada dos Agentes

## 🎯 Objetivos da Aula

- Otimizar o desempenho individual de cada agente através de prompts refinados
- Configurar parâmetros avançados dos modelos OpenAI para diferentes tipos de agentes
- Implementar testes unitários e debugging para agentes individuais
- Estabelecer métricas de qualidade e monitoramento de custos

## 📁 Estrutura da Aula

```
aula5/
├── README.md                    # Este arquivo
├── main.py                      # Arquivo principal com exemplos
├── exemplos/
│   ├── 01_prompt_engineering.py # Técnicas avançadas de prompts
│   ├── 02_configuracao_modelos.py # Configuração de parâmetros OpenAI
│   ├── 03_testes_agentes.py     # Testes unitários para agentes
│   └── 04_monitoramento.py      # Sistema de monitoramento
├── templates/
│   ├── agente_otimizado.py      # Template para agentes otimizados
│   └── suite_testes.py          # Template para testes
└── exercicios/
    ├── exercicio1_prompts.py    # Exercício de prompt engineering
    ├── exercicio2_config.py     # Exercício de configuração
    └── exercicio3_testes.py     # Exercício de testes
```

## 🚀 Como Usar

1. **Configure seu ambiente:**

   ```bash
   pip install crewai openai python-dotenv pytest
   ```

2. **Configure sua chave OpenAI:**

   ```bash
   export OPENAI_API_KEY="sua_chave_aqui"
   ```

3. **Execute os exemplos em ordem:**
   - Comece com `01_prompt_engineering.py`
   - Continue com `02_configuracao_modelos.py`
   - Teste com `03_testes_agentes.py`
   - Monitore com `04_monitoramento.py`

4. **Pratique com os exercícios:**
   - Complete os exercícios na pasta `exercicios/`
   - Use os templates como base

## 🔧 Conceitos Abordados

### 🎨 1. Engenharia de Prompts Avançada

> **💡 Few-shot Learning**  
> Técnica onde fornecemos **exemplos específicos** no prompt para ensinar o agente como realizar uma tarefa. Ao invés de apenas descrever o que queremos, mostramos exemplos concretos de entrada e saída esperada.
>
> ✅ *Resultado: Maior precisão e consistência nas respostas*

> **🧠 Chain-of-thought Prompting**  
> Método que encoraja o agente a **"pensar em voz alta"**, quebrando problemas complexos em etapas menores e mais gerenciáveis. Isso melhora significativamente a qualidade das respostas para tarefas que requerem raciocínio.
>
> ✅ *Resultado: Respostas mais estruturadas e lógicas*

> **⚡ Otimização para Redução de Tokens**  
> Estratégias para tornar os prompts **mais eficientes**, mantendo a qualidade das respostas mas reduzindo o número de tokens utilizados.
>
> ✅ *Resultado: Economia de custos e respostas mais rápidas*

### ⚙️ 2. Configuração de Modelos OpenAI

> **🌡️ Temperature (0.0 - 2.0)**  
> Controla a **criatividade/aleatoriedade** das respostas.
>
> - 📊 `0.1-0.3`: Tarefas que precisam de consistência
> - 🎨 `0.7-1.0`: Tarefas criativas

> **📏 Max_tokens**  
> Define o **número máximo de tokens** na resposta. Importante para controlar custos e garantir que as respostas tenham o tamanho adequado.

> **🎯 Top_p (0.0 - 1.0)**  
> Controla a **diversidade das respostas** através de amostragem por núcleo. Alternativa mais precisa ao temperature para controlar a aleatoriedade.

> **🤖 Escolha de Modelo**  
> Cada tipo de agente pode se beneficiar de modelos diferentes:
>
> - 🚀 `GPT-3.5`: Tarefas simples e rápidas
> - 🧠 `GPT-4`: Análises complexas e raciocínio avançado

### 🧪 3. Testes e Debugging

> **✅ Casos de Teste Unitários**  
> Desenvolvimento de **testes automatizados** para verificar se cada agente está funcionando corretamente em diferentes cenários.
>
> 🎯 *Objetivo: Garantir qualidade e confiabilidade*

> **👁️ Modo Verbose**  
> Ativação de **logs detalhados** que mostram o processo de pensamento dos agentes, facilitando a identificação de problemas e otimizações.
>
> 🔍 *Benefício: Debug mais eficiente*

> **📋 Logs Estruturados**  
> Sistema **organizado de logging** que permite rastrear o comportamento dos agentes, identificar gargalos e monitorar a performance ao longo do tempo.
>
> 📈 *Vantagem: Monitoramento contínuo*

### 📊 4. Monitoramento

> **💰 Tracking de Tokens**  
> Acompanhamento do **consumo de tokens** por agente e por tarefa.
>
> 💡 *Essencial para: Controle de custos e otimização de recursos*

> **🗄️ Cache de Respostas**  
> Sistema para **armazenar respostas frequentes**, evitando chamadas desnecessárias à API.
>
> 💸 *Benefício: Redução significativa de custos operacionais*

> **📈 Métricas de Performance**  
> Coleta e análise de dados sobre:
>
> - ⏱️ Tempo de resposta
> - ✅ Taxa de sucesso  
> - 🎯 Qualidade das respostas
> - 📊 Outros indicadores de performance

## ⚡ Dicas Importantes

- Use `verbose=True` durante desenvolvimento para entender o comportamento dos agentes
- Monitore sempre o uso de tokens para controlar custos
- Teste cada agente individualmente antes de integrar no sistema
- Documente os prompts que funcionam bem para reutilização

## 📚 Recursos Adicionais

- [Documentação CrewAI](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Python Testing with pytest](https://docs.pytest.org/)
