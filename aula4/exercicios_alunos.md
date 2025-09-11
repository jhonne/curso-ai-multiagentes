# 🎯 Exercícios Práticos - Aula 4: Cadeia de Agentes Especializados

Baseado no sistema de atendimento ao cliente demonstrado na aula, agora é hora de praticar criando suas próprias cadeias de agentes especializados!

## 🎓 Objetivos dos Exercícios

- Compreender a especialização de agentes
- Implementar comunicação sequencial entre agentes
- Otimizar para segurança e economia de custos
- Criar sistemas modulares e escaláveis

---

## 📋 Exercício 1: Sistema de Análise de Currículo (FÁCIL)

### 🎯 Objetivo

Criar uma cadeia de 3 agentes para analisar currículos e fornecer feedback profissional.

### 🏗️ Arquitetura Proposta

```
Currículo → Extrator → Avaliador → Conselheiro → Relatório Final
```

### 👥 Agentes Necessários

#### 1. **Agente Extrator de Dados**

- **Role**: "Extrator de Informações de Currículo"
- **Goal**: "Extrair informações estruturadas do currículo"
- **Backstory**: "Especialista em análise documental com foco em dados profissionais"
- **Output**: JSON com dados extraídos

#### 2. **Agente Avaliador**

- **Role**: "Avaliador de Currículo"
- **Goal**: "Avaliar qualidade e pontos fortes/fracos"
- **Backstory**: "Recrutador experiente com 10 anos de mercado"
- **Output**: Análise estruturada com pontuação

#### 3. **Agente Conselheiro**

- **Role**: "Conselheiro de Carreira"
- **Goal**: "Fornecer feedback construtivo e sugestões"
- **Backstory**: "Coach de carreira especialista em desenvolvimento profissional"
- **Output**: Relatório amigável com recomendações

### 📁 Base de Dados Simulada

```python
CRITERIOS_AVALIACAO = {
    "experiencia": {"peso": 30, "descricao": "Anos e relevância da experiência"},
    "educacao": {"peso": 25, "descricao": "Formação acadêmica e certificações"},
    "habilidades": {"peso": 25, "descricao": "Skills técnicas e comportamentais"},
    "apresentacao": {"peso": 20, "descricao": "Clareza e organização do currículo"}
}

FEEDBACK_TEMPLATES = {
    "pontos_fortes": "Principais qualificações identificadas",
    "areas_melhoria": "Aspectos que podem ser aprimorados",
    "sugestoes": "Recomendações específicas de melhoria"
}
```

### 🚀 Implementação Base

```python
# Configuração otimizada para economia
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Modelo mais econômico
    temperature=0.1,      # Consistência
    max_tokens=800        # Limite de resposta
)

# Tarefa para o Extrator
tarefa_extracao = Task(
    description="""
    Extraia informações do currículo: {curriculo_texto}
    
    FORMATO JSON OBRIGATÓRIO:
    {{
        "nome": "nome_candidato",
        "experiencia_anos": número,
        "educacao": "formação_principal",
        "habilidades": ["skill1", "skill2", "skill3"],
        "cargo_atual": "posição_atual"
    }}
    
    LIMITE: Resposta em máximo 200 palavras.
    """,
    agent=agente_extrator,
    expected_output="JSON estruturado com dados do currículo"
)
```

### ✅ Critério de Sucesso

- [ ] 3 agentes especializados funcionando
- [ ] Comunicação sequencial implementada
- [ ] Output final útil e estruturado
- [ ] Uso do modelo gpt-4o-mini para economia
- [ ] Limites de tokens configurados

---

## 📋 Exercício 2: Sistema de Planejamento de Viagem (MÉDIO)

### 🎯 Objetivo

Criar uma cadeia de 4 agentes para planejamento completo de viagens personalizadas.

### 🏗️ Arquitetura Proposta

```
Preferências → Pesquisador → Organizador → Orçamentista → Itinerário Final
```

