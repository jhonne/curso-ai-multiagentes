# 🎯 Guia de Implementação dos Exercícios - Aula 4

Este guia fornece instruções detalhadas para implementar cada exercício da aula 4, com foco em **cadeias de agentes especializados**.

## 📋 Visão Geral dos Exercícios

| Exercício | Complexidade | Agentes | Tempo Estimado | Conceitos Principais |
|-----------|--------------|---------|----------------|---------------------|
| **1 - Análise de Currículo** | 🟢 Fácil | 3 | 2-3 dias | Extração → Análise → Feedback |
| **2 - Planejamento de Viagem** | 🟡 Médio | 4 | 4-5 dias | Preferências → Pesquisa → Organização → Orçamento |
| **3 - Criação de Conteúdo** | 🟠 Avançado | 5 | 6-7 dias | Briefing → Pesquisa → Estratégia → Criação → Revisão |
| **4 - Suporte Técnico** | 🔴 Expert | 5 | 8-10 dias | Triagem → Diagnóstico → Solução → Validação → Comunicação |

---

## 🚀 Exercício 1: Sistema de Análise de Currículo (FÁCIL)

### 🎯 Objetivo

Criar uma cadeia de 3 agentes que analisam currículos e fornecem feedback profissional.

### 🔗 Fluxo da Cadeia

```
Currículo em Texto → Extrator → Avaliador → Conselheiro → Relatório Final
```

### 👥 Agentes Detalhados

#### 1. **Agente Extrator de Dados**

```python
agente_extrator = Agent(
    role="Extrator de Informações de Currículo",
    goal="Extrair dados estruturados de currículos de forma precisa e sistemática",
    backstory="""Especialista em análise documental com 8 anos de experiência 
    em RH. Expert em identificar e extrair informações relevantes.""",
    llm=llm_economico,
    verbose=False
)
```

**Tarefa:**

- **Input**: Texto completo do currículo
- **Output**: JSON estruturado com dados extraídos
- **Limite**: 150 palavras

#### 2. **Agente Avaliador**

```python
agente_avaliador = Agent(
    role="Avaliador de Currículo Profissional",
    goal="Avaliar qualidade e pontuar currículos segundo critérios objetivos",
    backstory="""Recrutador sênior com 12 anos de experiência. 
    Analisou mais de 5000 currículos de diversas áreas.""",
    llm=llm_economico,
    verbose=False
)
```

**Tarefa:**

- **Input**: JSON da tarefa anterior
- **Output**: Análise com pontuação e pontos fortes/fracos
- **Limite**: 200 palavras

#### 3. **Agente Conselheiro**

```python
agente_conselheiro = Agent(
    role="Conselheiro de Carreira",
    goal="Transformar análises técnicas em feedback construtivo e acionável",
    backstory="""Coach de carreira certificado. Especialista em 
    desenvolvimento profissional e comunicação empática.""",
    llm=llm_economico,
    verbose=False
)
```

**Tarefa:**

- **Input**: Análise da tarefa anterior
- **Output**: Feedback amigável com sugestões práticas
- **Limite**: 250 palavras

### 📊 Base de Dados para Implementação

```python
CRITERIOS_AVALIACAO = {
    "experiencia": {
        "peso": 30,
        "descricao": "Tempo e relevância da experiência profissional",
        "pontuacao": {
            "0-1 anos": 2,
            "2-4 anos": 4,
            "5-9 anos": 7,
            "10+ anos": 10
        }
    },
    "educacao": {
        "peso": 25,
        "descricao": "Formação acadêmica e certificações",
        "pontuacao": {
            "ensino_medio": 3,
            "tecnico": 5,
            "superior": 8,
            "pos_graduacao": 10
        }
    },
    "habilidades": {
        "peso": 25,
        "descricao": "Skills técnicas e comportamentais",
        "pontuacao": {
            "basicas": 3,
            "intermediarias": 6,
            "avancadas": 9,
            "expert": 10
        }
    },
    "apresentacao": {
        "peso": 20,
        "descricao": "Clareza, organização e formatação",
        "pontuacao": {
            "ruim": 2,
            "regular": 5,
            "boa": 8,
            "excelente": 10
        }
    }
}

TEMPLATES_FEEDBACK = {
    "pontos_fortes": [
        "Experiência sólida em [área]",
        "Formação acadêmica consistente",
        "Boa apresentação de habilidades",
        "Histórico profissional coerente"
    ],
    "areas_melhoria": [
        "Incluir mais detalhes sobre conquistas",
        "Adicionar certificações relevantes",
        "Melhorar formatação e organização",
        "Quantificar resultados alcançados"
    ],
    "sugestoes_praticas": [
        "Use métricas para demonstrar impacto",
        "Inclua palavras-chave da área",
        "Mantenha currículo atualizado",
        "Adapte currículo para cada vaga"
    ]
}
```

### 💻 Implementação Base

