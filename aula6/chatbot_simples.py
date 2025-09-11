"""
Aula 6 - Chatbot Simples: Versão Didática

Este arquivo demonstra um chatbot multi-agente de forma bem simples.
Perfeito para entender os conceitos básicos antes de partir para exemplos mais complexos.

🎯 Objetivo: Mostrar como agentes trabalham em sequência para responder usuários
"""

from crewai import Agent, Task, Crew, Process


class ChatbotSimples:
    """
    Um chatbot que usa 3 agentes trabalhando em sequência:
    1. Analisador - entende o que o usuário quer
    2. Pesquisador - busca/processa informações
    3. Respondedor - cria a resposta final
    """

    def __init__(self):
        self.agentes = self._criar_agentes()

    def _criar_agentes(self):
        """Cria os 3 agentes especializados"""

        # Agente 1: Analisa a pergunta do usuário
        analisador = Agent(
            role="Analisador de Perguntas",
            goal="Entender exatamente o que o usuário está perguntando",
            backstory="Você é especialista em interpretar perguntas de usuários.",
            verbose=True,
        )

        # Agente 2: Pesquisa/processa informações
        pesquisador = Agent(
            role="Pesquisador de Informações",
            goal="Encontrar ou processar informações relevantes",
            backstory="Você é especialista em buscar e organizar informações.",
            verbose=True,
        )

        # Agente 3: Cria a resposta final
        respondedor = Agent(
            role="Criador de Respostas",
            goal="Criar respostas claras e úteis para o usuário",
            backstory="Você é especialista em comunicação clara e amigável.",
            verbose=True,
        )

        return {
            "analisador": analisador,
            "pesquisador": pesquisador,
            "respondedor": respondedor,
        }

    def processar(self, pergunta_usuario):
        """
        Processa uma pergunta do usuário através dos 3 agentes

        Fluxo:
        Pergunta → Analisador → Pesquisador → Respondedor → Resposta Final
        """

        print(f"\n💬 Pergunta do usuário: {pergunta_usuario}")
        print("-" * 50)

        # Tarefa 1: Analisar a pergunta
        tarefa_analise = Task(
            description=f"""
            Analise esta pergunta do usuário: "{pergunta_usuario}"
            
            Identifique:
            - O que o usuário realmente quer saber
            - Que tipo de informação ele precisa
            - Como classificar esta pergunta
            """,
            expected_output="Análise clara do que o usuário está perguntando",
            agent=self.agentes["analisador"],
        )

        # Tarefa 2: Pesquisar informações
        tarefa_pesquisa = Task(
            description="""
            Com base na análise anterior, processe as informações necessárias.
            
            Organize:
            - Informações relevantes para responder
            - Fatos importantes sobre o tópico
            - Pontos-chave que devem ser mencionados
            """,
            expected_output="Informações organizadas sobre o tópico",
            agent=self.agentes["pesquisador"],
            context=[tarefa_analise],
        )

        # Tarefa 3: Criar resposta final
        tarefa_resposta = Task(
            description="""
            Crie uma resposta final para o usuário.
            
            A resposta deve ser:
            - Clara e fácil de entender
            - Útil e completa
            - Amigável e profissional
            """,
            expected_output="Resposta final completa para o usuário",
            agent=self.agentes["respondedor"],
            context=[tarefa_analise, tarefa_pesquisa],
        )

        # Criar e executar o crew
        crew = Crew(
            agents=list(self.agentes.values()),
            tasks=[tarefa_analise, tarefa_pesquisa, tarefa_resposta],
            process=Process.sequential,
        )

        # Executar e retornar resultado
        resultado = crew.kickoff()
        return resultado


def demonstracao():
    """Demonstração do chatbot com exemplos práticos"""

    print("🤖 CHATBOT SIMPLES - DEMONSTRAÇÃO")
    print("=" * 50)
    print("Este chatbot usa 3 agentes trabalhando em equipe!")
    print()

    # Criar o chatbot
    chatbot = ChatbotSimples()

    # Exemplos de perguntas para testar
    perguntas = [
        "O que é inteligência artificial?",
        "Como funciona o machine learning?",
        "Quais são as vantagens de usar múltiplos agentes?",
    ]

    # Testar cada pergunta
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n🔸 TESTE {i}")
        print("=" * 30)

        try:
            resposta = chatbot.processar(pergunta)
            print(f"\n✅ RESPOSTA FINAL:")
            print(f"{resposta}")

        except Exception as e:
            print(f"❌ Erro: {e}")

        if i < len(perguntas):
            input("\n⏳ Pressione Enter para próximo teste...")


def modo_interativo():
    """Modo interativo - usuário pode fazer perguntas"""

    print("\n🎮 MODO INTERATIVO")
    print("=" * 30)
    print("Agora você pode fazer suas próprias perguntas!")
    print("Digite 'sair' para terminar")
    print()

    chatbot = ChatbotSimples()

    while True:
        pergunta = input("💭 Sua pergunta: ").strip()

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        if not pergunta:
            print("⚠️  Por favor, digite uma pergunta válida")
            continue

        try:
            resposta = chatbot.processar(pergunta)
            print(f"\n🤖 Resposta: {resposta}\n")

        except Exception as e:
            print(f"❌ Erro ao processar: {e}\n")


if __name__ == "__main__":
    print("🎓 AULA 6 - CHATBOT MULTI-AGENTE SIMPLES")
    print("=" * 60)
    print()
    print("Escolha uma opção:")
    print("1 - Ver demonstração com exemplos")
    print("2 - Modo interativo (fazer suas perguntas)")
    print()

    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == "1":
        demonstracao()
    elif opcao == "2":
        modo_interativo()
    else:
        print("❌ Opção inválida. Execute novamente e escolha 1 ou 2.")