### 👥 Agentes Necessários

#### 1. **Agente Analisador de Preferências**

- **Role**: "Analisador de Preferências de Viagem"
- **Goal**: "Compreender perfil e preferências do viajante"
- **Output**: Perfil estruturado do viajante

#### 2. **Agente Pesquisador de Destinos**

- **Role**: "Pesquisador de Destinos e Atrações"
- **Goal**: "Buscar melhores opções de destinos e atividades"
- **Output**: Lista de destinos e atrações recomendadas

#### 3. **Agente Organizador de Roteiro**

- **Role**: "Organizador de Itinerário"
- **Goal**: "Estruturar cronograma otimizado da viagem"
- **Output**: Roteiro dia a dia detalhado

#### 4. **Agente Especialista em Orçamento**

- **Role**: "Consultor Financeiro de Viagens"
- **Goal**: "Calcular custos e sugerir alternativas econômicas"
- **Output**: Orçamento detalhado com opções

### 📁 Base de Dados Simulada

```python
DESTINOS_DB = {
    "praia": {
        "nacionais": ["Florianópolis", "Porto de Galinhas", "Jericoacoara"],
        "internacionais": ["Cancún", "Punta Cana", "Mykonos"],
        "custo_medio_dia": {"nacional": 200, "internacional": 300}
    },
    "montanha": {
        "nacionais": ["Campos do Jordão", "Gramado", "Monte Verde"],
        "internacionais": ["Bariloche", "Aspen", "Chamonix"],
        "custo_medio_dia": {"nacional": 180, "internacional": 250}
    },
    "cultural": {
        "nacionais": ["Salvador", "Ouro Preto", "São Luís"],
        "internacionais": ["Paris", "Roma", "Kyoto"],
        "custo_medio_dia": {"nacional": 150, "internacional": 280}
    }
}

TIPOS_HOSPEDAGEM = {
    "econômica": {"multiplicador": 0.7, "exemplos": ["Hostel", "Pousada"]},
    "padrão": {"multiplicador": 1.0, "exemplos": ["Hotel 3-4 estrelas"]},
    "luxo": {"multiplicador": 2.0, "exemplos": ["Resort", "Hotel 5 estrelas"]}
}
```

### 🛡️ Implementação com Segurança

```python
def criar_agente_seguro(role, goal, backstory):
    """Cria agente com configurações de segurança e economia"""
    
    # Backstory otimizado (máximo 300 caracteres)
    backstory_otimizado = backstory[:300] + "..." if len(backstory) > 300 else backstory
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory_otimizado,
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=600  # Limite para economia
        ),
        verbose=False  # Reduz output desnecessário
    )

def validar_entrada_viagem(preferencias):
    """Valida entrada do usuário"""
    campos_obrigatorios = ["destino_tipo", "orcamento", "duracao", "pessoas"]
    
    for campo in campos_obrigatorios:
        if campo not in preferencias:
            raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    if len(str(preferencias)) > 2000:  # Limite de caracteres
        raise ValueError("Entrada muito longa. Máximo 2000 caracteres.")
    
    return True
```

### ✅ Critério de Sucesso

- [ ] 4 agentes especializados funcionando
- [ ] Validação de entrada implementada
- [ ] Base de dados simulada utilizada
- [ ] Cálculo de orçamento funcional
- [ ] Monitoramento de custos da API

---

## 📋 Exercício 3: Sistema de Criação de Conteúdo (AVANÇADO)

### 🎯 Objetivo

Criar uma cadeia de 5 agentes para produção de conteúdo completo para redes sociais.

### 🏗️ Arquitetura Proposta

```
Briefing → Pesquisador → Estrategista → Criativo → Revisor → Conteúdo Final
```

### 👥 Agentes Necessários

#### 1. **Agente Analisador de Briefing**

- **Role**: "Analisador de Briefing de Conteúdo"
- **Goal**: "Compreender objetivos e público-alvo"
- **Especialização**: Interpretação de requisitos de marketing