```python
def criar_tarefas_curriculo(agentes, curriculo_texto):
    agente_extrator, agente_avaliador, agente_conselheiro = agentes
    
    tarefa_extracao = Task(
        description=f"""
        Extraia informações estruturadas deste currículo: {curriculo_texto}
        
        FORMATO JSON OBRIGATÓRIO:
        {{
            "nome": "nome_candidato",
            "experiencia_anos": numero_anos,
            "educacao_nivel": "nivel_educacional",
            "habilidades": ["skill1", "skill2", "skill3"],
            "cargo_atual": "posicao_atual",
            "area_atuacao": "area_principal"
        }}
        
        Seja preciso e objetivo. LIMITE: 150 palavras.
        """,
        agent=agente_extrator,
        expected_output="JSON estruturado com dados extraídos do currículo"
    )
    
    tarefa_avaliacao = Task(
        description=f"""
        Avalie o currículo baseado nos dados extraídos usando estes critérios:
        {CRITERIOS_AVALIACAO}
        
        Forneça:
        1. Pontuação geral (0-100)
        2. Pontuação por critério
        3. Principais pontos fortes (máximo 3)
        4. Principais áreas de melhoria (máximo 3)
        
        Seja objetivo e baseie-se nos critérios fornecidos. LIMITE: 200 palavras.
        """,
        agent=agente_avaliador,
        expected_output="Avaliação estruturada com pontuação e análise detalhada",
        context=[tarefa_extracao]
    )
    
    tarefa_feedback = Task(
        description="""
        Transforme a avaliação técnica em feedback construtivo e encorajador.
        
        Estrutura da resposta:
        1. Cumprimento personalizado
        2. Reconhecimento dos pontos fortes
        3. Sugestões específicas de melhoria
        4. Próximos passos recomendados
        5. Mensagem final motivacional
        
        Use tom profissional mas caloroso. LIMITE: 250 palavras.
        """,
        agent=agente_conselheiro,
        expected_output="Feedback final amigável e útil para o candidato",
        context=[tarefa_avaliacao]
    )
    
    return [tarefa_extracao, tarefa_avaliacao, tarefa_feedback]
```

### ✅ Critérios de Sucesso

- [ ] **Funcionalidade**: Sistema processa currículos sem erros
- [ ] **Estrutura**: 3 agentes especializados comunicando em sequência
- [ ] **Qualidade**: Feedback útil e construtivo
- [ ] **Economia**: Custo < $0.01 por análise
- [ ] **Validação**: Entrada validada adequadamente

---

## 🚀 Exercício 2: Sistema de Planejamento de Viagem (MÉDIO)

### 🎯 Objetivo

Criar uma cadeia de 4 agentes para planejamento completo de viagens personalizadas.

### 🔗 Fluxo da Cadeia

```
Preferências → Analisador → Pesquisador → Organizador → Orçamentista → Itinerário Final
```

### 👥 Agentes Detalhados

#### 1. **Agente Analisador de Preferências**

```python
agente_analisador = Agent(
    role="Analisador de Preferências de Viagem",
    goal="Compreender perfil detalhado e preferências do viajante",
    backstory="""Consultor de viagens com 15 anos de experiência. 
    Expert em interpretar necessidades e criar perfis de viajantes.""",
    llm=llm_economico,
    verbose=False
)
```

**Responsabilidades:**

- Analisar preferências informadas
- Identificar tipo de viajante
- Extrair restrições e requisitos
- Definir prioridades

#### 2. **Agente Pesquisador de Destinos**

```python
agente_pesquisador = Agent(
    role="Pesquisador de Destinos e Atrações",
    goal="Buscar e recomendar destinos ideais baseado no perfil",
    backstory="""Especialista em destinos turísticos globais. 
    Conhece tendências e melhores opções para cada perfil.""",
    llm=llm_economico,
    verbose=False
)
```

**Responsabilidades:**

- Sugerir destinos compatíveis
- Listar atrações principais
- Considerar época/clima
- Avaliar acessibilidade

#### 3. **Agente Organizador de Roteiro**

```python
agente_organizador = Agent(
    role="Organizador de Itinerário",
    goal="Estruturar cronograma otimizado e lógico da viagem",
    backstory="""Planejador de roteiros com expertise em logística. 
    Otimiza tempo e experiências em viagens.""",
    llm=llm_economico,
    verbose=False
)
```

**Responsabilidades:**

- Criar cronograma dia a dia
- Otimizar deslocamentos
- Balancear atividades
- Incluir tempo livre

#### 4. **Agente Especialista em Orçamento**

```python
agente_orcamentista = Agent(
    role="Consultor Financeiro de Viagens",
    goal="Calcular custos realistas e sugerir alternativas econômicas",
    backstory="""Consultor financeiro especializado em turismo. 
    Expert em orçamentos e opções de economia.""",
    llm=llm_economico,
    verbose=False
)
```

**Responsabilidades:**

- Calcular custos totais
- Sugerir alternativas econômicas
- Detalhar gastos por categoria
- Propor formas de pagamento

