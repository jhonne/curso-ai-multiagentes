"""
Aula 6 - Definição dos Agentes

Este arquivo contém a definição de todos os agentes especializados
usados no sistema de chatbot multi-agente.

Cada agente tem:
- Role (papel/função)
- Goal (objetivo)
- Backstory (história/contexto)
- Configurações específicas
"""

from crewai import Agent


def criar_agente_triagem():
    """
    Agente de Triagem - Primeira análise da mensagem

    Função: Receber e classificar inicialmente a mensagem do usuário
    """
    return Agent(
        role="Especialista em Triagem de Mensagens",
        goal="Fazer a primeira análise e classificação da mensagem do usuário",
        backstory="""
        Você é um especialista em triagem com anos de experiência em 
        atendimento ao cliente. Sua função é receber mensagens e fazer 
        uma primeira classificação para direcionar ao tratamento correto.
        
        Você é excelente em:
        - Identificar o tipo de solicitação
        - Classificar a urgência
        - Detectar o sentimento da mensagem
        - Extrair informações-chave
        """,
        verbose=True,
        allow_delegation=False,
    )


def criar_agente_intencao():
    """
    Agente de Intenção - Análise profunda do que o usuário quer

    Função: Entender profundamente a intenção por trás da mensagem
    """
    return Agent(
        role="Analista de Intenções",
        goal="Compreender profundamente o que o usuário realmente precisa",
        backstory="""
        Você é um psicólogo especializado em comunicação e análise de 
        intenções. Sua expertise está em ir além das palavras e entender 
        o que as pessoas realmente querem.
        
        Suas especialidades:
        - Análise de linguagem natural
        - Identificação de necessidades ocultas
        - Compreensão de contexto emocional
        - Mapeamento de objetivos do usuário
        """,
        verbose=True,
        allow_delegation=False,
    )


def criar_agente_busca():
    """
    Agente de Busca - Processa e organiza informações

    Função: Buscar, processar e organizar informações relevantes
    """
    return Agent(
        role="Especialista em Pesquisa e Informação",
        goal="Encontrar e organizar informações relevantes para a resposta",
        backstory="""
        Você é um bibliotecário digital com vasta experiência em pesquisa 
        e organização de informações. Sua missão é encontrar dados precisos 
        e organizá-los de forma útil.
        
        Suas habilidades:
        - Pesquisa eficiente de informações
        - Organização lógica de dados
        - Verificação de relevância
        - Síntese de informações complexas
        """,
        verbose=True,
        allow_delegation=False,
    )


def criar_agente_resposta():
    """
    Agente de Resposta - Cria a resposta final

    Função: Formular a resposta final de forma clara e útil
    """
    return Agent(
        role="Especialista em Comunicação e Respostas",
        goal="Criar respostas claras, úteis e bem estruturadas",
        backstory="""
        Você é um especialista em comunicação com formação em jornalismo 
        e redação técnica. Sua missão é transformar informações complexas 
        em respostas claras e acessíveis.
        
        Seus pontos fortes:
        - Comunicação clara e objetiva
        - Adaptação ao público-alvo
        - Estruturação lógica de informações
        - Tom amigável e profissional
        """,
        verbose=True,
        allow_delegation=False,
    )


def criar_todos_agentes():
    """
    Função utilitária para criar todos os agentes de uma vez

    Retorna um dicionário com todos os agentes organizados por função
    """
    return {
        "triagem": criar_agente_triagem(),
        "intencao": criar_agente_intencao(),
        "busca": criar_agente_busca(),
        "resposta": criar_agente_resposta(),
    }


# Versões simplificadas para exemplos básicos
def criar_agentes_simples():
    """
    Versão simplificada dos agentes para exemplos introdutórios
    """

    agente_analisador = Agent(
        role="Analisador",
        goal="Entender a pergunta do usuário",
        backstory="Você entende perguntas e identifica o que as pessoas querem saber.",
        verbose=True,
    )

    agente_processador = Agent(
        role="Processador",
        goal="Processar informações sobre o tópico",
        backstory="Você organiza informações de forma clara e útil.",
        verbose=True,
    )

    agente_respondedor = Agent(
        role="Respondedor",
        goal="Criar respostas finais",
        backstory="Você cria respostas claras e amigáveis para usuários.",
        verbose=True,
    )

    return agente_analisador, agente_processador, agente_respondedor


if __name__ == "__main__":
    """
    Teste rápido para verificar se os agentes são criados corretamente
    """
    print("🤖 Testando criação de agentes...")

    # Teste agentes completos
    agentes_completos = criar_todos_agentes()
    print(f"✅ Agentes completos criados: {list(agentes_completos.keys())}")

    # Teste agentes simples
    agentes_simples = criar_agentes_simples()
    print(f"✅ Agentes simples criados: {len(agentes_simples)} agentes")

    print("\n🎯 Todos os agentes foram criados com sucesso!")