#### 2. **Agente Pesquisador de Trends**

- **Role**: "Pesquisador de Tendências"
- **Goal**: "Identificar trends e tópicos relevantes"
- **Especialização**: Análise de mercado e comportamento digital

#### 3. **Agente Estrategista de Conteúdo**

- **Role**: "Estrategista de Conteúdo Digital"
- **Goal**: "Definir abordagem e formato de conteúdo"
- **Especialização**: Planejamento de campanhas digitais

#### 4. **Agente Criativo**

- **Role**: "Criador de Conteúdo"
- **Goal**: "Produzir conteúdo engajante e original"
- **Especialização**: Copywriting e storytelling

#### 5. **Agente Revisor**

- **Role**: "Editor e Revisor de Conteúdo"
- **Goal**: "Garantir qualidade e conformidade"
- **Especialização**: Edição e controle de qualidade

### 📁 Base de Dados Simulada

```python
PLATAFORMAS_CONFIG = {
    "instagram": {
        "limite_caracteres": 2200,
        "hashtags_recomendadas": 5,
        "formatos": ["carrossel", "story", "reel", "post_único"]
    },
    "linkedin": {
        "limite_caracteres": 3000,
        "hashtags_recomendadas": 3,
        "formatos": ["artigo", "post_profissional", "poll"]
    },
    "twitter": {
        "limite_caracteres": 280,
        "hashtags_recomendadas": 2,
        "formatos": ["thread", "post_único", "reply"]
    }
}

TRENDS_TEMAS = {
    "tecnologia": ["IA", "automação", "futuro do trabalho", "inovação"],
    "negócios": ["empreendedorismo", "liderança", "produtividade", "vendas"],
    "lifestyle": ["bem-estar", "sustentabilidade", "desenvolvimento pessoal"]
}

TEMPLATES_CONTEUDO = {
    "educativo": "Como fazer X: [passo a passo]",
    "inspiracional": "A história de [pessoa] que [conquista]",
    "dica_rápida": "3 maneiras de [objetivo] em [tempo]",
    "pergunta_engajamento": "Qual sua opinião sobre [tópico]?"
}
```

### 🔒 Implementação com Segurança Avançada

```python
import hashlib
from openai import OpenAI

class CrewAIContentSecurity:
    def __init__(self):
        self.client = OpenAI()
        self.safety_identifiers = {}
        
    def gerar_safety_id(self, usuario_email):
        """Gera identificador de segurança"""
        return hashlib.sha256(usuario_email.encode()).hexdigest()[:16]
    
    def verificar_conteudo_seguro(self, texto):
        """Verifica se conteúdo é apropriado"""
        try:
            response = self.client.moderations.create(input=texto)
            return not response.results[0].flagged
        except Exception as e:
            print(f"Erro na moderação: {e}")
            return False  # Conservador em caso de erro
    
    def processar_briefing_seguro(self, briefing, usuario_email):
        """Processa briefing com verificações de segurança"""
        # 1. Validar entrada
        if len(briefing) > 3000:
            raise ValueError("Briefing muito longo. Máximo 3000 caracteres.")
        
        # 2. Verificar moderação
        if not self.verificar_conteudo_seguro(briefing):
            raise ValueError("Briefing contém conteúdo inadequado.")
        
        # 3. Registrar safety identifier
        safety_id = self.gerar_safety_id(usuario_email)
        self.safety_identifiers[safety_id] = {
            "usuario": usuario_email,
            "timestamp": time.time()
        }
        
        return safety_id

# Monitor de custos
class MonitorCustos:
    def __init__(self, orcamento=5.0):
        self.orcamento = orcamento
        self.gasto_atual = 0.0
        self.precos = {
            "gpt-4o-mini": {"input": 0.15/1000000, "output": 0.60/1000000}
        }
    
    def estimar_custo(self, texto_entrada, tamanho_resposta_esperado):
        """Estima custo da operação"""
        tokens_input = len(texto_entrada) * 0.25
        tokens_output = tamanho_resposta_esperado
        
        custo = (tokens_input * self.precos["gpt-4o-mini"]["input"] + 
                tokens_output * self.precos["gpt-4o-mini"]["output"])
        
        return custo
    
    def verificar_orcamento(self, custo_estimado):
        """Verifica se operação cabe no orçamento"""
        if self.gasto_atual + custo_estimado > self.orcamento:
            raise Exception(f"Custo excederia orçamento. Atual: ${self.gasto_atual:.4f}")
        return True
    
    def registrar_gasto(self, custo):
        """Registra gasto realizado"""
        self.gasto_atual += custo
        if self.gasto_atual > self.orcamento * 0.8:
            print(f"⚠️ 80% do orçamento usado: ${self.gasto_atual:.4f}/${self.orcamento:.4f}")
```