### 📊 Base de Dados Expandida

```python
DESTINOS_DETALHADOS = {
    "praia": {
        "nacionais": {
            "florianopolis": {
                "custo_dia": 180,
                "epoca_ideal": "dez-mar",
                "atrações": ["Lagoa da Conceição", "Joaquina", "Centro Histórico"],
                "tipo_viajante": ["casal", "familia", "amigos"]
            },
            "porto_galinhas": {
                "custo_dia": 200,
                "epoca_ideal": "set-mar",
                "atrações": ["Piscinas Naturais", "Praia do Pontal", "Buggy"],
                "tipo_viajante": ["casal", "familia"]
            }
        },
        "internacionais": {
            "cancun": {
                "custo_dia": 350,
                "epoca_ideal": "nov-abr",
                "atrações": ["Chichen Itza", "Xcaret", "Zona Hoteleira"],
                "tipo_viajante": ["casal", "amigos", "lua_mel"]
            }
        }
    },
    "aventura": {
        "nacionais": {
            "chapada_diamantina": {
                "custo_dia": 120,
                "epoca_ideal": "mai-set",
                "atrações": ["Poco Encantado", "Vale do Pati", "Cachoeira da Fumaça"],
                "tipo_viajante": ["aventureiro", "amigos"]
            }
        }
    }
}

CATEGORIAS_ORCAMENTO = {
    "hospedagem": {"economica": 0.3, "padrão": 0.4, "luxo": 0.6},
    "alimentacao": {"economica": 0.2, "padrão": 0.25, "luxo": 0.3},
    "transporte": {"economica": 0.15, "padrão": 0.2, "luxo": 0.25},
    "atividades": {"economica": 0.25, "padrão": 0.15, "luxo": 0.1},
    "extras": {"economica": 0.1, "padrão": 0.1, "luxo": 0.15}
}

PERFIS_VIAJANTE = {
    "aventureiro": {
        "prioridades": ["atividades", "experiencias"],
        "orcamento_sugerido": "economica",
        "destinos_preferidos": ["montanha", "aventura", "ecoturismo"]
    },
    "relaxamento": {
        "prioridades": ["conforto", "tranquilidade"],
        "orcamento_sugerido": "padrão",
        "destinos_preferidos": ["praia", "spa", "resort"]
    },
    "cultural": {
        "prioridades": ["historia", "museus", "gastronomia"],
        "orcamento_sugerido": "padrão",
        "destinos_preferidos": ["cidades historicas", "capitais"]
    }
}
```

### 💻 Implementação com Validação

```python
def validar_preferencias_viagem(preferencias):
    """Valida entrada específica para planejamento de viagem"""
    campos_obrigatorios = ["destino_tipo", "orcamento", "duracao", "pessoas"]
    
    for campo in campos_obrigatorios:
        if campo not in preferencias:
            raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    # Validações específicas
    if preferencias["orcamento"] <= 0:
        raise ValueError("Orçamento deve ser positivo")
    
    if not 1 <= preferencias["duracao"] <= 30:
        raise ValueError("Duração deve ser entre 1 e 30 dias")
    
    if not 1 <= preferencias["pessoas"] <= 10:
        raise ValueError("Número de pessoas deve ser entre 1 e 10")
    
    return True

def criar_tarefas_viagem(agentes, preferencias_usuario):
    agente_analisador, agente_pesquisador, agente_organizador, agente_orcamentista = agentes
    
    tarefa_analise = Task(
        description=f"""
        Analise estas preferências de viagem: {preferencias_usuario}
        
        Identifique:
        1. Perfil do viajante (aventureiro/relaxamento/cultural)
        2. Prioridades principais
        3. Restrições ou requisitos especiais
        4. Tipo de experiência desejada
        
        FORMATO JSON:
        {{
            "perfil_viajante": "tipo_identificado",
            "prioridades": ["prioridade1", "prioridade2"],
            "restricoes": ["restricao1", "restricao2"],
            "experiencia_desejada": "descricao"
        }}
        
        LIMITE: 150 palavras.
        """,
        agent=agente_analisador,
        expected_output="Análise estruturada do perfil do viajante"
    )
    
    tarefa_pesquisa = Task(
        description=f"""
        Com base no perfil identificado, pesquise e recomende:
        
        Base de destinos disponível: {DESTINOS_DETALHADOS}
        
        Forneça:
        1. 3 destinos principais recomendados
        2. Principais atrações de cada destino
        3. Época ideal para visita
        4. Por que cada destino combina com o perfil
        
        Considere orçamento e preferências identificadas. LIMITE: 200 palavras.
        """,
        agent=agente_pesquisador,
        expected_output="Lista de destinos recomendados com justificativas",
        context=[tarefa_analise]
    )
    
    tarefa_organizacao = Task(
        description="""
        Crie um roteiro detalhado baseado nos destinos recomendados.
        
        Estruture:
        1. Cronograma dia a dia
        2. Atividades em cada dia
        3. Tempos de deslocamento
        4. Dicas de logística
        
        Otimize tempo e experiências. LIMITE: 250 palavras.
        """,
        agent=agente_organizador,
        expected_output="Itinerário detalhado dia a dia",
        context=[tarefa_pesquisa]
    )
    
    tarefa_orcamento = Task(
        description=f"""
        Calcule o orçamento detalhado para o roteiro proposto.
        
        Use estas categorias: {CATEGORIAS_ORCAMENTO}
        
        Forneça:
        1. Custo total estimado
        2. Breakdown por categoria
        3. Opções de economia
        4. Alternativas de pagamento
        
        Seja realista e detalhado. LIMITE: 200 palavras.
        """,
        agent=agente_orcamentista,
        expected_output="Orçamento detalhado com alternativas",
        context=[tarefa_organizacao]
    )
    
    return [tarefa_analise, tarefa_pesquisa, tarefa_organizacao, tarefa_orcamento]
```

