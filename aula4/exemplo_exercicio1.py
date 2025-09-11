"""
Exemplo Prático: Sistema de Análise de Currículo - Exercício 1
Demonstração simplificada da cadeia de agentes especializados

Este exemplo mostra como implementar o Exercício 1 com todas as boas práticas
de segurança e economia de custos aprendidas na aula 4.
"""

import os
import time
import hashlib
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Verificar se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  ATENÇÃO: Configure a variável OPENAI_API_KEY")
    print("No Windows PowerShell: $env:OPENAI_API_KEY='sua_chave_aqui'")
    exit(1)

# =============================================================================
# CONFIGURAÇÃO DE SEGURANÇA E ECONOMIA
# =============================================================================


class MonitorCustos:
    """Monitor de custos otimizado para GPT-4o Mini"""

    def __init__(self, orcamento=2.0):
        self.orcamento = orcamento
        self.gasto_atual = 0.0
        # Preços atualizados GPT-4o Mini (input/output por 1M tokens)
        self.precos = {"input": 0.15 / 1000000, "output": 0.60 / 1000000}

    def estimar_custo(self, texto_entrada, tokens_saida_esperados=600):
        """Estima custo da operação"""
        tokens_input = len(texto_entrada) * 0.25  # Aproximação
        custo = (
            tokens_input * self.precos["input"]
            + tokens_saida_esperados * self.precos["output"]
        )
        return custo

    def verificar_orcamento(self, custo_estimado):
        """Verifica se operação cabe no orçamento"""
        if self.gasto_atual + custo_estimado > self.orcamento:
            raise Exception(
                f"❌ Custo excederia orçamento! Atual: ${self.gasto_atual:.4f}"
            )
        return True

    def registrar_gasto(self, custo):
        """Registra gasto realizado"""
        self.gasto_atual += custo
        print(f"💰 Custo desta operação: ${custo:.6f}")
        print(f"💸 Total gasto: ${self.gasto_atual:.4f}")
        print(f"💳 Restante: ${self.orcamento - self.gasto_atual:.4f}")

        if self.gasto_atual > self.orcamento * 0.8:
            print(f"⚠️ ATENÇÃO: 80% do orçamento usado!")


class CacheInteligente:
    """Cache para economizar em queries similares"""

    def __init__(self, ttl=1800):  # 30 minutos
        self.cache = {}
        self.ttl = ttl

    def gerar_chave(self, curriculo):
        """Gera chave única para o currículo"""
        return hashlib.md5(curriculo.encode()).hexdigest()

    def buscar(self, curriculo):
        """Busca análise no cache"""
        chave = self.gerar_chave(curriculo)
        if chave in self.cache:
            timestamp, resultado = self.cache[chave]
            if time.time() - timestamp < self.ttl:
                print("✅ Cache HIT - Economia de ~$0.002!")
                return resultado
            else:
                del self.cache[chave]
        return None

    def salvar(self, curriculo, resultado):
        """Salva resultado no cache"""
        chave = self.gerar_chave(curriculo)
        self.cache[chave] = (time.time(), resultado)


def validar_entrada(curriculo):
    """Valida entrada do usuário"""
    if not curriculo or not isinstance(curriculo, str):
        raise ValueError("Currículo deve ser um texto válido")

    if len(curriculo) < 50:
        raise ValueError("Currículo muito curto. Mínimo 50 caracteres.")

    if len(curriculo) > 3000:
        raise ValueError("Currículo muito longo. Máximo 3000 caracteres.")

    return True


# =============================================================================
# BASE DE DADOS E CONFIGURAÇÕES
# =============================================================================

CRITERIOS_AVALIACAO = {
    "experiencia": {"peso": 30, "descricao": "Anos e relevância da experiência"},
    "educacao": {"peso": 25, "descricao": "Formação acadêmica e certificações"},
    "habilidades": {"peso": 25, "descricao": "Skills técnicas e comportamentais"},
    "apresentacao": {"peso": 20, "descricao": "Clareza e organização do currículo"},
}

FEEDBACK_TEMPLATES = {
    "pontos_fortes": "Principais qualificações identificadas",
    "areas_melhoria": "Aspectos que podem ser aprimorados",
    "sugestoes": "Recomendações específicas de melhoria",
}

# Configuração otimizada do LLM para economia máxima
llm_economico = ChatOpenAI(
    model="gpt-4o-mini",  # Modelo mais econômico (85% mais barato que GPT-4o)
    temperature=0.1,  # Baixa variabilidade para consistência
    max_tokens=600,  # Limite de resposta para controlar custos
)

# =============================================================================
# AGENTES ESPECIALIZADOS
# =============================================================================