### 🎨 Cache Inteligente para Economia

```python
import json
import time

class CacheConteudo:
    def __init__(self, ttl=1800):  # 30 minutos
        self.cache = {}
        self.ttl = ttl
    
    def gerar_chave(self, briefing, plataforma, tipo_conteudo):
        """Gera chave única para cache"""
        key_string = f"{briefing}|{plataforma}|{tipo_conteudo}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def buscar_cache(self, briefing, plataforma, tipo_conteudo):
        """Busca conteúdo no cache"""
        chave = self.gerar_chave(briefing, plataforma, tipo_conteudo)
        
        if chave in self.cache:
            timestamp, conteudo = self.cache[chave]
            if time.time() - timestamp < self.ttl:
                print("✅ Cache HIT - Economia de $0.02")
                return conteudo
            else:
                del self.cache[chave]
        
        return None
    
    def salvar_cache(self, briefing, plataforma, tipo_conteudo, conteudo):
        """Salva conteúdo no cache"""
        chave = self.gerar_chave(briefing, plataforma, tipo_conteudo)
        self.cache[chave] = (time.time(), conteudo)
```

### ✅ Critério de Sucesso

- [ ] 5 agentes especializados funcionando
- [ ] Sistema de moderação implementado
- [ ] Cache para economia funcionando
- [ ] Monitoramento de custos ativo
- [ ] Safety identifiers configurados
- [ ] Validação de entrada completa

---

## 🎯 Exercício 4: Sistema de Suporte Técnico (EXPERT)

### 🎯 Objetivo

Criar um sistema completo de diagnóstico e resolução de problemas técnicos.

### 🏗️ Arquitetura Proposta

```
Problema → Triagem → Diagnosticador → Solucionador → Validador → Instruções Finais
```

### 👥 Agentes Necessários

#### 1. **Agente de Triagem**

- Classificar severidade e categoria do problema
- Identificar urgência e impacto

#### 2. **Agente Diagnosticador**

- Analisar sintomas e identificar causa raiz
- Solicitar informações adicionais se necessário

#### 3. **Agente Solucionador**

- Propor soluções baseadas no diagnóstico
- Considerar diferentes abordagens

#### 4. **Agente Validador**

- Verificar viabilidade da solução
- Identificar riscos potenciais

#### 5. **Agente Comunicador**

- Transformar solução técnica em instruções claras
- Adequar linguagem ao nível do usuário

### 📁 Base de Dados Simulada

```python
CATEGORIAS_PROBLEMAS = {
    "hardware": {
        "subcategorias": ["monitor", "teclado", "mouse", "impressora"],
        "severidade_media": "média",
        "tempo_resolucao": "2-4 horas"
    },
    "software": {
        "subcategorias": ["sistema", "aplicativo", "driver", "segurança"],
        "severidade_media": "alta",
        "tempo_resolucao": "1-2 horas"
    },
    "rede": {
        "subcategorias": ["internet", "wifi", "compartilhamento", "VPN"],
        "severidade_media": "alta",
        "tempo_resolucao": "30min-2 horas"
    }
}

SOLUCOES_CONHECIDAS = {
    "internet_lenta": [
        "Reiniciar roteador",
        "Verificar cabos",
        "Contatar provedor",
        "Atualizar drivers"
    ],
    "aplicativo_trava": [
        "Fechar e reabrir aplicativo",
        "Reiniciar computador",
        "Verificar atualizações",
        "Reinstalar aplicativo"
    ]
}
```