### ✅ Critérios de Sucesso

- [ ] **4 agentes especializados** funcionando em sequência
- [ ] **Validação robusta** de preferências de entrada
- [ ] **Base de dados** realista utilizada
- [ ] **Cálculo de orçamento** funcional e preciso
- [ ] **Itinerário detalhado** com cronograma dia a dia

---

## 🚀 Exercício 3: Sistema de Criação de Conteúdo (AVANÇADO)

### 🎯 Objetivo

Criar uma cadeia de 5 agentes para produção completa de conteúdo para redes sociais.

### 🔗 Fluxo da Cadeia

```
Briefing → Analisador → Pesquisador → Estrategista → Criativo → Revisor → Conteúdo Final
```

### 🛡️ Implementação com Segurança Avançada

```python
import hashlib
from openai import OpenAI

class ContentSecurityManager:
    def __init__(self):
        self.client = OpenAI()
        self.safety_identifiers = {}
        
    def gerar_safety_id(self, usuario_email):
        """Gera identificador de segurança para rastreabilidade"""
        return hashlib.sha256(usuario_email.encode()).hexdigest()[:16]
    
    def verificar_moderacao(self, texto):
        """Verifica conteúdo usando API de Moderação OpenAI"""
        try:
            response = self.client.moderations.create(input=texto)
            resultado = response.results[0]
            
            if resultado.flagged:
                categorias = [cat for cat, flag in resultado.categories.model_dump().items() if flag]
                raise ValueError(f"Conteúdo flagged nas categorias: {categorias}")
            
            return True
            
        except Exception as e:
            print(f"Erro na moderação: {e}")
            return False  # Conservador em caso de erro
    
    def validar_briefing_completo(self, briefing, usuario_email):
        """Validação completa do briefing com segurança"""
        # 1. Validação básica
        if len(briefing) > 4000:
            raise ValueError("Briefing muito longo. Máximo 4000 caracteres.")
        
        # 2. Verificação de moderação
        if not self.verificar_moderacao(briefing):
            raise ValueError("Briefing contém conteúdo inadequado.")
        
        # 3. Registrar safety identifier
        safety_id = self.gerar_safety_id(usuario_email)
        self.safety_identifiers[safety_id] = {
            "usuario": usuario_email,
            "timestamp": time.time(),
            "briefing_hash": hashlib.md5(briefing.encode()).hexdigest()
        }
        
        return safety_id

class CacheAvancado:
    """Cache inteligente para conteúdo com TTL específico"""
    def __init__(self):
        self.cache_briefing = {}     # TTL curto - 30 min
        self.cache_trends = {}       # TTL médio - 2 horas
        self.cache_templates = {}    # TTL longo - 24 horas
        
    def buscar_briefing(self, briefing, plataforma):
        """Busca análise de briefing no cache"""
        chave = hashlib.md5(f"{briefing}|{plataforma}".encode()).hexdigest()
        
        if chave in self.cache_briefing:
            timestamp, resultado = self.cache_briefing[chave]
            if time.time() - timestamp < 1800:  # 30 minutos
                print("✅ Cache HIT - Briefing (economia: $0.003)")
                return resultado
            else:
                del self.cache_briefing[chave]
        
        return None
    
    def salvar_briefing(self, briefing, plataforma, resultado):
        """Salva análise de briefing no cache"""
        chave = hashlib.md5(f"{briefing}|{plataforma}".encode()).hexdigest()
        self.cache_briefing[chave] = (time.time(), resultado)
```

### 👥 Agentes Especializados Avançados

#### 1. **Agente Analisador de Briefing**

```python
agente_analisador = Agent(
    role="Analisador Estratégico de Briefing",
    goal="Extrair insights profundos e objetivos estratégicos do briefing",
    backstory="""Estrategista de marketing digital com 12 anos de experiência. 
    Expert em interpretar objetivos de negócio e traduzir em estratégias de conteúdo.""",
    llm=llm_economico,
    verbose=False
)
```

