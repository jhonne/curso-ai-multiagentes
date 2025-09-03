"""
Aula 6 - Exemplo Básico: Primeiro Sistema Multi-Agente

Este é o exemplo mais simples possível para entender como múltiplos agentes
trabalham juntos para processar uma conversa.

Conceitos demonstrados:
1. Definição de agentes especializados
2. Criação de tarefas sequenciais
3. Passagem de contexto entre agentes
4. Orquestração através de um Crew
"""

import os
from crewai import Agent, Task, Crew, Process

# Configuração da API (certifique-se de ter a chave configurada)
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"


def criar_agentes():
    """
    Criamos 3 agentes especializados para demonstrar o fluxo:
    1. Recepcionista - primeira análise
    2. Especialista - processamento detalhado
    3. Comunicador - resposta final
    """

    # Agente 1: Recepcionista - Faz a primeira análise
    recepcionista = Agent(
        role="Recepcionista Digital",
        goal="Receber e fazer a primeira análise da mensagem do usuário",
        backstory="""Você é um recepcionista digital experiente. 
        Sua função é receber mensagens dos usuários e fazer uma primeira 
        análise para entender o tipo de solicitação.""",
        verbose=True,
        allow_delegation=False,
    )

    # Agente 2: Especialista - Processa a informação
    especialista = Agent(
        role="Especialista em Análise",
        goal="Analisar profundamente a solicitação e buscar informações relevantes",
        backstory="""Você é um especialista em análise de informações.
        Você recebe a análise inicial do recepcionista e faz um processamento
        mais detalhado para entender exatamente o que o usuário precisa.""",
        verbose=True,
        allow_delegation=False,
    )

    # Agente 3: Comunicador - Formula a resposta final
    comunicador = Agent(
        role="Especialista em Comunicação",
        goal="Criar uma resposta clara e útil para o usuário",
        backstory="""Você é um especialista em comunicação. 
        Sua função é pegar todas as informações processadas pelos outros 
        agentes e criar uma resposta final clara, útil e amigável para o usuário.""",
        verbose=True,
        allow_delegation=False,
    )

    return recepcionista, especialista, comunicador


def criar_tarefas(mensagem_usuario, recepcionista, especialista, comunicador):
    """
    Criamos 3 tarefas sequenciais que demonstram como a informação
    flui de um agente para outro.
    """

    # Tarefa 1: Recepção e análise inicial
    tarefa_recepcao = Task(
        description=f"""
        Analise a seguinte mensagem do usuário: "{mensagem_usuario}"
        
        Sua análise deve incluir:
        1. Tipo de solicitação (pergunta, pedido de ajuda, reclamação, etc.)
        2. Tópico principal
        3. Nível de urgência aparente
        4. Informações adicionais que podem ser necessárias
        
        Seja claro e objetivo na sua análise.
        """,
        expected_output="Uma análise estruturada da mensagem do usuário com tipo, tópico e urgência",
        agent=recepcionista,
    )

    # Tarefa 2: Análise especializada
    tarefa_analise = Task(
        description="""
        Com base na análise inicial do recepcionista, faça uma análise mais profunda:
        
        1. Confirme ou refine a classificação inicial
        2. Identifique as informações específicas que o usuário precisa
        3. Determine se é necessário buscar informações adicionais
        4. Sugira o tipo de resposta mais adequado
        
        Use o contexto da análise anterior para fazer sua avaliação.
        """,
        expected_output="Análise detalhada com recomendações específicas sobre como responder",
        agent=especialista,
        context=[tarefa_recepcao],  # Esta tarefa usa o resultado da anterior
    )

    # Tarefa 3: Geração da resposta final
    tarefa_resposta = Task(
        description="""
        Com base em todas as análises anteriores, crie uma resposta final para o usuário.
        
        A resposta deve ser:
        1. Clara e fácil de entender
        2. Direta e útil
        3. Amigável e profissional
        4. Apropriada para o tipo de solicitação identificado
        
        Use todas as informações dos agentes anteriores para criar a melhor resposta possível.
        """,
        expected_output="Uma resposta final clara e útil para o usuário",
        agent=comunicador,
        context=[
            tarefa_recepcao,
            tarefa_analise,
        ],  # Esta tarefa usa ambos os resultados anteriores
    )

    return [tarefa_recepcao, tarefa_analise, tarefa_resposta]


def processar_mensagem(mensagem_usuario):
    """
    Função principal que orquestra todo o processo:
    1. Cria os agentes
    2. Cria as tarefas
    3. Executa o Crew
    4. Retorna o resultado final
    """

    print(f"\n🤖 Processando mensagem: '{mensagem_usuario}'\n")
    print("=" * 60)

    # Passo 1: Criar os agentes
    recepcionista, especialista, comunicador = criar_agentes()

    # Passo 2: Criar as tarefas
    tarefas = criar_tarefas(mensagem_usuario, recepcionista, especialista, comunicador)

    # Passo 3: Criar e executar o Crew
    crew = Crew(
        agents=[recepcionista, especialista, comunicador],
        tasks=tarefas,
        process=Process.sequential,  # Execução sequencial (uma tarefa após a outra)
        verbose=True,
    )

    # Passo 4: Executar o processo
    resultado = crew.kickoff()

    return resultado


def main():
    """
    Função principal - demonstra o sistema com alguns exemplos
    """
    print("🎓 Aula 6 - Exemplo Básico: Sistema Multi-Agente")
    print("=" * 60)
    print()
    print("Este exemplo demonstra como 3 agentes trabalham juntos:")
    print("1. 👋 Recepcionista - Faz a primeira análise")
    print("2. 🔍 Especialista - Analisa profundamente")
    print("3. 💬 Comunicador - Cria a resposta final")
    print()

    # Exemplos de teste
    exemplos = [
        "Olá! Como posso aprender sobre inteligência artificial?",
        "Estou com dificuldades para configurar meu projeto Python",
        "Qual a diferença entre machine learning e deep learning?",
    ]

    # Processar cada exemplo
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n📝 EXEMPLO {i}")
        print("=" * 40)

        try:
            resultado_final = processar_mensagem(exemplo)
            print(f"\n✅ RESPOSTA FINAL:")
            print("-" * 20)
            print(resultado_final)
            print("\n" + "=" * 60)

        except Exception as e:
            print(f"❌ Erro ao processar exemplo {i}: {str(e)}")
            continue

        # Pausa entre exemplos para melhor visualização
        input("\nPressione Enter para continuar para o próximo exemplo...")


if __name__ == "__main__":
    main()