### ✅ Critério de Sucesso

- [ ] Sistema completo de 5 agentes
- [ ] Classificação automática de problemas
- [ ] Base de soluções funcionando
- [ ] Escalabilidade para novos tipos de problema
- [ ] Todas as práticas de segurança e economia implementadas

---

## 🛠️ Recursos para Desenvolvimento

### 📁 Estrutura de Arquivos Recomendada

```
exercicio_X/
├── main.py              # Arquivo principal
├── agentes.py           # Definições dos agentes
├── tarefas.py           # Definições das tarefas
├── utils.py             # Utilitários (cache, validação)
├── data.py              # Base de dados simulada
├── security.py          # Funções de segurança
└── README.md           # Documentação do exercício
```

### 🔧 Template Básico de Implementação

```python
# main.py - Template base
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from utils import CacheInteligente, MonitorCustos, validar_entrada
from security import CrewAISecurityManager

def main():
    # 1. Configuração de segurança
    security = CrewAISecurityManager()
    monitor = MonitorCustos(orcamento=3.0)
    cache = CacheInteligente()
    
    # 2. Configuração do LLM otimizado
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=500
    )
    
    # 3. Criar agentes
    agentes = criar_agentes(llm)
    
    # 4. Criar tarefas
    tarefas = criar_tarefas(agentes)
    
    # 5. Criar crew
    crew = Crew(
        agents=agentes,
        tasks=tarefas,
        process=Process.sequential,
        verbose=False
    )
    
    # 6. Executar com monitoramento
    entrada = input("Digite sua entrada: ")
    
    try:
        validar_entrada(entrada)
        custo_estimado = monitor.estimar_custo(entrada, 500)
        monitor.verificar_orcamento(custo_estimado)
        
        resultado = crew.kickoff(inputs={"entrada": entrada})
        
        monitor.registrar_gasto(custo_estimado)
        print(f"✅ Resultado: {resultado}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
```

### 🧪 Script de Teste para Cada Exercício

```python
# test_exercicio.py
def testar_exercicio():
    """Testa o exercício com entradas pré-definidas"""
    
    casos_teste = [
        {"entrada": "caso_simples", "esperado": "resultado_basico"},
        {"entrada": "caso_complexo", "esperado": "resultado_avancado"},
        {"entrada": "caso_limite", "esperado": "erro_validacao"}
    ]
    
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n🧪 Teste {i}: {caso['entrada']}")
        try:
            resultado = processar_entrada(caso["entrada"])
            print(f"✅ Sucesso: {resultado}")
        except Exception as e:
            print(f"⚠️ Erro: {e}")

# Para executar: python test_exercicio.py
```

---

## 🏆 Critérios de Avaliação

### ⭐ Básico (Exercício 1)

- [ ] **Funcionalidade**: Sistema funciona sem erros
- [ ] **Estrutura**: 3 agentes especializados
- [ ] **Comunicação**: Context entre tarefas funcionando
- [ ] **Economia**: Uso do gpt-4o-mini
- [ ] **Documentação**: README com instruções

### ⭐⭐ Intermediário (Exercício 2)

- [ ] **Tudo do básico** +
- [ ] **Validação**: Entrada validada adequadamente
- [ ] **Base de dados**: Simulação realista
- [ ] **Monitoramento**: Controle de custos implementado
- [ ] **Modularidade**: Código bem organizado

### ⭐⭐⭐ Avançado (Exercício 3)