#### 2. **Agente Pesquisador de Trends**

```python
agente_pesquisador = Agent(
    role="Pesquisador de Tendências Digitais",
    goal="Identificar trends relevantes e oportunidades de momento",
    backstory="""Analista de trends com expertise em comportamento digital. 
    Monitora constantemente tendências de plataformas sociais.""",
    llm=llm_economico,
    verbose=False
)
```

### 📊 Base de Dados Avançada

```python
PLATAFORMAS_DETALHADAS = {
    "instagram": {
        "limite_caracteres": 2200,
        "hashtags_otimas": 5,
        "melhores_horarios": ["18h-21h", "12h-14h"],
        "formatos": {
            "carrossel": {"max_slides": 10, "engajamento": "alto"},
            "story": {"max_segundos": 15, "engajamento": "médio"},
            "reel": {"max_segundos": 60, "engajamento": "muito_alto"},
            "post_unico": {"max_imagens": 1, "engajamento": "médio"}
        },
        "publico_alvo": ["18-34", "visual", "lifestyle"],
        "tom_ideal": "casual_profissional"
    },
    "linkedin": {
        "limite_caracteres": 3000,
        "hashtags_otimas": 3,
        "melhores_horarios": ["8h-10h", "17h-19h"],
        "formatos": {
            "artigo": {"max_caracteres": 125000, "engajamento": "alto"},
            "post_profissional": {"max_caracteres": 3000, "engajamento": "médio"},
            "poll": {"max_opcoes": 4, "engajamento": "muito_alto"}
        },
        "publico_alvo": ["25-54", "profissional", "B2B"],
        "tom_ideal": "profissional_autoridade"
    },
    "tiktok": {
        "limite_caracteres": 2200,
        "hashtags_otimas": 3,
        "melhores_horarios": ["19h-22h", "6h-10h"],
        "formatos": {
            "video_curto": {"max_segundos": 60, "engajamento": "muito_alto"},
            "dueto": {"max_segundos": 60, "engajamento": "alto"},
            "trend": {"max_segundos": 15, "engajamento": "muito_alto"}
        },
        "publico_alvo": ["16-24", "entretenimento", "trends"],
        "tom_ideal": "descontraido_autêntico"
    }
}

TRENDS_ATUAIS = {
    "tecnologia": {
        "keywords": ["IA", "automação", "futuro do trabalho", "inovação"],
        "hashtags": ["#IA", "#Tech", "#Inovação", "#FuturoDoTrabalho"],
        "abordagens": ["como a IA impacta", "tendências tech 2024", "ferramentas que facilitam"]
    },
    "lifestyle": {
        "keywords": ["bem-estar", "produtividade", "mindfulness", "equilíbrio"],
        "hashtags": ["#BemEstar", "#Mindfulness", "#Produtividade", "#LifestyleTips"],
        "abordagens": ["dicas de bem-estar", "rotina produtiva", "autocuidado"]
    },
    "negocios": {
        "keywords": ["empreendedorismo", "liderança", "vendas", "networking"],
        "hashtags": ["#Empreendedorismo", "#Liderança", "#Vendas", "#BusinessTips"],
        "abordagens": ["estratégias de negócio", "lições aprendidas", "cases de sucesso"]
    }
}

TEMPLATES_CONTEUDO = {
    "educativo": {
        "estrutura": "Como [ação]: [benefício] em [tempo]",
        "exemplos": ["Como automatizar: 50% do seu trabalho em 1 mês"],
        "call_to_action": "Salve este post para aplicar depois!"
    },
    "inspiracional": {
        "estrutura": "A história de [pessoa] que [conquista] e [aprendizado]",
        "exemplos": ["A história de Sara que triplicou as vendas e o que aprendeu"],
        "call_to_action": "Compartilhe sua própria experiência nos comentários!"
    },
    "dica_rapida": {
        "estrutura": "[Número] maneiras de [objetivo] em [tempo/contexto]",
        "exemplos": ["5 maneiras de melhorar produtividade trabalhando de casa"],
        "call_to_action": "Qual dica você vai testar primeiro?"
    }
}
```

### ✅ Critérios de Sucesso Avançados

- [ ] **5 agentes especializados** trabalhando em cadeia
- [ ] **API de moderação** integrada e funcionando
- [ ] **Cache multicamada** implementado
- [ ] **Safety identifiers** para rastreabilidade
- [ ] **Validação de conteúdo** em múltiplas camadas
- [ ] **Geração otimizada** para plataforma específica

---

## 🚀 Exercício 4: Sistema de Suporte Técnico (EXPERT)

### 🎯 Objetivo

Criar um sistema completo de diagnóstico e resolução automatizada de problemas técnicos.

### 🔗 Fluxo da Cadeia

```
Problema → Triagem → Diagnosticador → Solucionador → Validador → Comunicador → Instruções Finais
```

### 🏗️ Arquitetura Avançada com IA de Decisão

