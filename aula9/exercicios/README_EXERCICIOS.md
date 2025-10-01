# 🎓 Exercícios Práticos - Aula 9: Multi-Agente

## 📚 Introdução aos Exercícios

Os exercícios da **Aula 9** são projetados para aprofundar seu conhecimento em **sistemas multi-agente** com CrewAI, explorando diferentes aspectos da coordenação entre agentes especializados.

## 🎯 Objetivos de Aprendizado

Ao completar estes exercícios, você será capaz de:

- ✅ Criar agentes especializados com diferentes expertise
- ✅ Implementar ferramentas customizadas para cada agente
- ✅ Configurar processos de coordenação entre agentes
- ✅ Desenvolver sistemas de classificação automática
- ✅ Otimizar performance em sistemas multi-agente

## 📋 Lista de Exercícios

### 🟢 **Exercício 1: Criando um 4º Agente Especializado**

**Arquivo**: `exercicio1_agente_personalizado.py`

**Objetivo**: Adicionar um novo agente especializado ao sistema da Aula 9

**Desafio**: Criar um "Agente Geográfico" que se especializa em:

- Análises de localização e proximidade
- Mapas de cobertura por região
- Distâncias entre estabelecimentos
- Análises de acessibilidade geográfica

**Requisitos técnicos**:

- Implementar `GeograficoTool` customizada
- Configurar agente com backstory específico
- Integrar ao processo hierarchical existente
- Adicionar palavras-chave para classificação automática

---

### 🟡 **Exercício 2: Ferramenta Especializada Avançada**

**Arquivo**: `exercicio2_ferramenta_especializada.py`

**Objetivo**: Desenvolver uma ferramenta completamente nova

**Desafio**: Criar "AnaliseTemporalTool" que analisa:

- Padrões temporais de atendimentos
- Sazonalidade de queixas específicas
- Evolução histórica dos dados
- Predições baseadas em tendências

**Requisitos técnicos**:

- Herdar de `BaseTool` corretamente
- Implementar análises temporais complexas
- Gerar gráficos ou visualizações textuais
- Integrar com agente existente ou novo

---

### 🔴 **Exercício 3: Sistema de Coordenação Personalizado**

**Arquivo**: `exercicio3_coordenacao_avancada.py`

**Objetivo**: Implementar processo de coordenação customizado

**Desafio**: Criar sistema onde:

- Agente Analisador sempre executa primeiro
- Agente Especialista apropriado executa segundo
- Agente "Consolidador" combina resultados
- Sistema retorna relatório final integrado

**Requisitos técnicos**:

- Usar `Process.sequential` com ordem específica
- Implementar contexto compartilhado entre tarefas
- Criar agente "Consolidador" novo
- Gerar relatório final unificado

## 📁 Estrutura de Arquivos

```
aula9/exercicios/
├── README_EXERCICIOS.md              # Este arquivo
├── exercicio1_agente_personalizado.py # Exercício 1
├── exercicio2_ferramenta_especializada.py # Exercício 2  
├── exercicio3_coordenacao_avancada.py # Exercício 3
├── solucoes/                         # Soluções dos exercícios
│   ├── solucao_exercicio1.py
│   ├── solucao_exercicio2.py
│   └── solucao_exercicio3.py
└── templates/                        # Templates para começar
    ├── template_agente.py
    ├── template_ferramenta.py
    └── template_coordenacao.py
```

## 🛠️ Recursos de Apoio

### 📖 **Documentação de Referência**

- **CrewAI Agents**: <https://docs.crewai.com/core-concepts/agents>
- **Custom Tools**: <https://docs.crewai.com/tools/custom-tools>
- **Process Types**: <https://docs.crewai.com/core-concepts/processes>
- **Task Management**: <https://docs.crewai.com/core-concepts/tasks>

### 💡 **Dicas Importantes**

1. **Sempre teste** cada componente individualmente antes de integrar
2. **Use verbose=True** durante desenvolvimento para debug
3. **Implemente tratamento de erros** robusto
4. **Documente bem** o propósito de cada agente/ferramenta
5. **Otimize queries SQL** para performance

### 🔧 **Comandos Úteis**

```bash
# Executar exercício específico
uv run aula9/exercicios/exercicio1_agente_personalizado.py

# Testar ferramenta isoladamente  
uv run aula9/exercicios/exercicio2_ferramenta_especializada.py

# Executar sistema coordenado
uv run aula9/exercicios/exercicio3_coordenacao_avancada.py

# Verificar solução oficial
uv run aula9/exercicios/solucoes/solucao_exercicio1.py
```

## 🎯 Critérios de Avaliação

### ✅ **Exercício 1 - Agente Personalizado**

**Básico (60%)**:

- [ ] Agente criado com role, goal e backstory apropriados
- [ ] Ferramenta customizada implementada
- [ ] Integração básica com sistema existente

**Intermediário (80%)**:

- [ ] Palavras-chave adicionadas ao classificador
- [ ] Agente responde corretamente ao seu domínio
- [ ] Formatação de respostas otimizada

**Avançado (100%)**:

- [ ] Análises geográficas complexas implementadas
- [ ] Performance otimizada com queries eficientes
- [ ] Documentação completa e exemplos de uso

### ✅ **Exercício 2 - Ferramenta Especializada**

**Básico (60%)**:

- [ ] Classe herda de BaseTool corretamente
- [ ] Método `_run()` implementado funcionalmente
- [ ] Acesso ao banco SQLite funcionando

**Intermediário (80%)**:

- [ ] Análises temporais implementadas
- [ ] Múltiplos tipos de análise suportados
- [ ] Tratamento de erros robusto