- [ ] **Tudo do intermediário** +
- [ ] **Segurança**: API de moderação ativa
- [ ] **Cache**: Sistema de cache funcionando
- [ ] **Safety IDs**: Identificadores implementados
- [ ] **Robustez**: Tratamento de erros completo

### ⭐⭐⭐⭐ Expert (Exercício 4)

- [ ] **Tudo do avançado** +
- [ ] **Sistema completo**: 5+ agentes especializados
- [ ] **Escalabilidade**: Fácil adicionar novos tipos
- [ ] **Otimização**: <90% economia vs implementação básica
- [ ] **Produção ready**: Logs, métricas, alertas

---

## 🚀 Dicas de Implementação

### 💡 Para Economizar Custos

1. **Use sempre gpt-4o-mini** - Economia de 85%
2. **Implemente cache** - Pode economizar 50% adicional
3. **Limite outputs** - Evita respostas desnecessariamente longas
4. **Monitore gastos** - Alertas quando atingir 80% do orçamento

### 🛡️ Para Garantir Segurança

1. **Valide todas as entradas** - Limite caracteres e formato
2. **Use API de moderação** - Especialmente para conteúdo público
3. **Implemente safety identifiers** - Para rastreabilidade
4. **Trate erros graciosamente** - Não exponha informações internas

### 🎯 Para Melhor Qualidade

1. **Backstories concisos** - Máximo 300 caracteres
2. **Expected outputs específicos** - Seja claro sobre o formato
3. **Context apropriado** - Passe informações relevantes entre tarefas
4. **Teste com casos extremos** - Entradas inválidas, muito longas, etc.

---

## 📚 Recursos de Apoio

### 📖 Documentação

- [CrewAI Documentation](https://docs.crewai.com)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Arquivo local: CREWAI_REFERENCE.md](../docs/CREWAI_REFERENCE.md)

### 🔧 Códigos de Referência

- `main.py` - Sistema completo de atendimento
- `exemplo_simples.py` - Versão simplificada
- `../docs/GUIA_SEGURANCA.md` - Práticas de segurança
- `../docs/RESUMO_OTIMIZACAO_OPENAI.md` - Otimização de custos

### 💬 Quando Pedir Ajuda

- **Erro de API**: Verifique sua chave OpenAI
- **Agente não responde**: Revise o backstory e goal
- **Context não funciona**: Verifique a ordem das tarefas
- **Custos altos**: Implemente cache e use gpt-4o-mini

---

## 🎉 Entrega dos Exercícios

### 📤 O que Entregar

1. **Código fonte** completo funcionando
2. **README.md** com instruções de execução
3. **Exemplos de teste** com outputs esperados
4. **Relatório de custos** estimados por execução
5. **Screenshot** de uma execução bem-sucedida

### 📊 Formato do Relatório de Custos

```markdown
## Relatório de Custos - [Nome do Exercício]

### Configuração
- Modelo: gpt-4o-mini
- Agentes: X agentes
- Tarefas: X tarefas

### Custos por Execução
- Entrada média: X tokens
- Saída média: X tokens  
- Custo estimado: $X.XXXX

### Otimizações Implementadas
- [ ] Cache (economia: X%)
- [ ] Limites de output (economia: X%)
- [ ] Validação de entrada
- [ ] Monitoramento de gastos

### Total Estimado para 100 Execuções
- Sem otimizações: $X.XX
- Com otimizações: $X.XX
- **Economia: XX%**
```

### 🗓️ Prazos Sugeridos

- **Exercício 1**: 2-3 dias
- **Exercício 2**: 4-5 dias  
- **Exercício 3**: 6-7 dias
- **Exercício 4**: 8-10 dias

---

**🎯 Sucesso em seus exercícios! Lembre-se: especialização + comunicação + economia = CrewAI eficiente!**

*Para dúvidas específicas, consulte os arquivos de referência na pasta `docs/` ou os exemplos na aula 4.*