```python
class SistemaDiagnostico:
    """Sistema inteligente de diagnóstico com árvore de decisão"""
    
    def __init__(self):
        self.base_conhecimento = self.carregar_base_conhecimento()
        self.historico_casos = []
        
    def classificar_problema(self, descricao):
        """Classifica problema usando IA e base de conhecimento"""
        # Implementa classificação inteligente
        # Retorna categoria, severidade, urgência
        pass
    
    def buscar_solucoes_similares(self, problema_classificado):
        """Busca casos similares no histórico"""
        # Implementa busca semântica
        # Retorna soluções que funcionaram antes
        pass
    
    def validar_solucao(self, problema, solucao_proposta):
        """Valida se solução é apropriada para o problema"""
        # Implementa validação lógica
        # Verifica compatibilidade e riscos
        pass
```

### 📊 Base de Conhecimento Técnico

```python
BASE_CONHECIMENTO_TECNICO = {
    "hardware": {
        "problemas_comuns": {
            "tela_preta": {
                "sintomas": ["monitor não liga", "tela escura", "sem imagem"],
                "causas_possiveis": ["cabo desconectado", "monitor defeituoso", "placa de vídeo"],
                "solucoes_ordenadas": [
                    {"acao": "verificar_cabos", "sucesso_rate": 60, "dificuldade": "fácil"},
                    {"acao": "testar_outro_monitor", "sucesso_rate": 30, "dificuldade": "médio"},
                    {"acao": "verificar_placa_video", "sucesso_rate": 10, "dificuldade": "difícil"}
                ]
            },
            "computador_lento": {
                "sintomas": ["lentidão geral", "demora para iniciar", "travamentos"],
                "causas_possiveis": ["pouco espaço HD", "muitos programas iniciando", "vírus"],
                "solucoes_ordenadas": [
                    {"acao": "limpar_disco", "sucesso_rate": 40, "dificuldade": "fácil"},
                    {"acao": "desabilitar_programas_inicio", "sucesso_rate": 35, "dificuldade": "médio"},
                    {"acao": "scan_antivirus", "sucesso_rate": 25, "dificuldade": "médio"}
                ]
            }
        }
    },
    "software": {
        "problemas_comuns": {
            "aplicativo_nao_abre": {
                "sintomas": ["erro ao iniciar", "aplicativo trava", "mensagem de erro"],
                "causas_possiveis": ["arquivo corrompido", "falta de permissão", "dependência faltando"],
                "solucoes_ordenadas": [
                    {"acao": "executar_como_admin", "sucesso_rate": 45, "dificuldade": "fácil"},
                    {"acao": "reinstalar_aplicativo", "sucesso_rate": 40, "dificuldade": "médio"},
                    {"acao": "verificar_dependencias", "sucesso_rate": 15, "dificuldade": "difícil"}
                ]
            }
        }
    },
    "rede": {
        "problemas_comuns": {
            "sem_internet": {
                "sintomas": ["não conecta", "internet lenta", "páginas não carregam"],
                "causas_possiveis": ["problema ISP", "roteador", "configuração"],
                "solucoes_ordenadas": [
                    {"acao": "reiniciar_roteador", "sucesso_rate": 50, "dificuldade": "fácil"},
                    {"acao": "verificar_cabos", "sucesso_rate": 30, "dificuldade": "fácil"},
                    {"acao": "contatar_provedor", "sucesso_rate": 20, "dificuldade": "médio"}
                ]
            }
        }
    }
}

SCRIPTS_SOLUCAO = {
    "limpar_disco": {
        "windows": [
            "1. Abrir 'Este Computador'",
            "2. Clicar com botão direito no disco C:",
            "3. Selecionar 'Propriedades'",
            "4. Clicar em 'Limpeza de Disco'",
            "5. Marcar todas as opções e clicar 'OK'"
        ],
        "tempo_estimado": "10-15 minutos"
    },
    "reiniciar_roteador": {
        "universal": [
            "1. Desligar o roteador da tomada",
            "2. Aguardar 30 segundos",
            "3. Religar o roteador",
            "4. Aguardar 2-3 minutos para reconectar",
            "5. Testar a conexão"
        ],
        "tempo_estimado": "5 minutos"
    }
}
```

### 👥 Agentes Especializados Expert

#### 1. **Agente de Triagem Inteligente**

```python
agente_triagem = Agent(
    role="Especialista em Triagem de Problemas Técnicos",
    goal="Classificar problemas com precisão máxima para direcionamento correto",
    backstory="""Técnico sênior com 15 anos de experiência em suporte. 
    Expert em identificar rapidamente categoria, severidade e urgência de problemas técnicos.""",
    tools=[
        CategorizadorProblemasTool(),
        CalculadorSeveridadeTool(),
        ValidadorUrgenciaTool()
    ],
    llm=llm_economico,
    verbose=False
)
```

#### 2. **Agente Diagnosticador Avançado**