def criar_agentes():
    """Cria os 3 agentes especializados"""

    # AGENTE 1: Extrator de Dados
    agente_extrator = Agent(
        role="Extrator de Informações de Currículo",
        goal="Extrair dados estruturados do currículo de forma precisa",
        backstory="""Especialista em análise documental com foco em dados profissionais. 
        Extrai informações de forma sistemática e estruturada.""",
        llm=llm_economico,
        verbose=False,  # Reduz output para economia
    )

    # AGENTE 2: Avaliador
    agente_avaliador = Agent(
        role="Avaliador de Currículo",
        goal="Avaliar qualidade e identificar pontos fortes e fracos",
        backstory="""Recrutador experiente com 10 anos de mercado. 
        Especialista em avaliar perfis profissionais rapidamente.""",
        llm=llm_economico,
        verbose=False,
    )

    # AGENTE 3: Conselheiro
    agente_conselheiro = Agent(
        role="Conselheiro de Carreira",
        goal="Fornecer feedback construtivo e sugestões de melhoria",
        backstory="""Coach de carreira especialista em desenvolvimento profissional. 
        Transforma análises técnicas em conselhos práticos.""",
        llm=llm_economico,
        verbose=False,
    )

    return [agente_extrator, agente_avaliador, agente_conselheiro]


# =============================================================================
# TAREFAS DA CADEIA
# =============================================================================


def criar_tarefas(agentes, curriculo_texto):
    """Cria as tarefas da cadeia de análise"""

    agente_extrator, agente_avaliador, agente_conselheiro = agentes

    # TAREFA 1: Extração de Dados
    tarefa_extracao = Task(
        description=f"""
        Extraia informações estruturadas deste currículo: {curriculo_texto}
        
        FORMATO JSON OBRIGATÓRIO:
        {{
            "nome": "nome_candidato",
            "experiencia_anos": numero_anos,
            "educacao": "formacao_principal",
            "habilidades": ["skill1", "skill2", "skill3"],
            "cargo_atual": "posicao_atual_ou_ultima"
        }}
        
        LIMITE: Resposta em máximo 150 palavras.
        """,
        agent=agente_extrator,
        expected_output="JSON estruturado com dados do currículo",
    )

    # TAREFA 2: Avaliação
    tarefa_avaliacao = Task(
        description=f"""
        Com base nos dados extraídos da tarefa anterior, avalie o currículo usando estes critérios:
        {CRITERIOS_AVALIACAO}
        
        Forneça:
        1. Pontuação geral (0-100)
        2. Pontos fortes identificados
        3. Áreas que precisam melhorar
        
        LIMITE: Resposta em máximo 200 palavras.
        """,
        agent=agente_avaliador,
        expected_output="Avaliação estruturada com pontuação e análise",
        context=[tarefa_extracao],
    )

    # TAREFA 3: Feedback Final
    tarefa_feedback = Task(
        description="""
        Transforme a avaliação técnica da tarefa anterior em um feedback amigável e construtivo.
        
        Inclua:
        1. Cumprimento e reconhecimento dos pontos fortes
        2. Sugestões específicas de melhoria
        3. Próximos passos recomendados
        4. Tom encorajador e profissional
        
        LIMITE: Resposta em máximo 250 palavras.
        """,
        agent=agente_conselheiro,
        expected_output="Feedback final amigável e útil para o candidato",
        context=[tarefa_avaliacao],
    )

    return [tarefa_extracao, tarefa_avaliacao, tarefa_feedback]


# =============================================================================
# FUNÇÃO PRINCIPAL DE ANÁLISE
# =============================================================================


def analisar_curriculo(curriculo_texto, monitor, cache):
    """Analisa currículo através da cadeia de agentes"""

    print("=" * 60)
    print("🤖 SISTEMA DE ANÁLISE DE CURRÍCULO - CADEIA DE AGENTES")
    print("=" * 60)
    print(f"📝 Currículo recebido ({len(curriculo_texto)} caracteres)")
    print("=" * 60)

    # 1. Verificar cache primeiro
    resultado_cache = cache.buscar(curriculo_texto)
    if resultado_cache:
        print("🚀 Retornando resultado do cache...")
        return resultado_cache

    # 2. Validar entrada
    validar_entrada(curriculo_texto)

    # 3. Estimar e verificar custo
    custo_estimado = monitor.estimar_custo(curriculo_texto)
    monitor.verificar_orcamento(custo_estimado)

    print(f"💰 Custo estimado: ${custo_estimado:.6f}")
    print("🚀 Iniciando análise...")

    # 4. Criar agentes e tarefas
    agentes = criar_agentes()
    tarefas = criar_tarefas(agentes, curriculo_texto)

    # 5. Criar e executar crew
    crew_analise = Crew(
        agents=agentes,
        tasks=tarefas,
        process=Process.sequential,
        verbose=False,  # Modo silencioso para economia
    )

    # 6. Executar análise
    start_time = time.time()
    resultado = crew_analise.kickoff()
    execution_time = time.time() - start_time

    # 7. Registrar custos e métricas
    monitor.registrar_gasto(custo_estimado)
    cache.salvar(curriculo_texto, resultado)

    print(f"⏱️ Tempo de execução: {execution_time:.2f}s")
    print("\n" + "=" * 60)
    print("✅ ANÁLISE COMPLETA:")
    print("=" * 60)
    print(resultado)
    print("=" * 60)

    return resultado