**Avançado (100%)**:

- [ ] Análises estatísticas avançadas
- [ ] Visualizações textuais ou gráficos
- [ ] Performance otimizada para grandes datasets

### ✅ **Exercício 3 - Coordenação Avançada**

**Básico (60%)**:

- [ ] Sistema executa agentes em ordem correta
- [ ] Contexto básico compartilhado entre tarefas
- [ ] Relatório final gerado

**Intermediário (80%)**:

- [ ] Agente Consolidador implementado
- [ ] Integração fluida entre resultados
- [ ] Formatação profissional do relatório

**Avançado (100%)**:

- [ ] Sistema robusto com tratamento de falhas
- [ ] Métricas de qualidade implementadas
- [ ] Extensibilidade para novos agentes

## 🚀 Execução dos Exercícios

### 📋 **Pré-requisitos**

1. **Aula 9 funcionando**: `uv run aula9/main.py`
2. **Banco SQLite**: Arquivo `db/curso.db` presente
3. **API Key**: OpenAI configurada no `.env`
4. **Dependências**: `uv sync` executado

### 🔄 **Workflow Recomendado**

1. **Leia o README** do exercício específico
2. **Analise o template** fornecido (se disponível)
3. **Implemente gradualmente** testando cada parte
4. **Execute e teste** a funcionalidade
5. **Compare com solução** oficial
6. **Refine e otimize** sua implementação

### 🧪 **Como Testar**

```bash
# Teste 1: Execução básica
uv run aula9/exercicios/exercicio1_agente_personalizado.py

# Teste 2: Modo verbose para debug
VERBOSE=True uv run aula9/exercicios/exercicio1_agente_personalizado.py

# Teste 3: Com pergunta específica
echo "Mostre estabelecimentos próximos ao centro" | uv run aula9/exercicios/exercicio1_agente_personalizado.py
```

## 💡 **Dicas Avançadas**

### 🔧 **Para Exercício 1 (Agente Geográfico)**

```python
# Exemplo de estrutura para análise geográfica
class GeograficoTool(BaseTool):
    def _calcular_distancia_aproximada(self, endereco1, endereco2):
        # Implementar cálculo de distância baseado em endereços
        pass
    
    def _analisar_cobertura_regional(self, bairro_central):
        # Analisar estabelecimentos em raio de X km
        pass
    
    def _mapear_acessibilidade(self):
        # Analisar facilidade de acesso por região
        pass
```

### 🔧 **Para Exercício 2 (Análise Temporal)**

```python
# Exemplo de estrutura para análise temporal
class AnaliseTemporalTool(BaseTool):
    def _analisar_tendencia_queixas(self, periodo_meses):
        # Analisar evolução de queixas ao longo do tempo
        pass
    
    def _detectar_sazonalidade(self, tipo_queixa):
        # Identificar padrões sazonais
        pass
    
    def _prever_demanda(self, estabelecimento_id):
        # Predição básica baseada em histórico
        pass
```

### 🔧 **Para Exercício 3 (Coordenação)**

```python
# Exemplo de estrutura para coordenação
def criar_agente_consolidador():
    return Agent(
        role="Consolidador de Análises",
        goal="Integrar resultados de múltiplos agentes",
        backstory="Especialista em síntese de informações...",
        tools=[ConsolidadorTool()]
    )

def executar_coordenacao_sequencial(pergunta):
    # 1. Análise automática
    # 2. Execução especializada  
    # 3. Consolidação final
    # 4. Relatório integrado
    pass
```

## 🏆 **Desafios Extras (Opcional)**

### 🌟 **Desafio 1: Performance**

Otimize seu sistema para responder em **menos de 2 segundos**:

- Cache de classificações
- Queries SQL otimizadas
- Paralelização quando possível

### 🌟 **Desafio 2: Robustez**

Implemente sistema à prova de falhas:

- Retry logic para falhas de API
- Fallback para agente genérico
- Logs detalhados de debugging

### 🌟 **Desafio 3: Extensibilidade**

Crie sistema facilmente extensível:

- Interface comum para novos agentes
- Sistema de plugins para ferramentas
- Configuração via arquivo JSON

## 📊 **Métricas de Sucesso**

Ao completar os exercícios, você deve atingir:

- ✅ **90%+ precisão** na classificação de consultas
- ✅ **100% cobertura** de tipos de consulta implementados
- ✅ **< 3 segundos** tempo médio de resposta
- ✅ **Zero falhas** em cenários de teste padrão
- ✅ **Código limpo** com documentação adequada

## 🤝 **Suporte e Comunidade**

### 💬 **Onde buscar ajuda**

- **Discord do curso**: Canal #aula9-exercicios
- **Issues GitHub**: Para bugs específicos
- **Documentação**: Arquivos `/docs/` do projeto
- **Soluções oficiais**: Pasta `solucoes/` após tentativas

### 📝 **Como compartilhar soluções**

1. **Fork** o repositório do curso
2. **Implemente** sua solução
3. **Teste** completamente
4. **Crie Pull Request** com descrição detalhada
5. **Participe** da discussão na comunidade

---

**🎯 Meta**: Dominar sistemas multi-agente criando especializações únicas e coordenação inteligente!

**⚡ Início**: Escolha um exercício e comece implementando: `uv run aula9/exercicios/exercicio1_agente_personalizado.py`

---

*Exercícios criados para Aula 9 - Multi-Agent Systems*
*Nível: Avançado | Duração estimada: 2-4 horas por exercício*
*Pré-requisito: Aula 9 completa e funcionando*