```python
agente_diagnosticador = Agent(
    role="Diagnosticador de Sistemas",
    goal="Identificar causa raiz usando análise sistemática e base de conhecimento",
    backstory="""Especialista em diagnóstico com formação em engenharia de sistemas. 
    Usa metodologia estruturada para identificar causas raiz rapidamente.""",
    tools=[
        BaseConchecimentoTool(),
        AnalisadorSintemasTool(),
        BuscadorCasosSimilaresTool()
    ],
    llm=llm_economico,
    verbose=False
)
```

### 💻 Implementação Expert com Monitoramento

```python
class SupportSystemMonitor:
    """Monitor completo do sistema de suporte"""
    
    def __init__(self):
        self.metricas = {
            "casos_resolvidos": 0,
            "tempo_medio_resolucao": 0,
            "taxa_sucesso": 0,
            "satisfacao_cliente": 0
        }
        self.casos_ativos = {}
        
    def iniciar_caso(self, caso_id, problema):
        """Inicia monitoramento de um caso"""
        self.casos_ativos[caso_id] = {
            "inicio": time.time(),
            "problema": problema,
            "etapa_atual": "triagem",
            "tentativas_solucao": 0
        }
    
    def atualizar_etapa(self, caso_id, nova_etapa):
        """Atualiza etapa atual do caso"""
        if caso_id in self.casos_ativos:
            self.casos_ativos[caso_id]["etapa_atual"] = nova_etapa
    
    def finalizar_caso(self, caso_id, resolvido=True, satisfacao=None):
        """Finaliza caso e registra métricas"""
        if caso_id in self.casos_ativos:
            caso = self.casos_ativos[caso_id]
            tempo_total = time.time() - caso["inicio"]
            
            # Atualizar métricas
            if resolvido:
                self.metricas["casos_resolvidos"] += 1
            
            # Calcular tempo médio
            self.metricas["tempo_medio_resolucao"] = (
                (self.metricas["tempo_medio_resolucao"] + tempo_total) / 2
            )
            
            del self.casos_ativos[caso_id]

def criar_sistema_suporte_completo():
    """Cria sistema completo de suporte técnico"""
    
    # Inicializar componentes
    security_manager = ContentSecurityManager()
    monitor = MonitorCustos(orcamento=5.0)
    system_monitor = SupportSystemMonitor()
    
    # Agentes especializados
    agentes = [
        criar_agente_triagem(),
        criar_agente_diagnosticador(), 
        criar_agente_solucionador(),
        criar_agente_validador(),
        criar_agente_comunicador()
    ]
    
    return {
        "agentes": agentes,
        "security": security_manager,
        "monitor_custos": monitor,
        "monitor_sistema": system_monitor,
        "base_conhecimento": BASE_CONHECIMENTO_TECNICO
    }
```

### ✅ Critérios de Sucesso Expert

- [ ] **Sistema completo** com 5+ agentes especializados
- [ ] **Base de conhecimento** rica e estruturada
- [ ] **Monitoramento em tempo real** de casos e métricas
- [ ] **Escalabilidade** para novos tipos de problema
- [ ] **Todas as práticas** de segurança e economia implementadas
- [ ] **Taxa de resolução** > 80% em problemas comuns
- [ ] **Tempo médio** < 10 minutos para diagnóstico

---

## 🛠️ Recursos de Desenvolvimento

### 📁 Estrutura de Projeto Recomendada

```
seu_exercicio/
├── main.py                 # Arquivo principal
├── config/
│   ├── __init__.py
│   ├── llm_config.py      # Configuração do LLM
│   └── security_config.py  # Configurações de segurança
├── agents/
│   ├── __init__.py
│   ├── agent_definitions.py
│   └── specialized_agents.py
├── tasks/
│   ├── __init__.py
│   └── task_chains.py
├── utils/
│   ├── __init__.py
│   ├── validators.py       # Validações
│   ├── cache.py           # Sistema de cache
│   ├── cost_monitor.py    # Monitor de custos
│   └── security.py        # Funções de segurança
├── data/
│   ├── __init__.py
│   ├── knowledge_base.py  # Base de dados simulada
│   └── test_data.py       # Dados para teste
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_tasks.py
│   └── test_integration.py
└── README.md              # Documentação completa
```

### 🧪 Template de Testes

```python
# tests/test_integration.py
import unittest
from utils.cost_monitor import MonitorCustos
from utils.validators import validar_entrada

class TestIntegracao(unittest.TestCase):
    
    def setUp(self):
        self.monitor = MonitorCustos(orcamento=0.50)
        
    def test_caso_basico(self):
        """Testa caso básico de funcionamento"""
        entrada = "Teste básico de entrada"
        
        # Validar entrada
        self.assertTrue(validar_entrada(entrada))
        
        # Verificar custo
        custo = self.monitor.estimar_custo(entrada)
        self.assertLess(custo, 0.01)  # Menos de $0.01
        
    def test_entrada_invalida(self):
        """Testa validação de entrada inválida"""
        with self.assertRaises(ValueError):
            validar_entrada("")  # Entrada vazia
            
        with self.assertRaises(ValueError):
            validar_entrada("x" * 5000)  # Muito longa
    
    def test_orcamento_excedido(self):
        """Testa comportamento quando orçamento é excedido"""
        self.monitor.gasto_atual = 0.45  # Quase no limite
        
        with self.assertRaises(Exception):
            self.monitor.verificar_orcamento(0.10)  # Excederia limite

if __name__ == '__main__':
    unittest.main()
```