# =============================================================================
# EXEMPLOS DE TESTE
# =============================================================================

CURRICULOS_EXEMPLO = {
    "desenvolvedor_junior": """
    João Silva
    Desenvolvedor Python Junior
    
    Experiência:
    - 2 anos como desenvolvedor Python
    - Projetos em Django e Flask
    - Conhecimento em SQL e PostgreSQL
    
    Educação:
    - Bacharel em Ciência da Computação - 2022
    - Curso Python Avançado - 2023
    
    Habilidades:
    Python, Django, Flask, SQL, Git, JavaScript básico
    
    Contato: joao@email.com
    """,
    "analista_senior": """
    Maria Santos
    Analista de Dados Sênior
    
    Experiência:
    - 7 anos em análise de dados
    - Liderança de equipe de 5 analistas
    - Projetos de BI e machine learning
    - Consultoria em grandes empresas
    
    Educação:
    - MBA em Data Science - 2020
    - Mestrado em Estatística - 2018
    - Certificação AWS Data Analytics
    
    Habilidades:
    Python, R, SQL, Tableau, Power BI, AWS, Machine Learning, Liderança
    
    Premiações: Melhor projeto de BI 2023
    """,
    "estagiario": """
    Pedro Costa
    Estudante de Administração
    
    Experiência:
    - Estágio em vendas (6 meses)
    - Projeto voluntário de marketing digital
    
    Educação:
    - Cursando Administração (7º semestre)
    - Curso de Excel avançado
    
    Habilidades:
    Excel, PowerPoint, Comunicação, Vendas
    
    Objetivos: Crescer na área comercial
    """,
}


def executar_exemplos():
    """Executa exemplos de teste"""

    monitor = MonitorCustos(orcamento=0.50)  # Orçamento baixo para demonstração
    cache = CacheInteligente()

    print(
        """
    🎯 EXEMPLOS DE ANÁLISE DE CURRÍCULO
    
    Este exemplo demonstra a cadeia de 3 agentes:
    1. 📊 Extrator: Extrai dados estruturados
    2. 🔍 Avaliador: Analisa qualidade e pontos fortes/fracos
    3. 💬 Conselheiro: Gera feedback amigável e construtivo
    """
    )

    for nome, curriculo in CURRICULOS_EXEMPLO.items():
        print(f"\n🔄 ANALISANDO: {nome.replace('_', ' ').title()}")

        try:
            analisar_curriculo(curriculo, monitor, cache)

            # Mostrar economia do cache na segunda execução
            if nome == "desenvolvedor_junior":
                print("\n🔄 TESTANDO CACHE - Executando mesmo currículo novamente...")
                analisar_curriculo(curriculo, monitor, cache)

        except Exception as e:
            print(f"❌ Erro na análise: {e}")

        if nome != list(CURRICULOS_EXEMPLO.keys())[-1]:
            input("\n⏸️  Pressione Enter para continuar...")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print(
        """
    🎯 EXEMPLO PRÁTICO - EXERCÍCIO 1: ANÁLISE DE CURRÍCULO
    
    Sistema demonstrando cadeia de agentes especializados com:
    ✅ Economia máxima (GPT-4o Mini)
    ✅ Cache inteligente
    ✅ Monitoramento de custos
    ✅ Validação de entrada
    ✅ 3 agentes especializados trabalhando em sequência
    """
    )

    escolha = input(
        "\nEscolha uma opção:\n1. Executar exemplos pré-definidos\n2. Analisar currículo personalizado\n\nDigite sua escolha (1 ou 2): "
    ).strip()

    if escolha == "1":
        executar_exemplos()

        print(f"\n📊 RELATÓRIO FINAL:")
        print(f"💰 Custo total: ~$0.005-0.015 por análise")
        print(f"⚡ Cache economiza: ~50% em análises repetidas")
        print(f"🎯 Economia vs GPT-4o: ~85%")

    elif escolha == "2":
        monitor = MonitorCustos(orcamento=1.0)
        cache = CacheInteligente()

        print("\n📝 Cole o texto do currículo abaixo (Ctrl+Z e Enter para finalizar):")
        curriculo_personalizado = ""
        try:
            while True:
                linha = input()
                curriculo_personalizado += linha + "\n"
        except EOFError:
            pass

        if curriculo_personalizado.strip():
            try:
                analisar_curriculo(curriculo_personalizado.strip(), monitor, cache)
            except Exception as e:
                print(f"❌ Erro na análise: {e}")
        else:
            print("❌ Nenhum currículo foi fornecido!")

    else:
        print("❌ Opção inválida!")

    print(
        "\n🎓 Exemplo concluído! Use este código como base para implementar seus próprios exercícios."
    )