### 📊 Template de Relatório de Custos

```python
# utils/cost_reporter.py
class CostReporter:
    """Gerador de relatórios de custo detalhados"""
    
    def __init__(self, monitor):
        self.monitor = monitor
        
    def gerar_relatorio_completo(self, execucoes_realizadas):
        """Gera relatório completo de custos"""
        
        relatorio = {
            "resumo": {
                "total_gasto": self.monitor.gasto_atual,
                "orcamento_inicial": self.monitor.orcamento,
                "percentual_usado": (self.monitor.gasto_atual / self.monitor.orcamento) * 100,
                "execucoes_realizadas": execucoes_realizadas
            },
            "metricas": {
                "custo_por_execucao": self.monitor.gasto_atual / max(execucoes_realizadas, 1),
                "economia_vs_gpt4o": self.calcular_economia_gpt4o(),
                "projecao_100_execucoes": (self.monitor.gasto_atual / max(execucoes_realizadas, 1)) * 100
            },
            "otimizacoes": {
                "modelo_usado": "gpt-4o-mini",
                "cache_implementado": True,
                "limites_output": True,
                "validacao_entrada": True
            }
        }
        
        return relatorio
    
    def calcular_economia_gpt4o(self):
        """Calcula economia comparado ao GPT-4o"""
        # GPT-4o custa ~16x mais que GPT-4o Mini
        custo_gpt4o = self.monitor.gasto_atual * 16
        economia = ((custo_gpt4o - self.monitor.gasto_atual) / custo_gpt4o) * 100
        return round(economia, 1)
```

---

## 🎯 Cronograma Sugerido de Implementação

### 📅 Semana 1 - Exercício 1 (Análise de Currículo)

- **Dia 1-2**: Setup básico e agente extrator
- **Dia 3**: Agente avaliador e base de dados
- **Dia 4**: Agente conselheiro e integração
- **Dia 5**: Testes, validação e documentação

### 📅 Semana 2 - Exercício 2 (Planejamento de Viagem)

- **Dia 1-2**: 4 agentes e base de dados expandida
- **Dia 3**: Sistema de validação robusto
- **Dia 4**: Cálculos de orçamento e otimizações
- **Dia 5**: Testes completos e casos extremos

### 📅 Semana 3 - Exercício 3 (Criação de Conteúdo)

- **Dia 1-2**: 5 agentes e API de moderação
- **Dia 3**: Sistema de cache multicamada
- **Dia 4**: Safety identifiers e segurança avançada
- **Dia 5**: Testes de segurança e performance

### 📅 Semana 4 - Exercício 4 (Suporte Técnico)

- **Dia 1-3**: Sistema completo com base de conhecimento
- **Dia 4**: Monitoramento e métricas em tempo real
- **Dia 5**: Documentação e apresentação final

---

## 🏆 Avaliação e Entrega

### 📤 Checklist de Entrega

Para cada exercício, entregar:

- [ ] **Código fonte** completo e documentado
- [ ] **README.md** com instruções claras
- [ ] **Testes automatizados** funcionando
- [ ] **Relatório de custos** detalhado
- [ ] **Screenshots** de execuções bem-sucedidas
- [ ] **Vídeo demonstração** (2-3 minutos)

### 🎯 Critérios de Avaliação

#### ⭐ Funcionalidade (30%)

- Sistema funciona sem erros
- Agentes comunicam corretamente
- Output é útil e relevante

#### ⭐ Qualidade Técnica (25%)

- Código bem estruturado
- Boas práticas implementadas
- Testes adequados

#### ⭐ Economia e Otimização (25%)

- Uso eficiente de recursos
- Cache implementado quando aplicável
- Monitoramento de custos ativo

#### ⭐ Segurança (20%)

- Validação de entrada robusta
- Moderação quando necessária
- Tratamento de erros adequado

### 🚀 Próximos Passos

Após completar os exercícios:

1. **Experimentar variações** - Tente diferentes números de agentes
2. **Adicionar ferramentas** - Integre APIs externas
3. **Melhorar performance** - Otimize ainda mais os custos
4. **Construir interfaces** - Crie UIs web com Streamlit
5. **Explorar casos reais** - Adapte para problemas do mundo real

---

**🎯 Sucesso em seus exercícios! Lembre-se: a especialização de agentes é a chave para sistemas CrewAI eficientes e escaláveis!**

*Para suporte adicional, consulte os arquivos de referência em `docs/` ou execute os exemplos em `aula4/`.*
