"""
Hello CrewAI - Exemplo Básico
Baseado no Módulo 1, Aula 1 do Curso de CrewAI

Este exemplo demonstra:
1. Como configurar um agente simples
2. Como criar uma tarefa básica
3. Como executar um crew com um único agente
"""

import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


def main():
    """Função principal do exemplo Hello CrewAI"""
    print("🚀 Iniciando Hello CrewAI...")

    # Verificar se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Erro: OPENAI_API_KEY não encontrada!")
        print("Por favor, configure sua chave de API da OpenAI no arquivo .env")
        return

    # Criando nosso primeiro agente
    hello_agent = Agent(
        role="Assistente Amigável em Português",
        goal="Cumprimentar o usuário de forma calorosa e apresentar o CrewAI em português brasileiro",
        backstory="""
        Você é um assistente virtual brasileiro, amigável e entusiasmado que adora
        apresentar pessoas ao incrível mundo do CrewAI. Você tem o dom
        de explicar conceitos complexos de forma simples e motivadora.
        Você SEMPRE responde em português brasileiro, usando uma linguagem
        calorosa e acessível para iniciantes em programação.
        """,
        verbose=True,  # Para ver o processo de pensamento do agente
        allow_delegation=False,
    )

    # Criando nossa primeira tarefa
    hello_task = Task(
        description="""
        IMPORTANTE: Responda EXCLUSIVAMENTE em português brasileiro.
        
        Crie uma mensagem de boas-vindas calorosa para alguém que está
        começando a aprender CrewAI. A mensagem deve:
        1. Cumprimentar de forma amigável em português
        2. Explicar brevemente o que é o CrewAI em linguagem simples
        3. Motivar o usuário a continuar aprendendo
        4. Incluir pelo menos um emoji
        5. Ser escrita em português brasileiro coloquial e amigável
        """,
        expected_output="""
        Uma mensagem de boas-vindas OBRIGATORIAMENTE em português brasileiro,
        amigável e motivadora, com 2-3 parágrafos explicando o CrewAI de forma
        simples e acessível. A resposta deve ser calorosa e usar linguagem
        brasileira natural.
        """,
        agent=hello_agent,
    )

    # Criando nosso primeiro crew
    hello_crew = Crew(
        agents=[hello_agent],
        tasks=[hello_task],
        verbose=True,  # Para ver todo o processo
    )

    print("\n🤖 Executando o crew...")
    print("=" * 50)

    # Executando o crew
    result = hello_crew.kickoff()

    print("\n" + "=" * 50)
    print("✅ Resultado final:")
    print("=" * 50)
    print(result)

    print("\n🎉 Hello CrewAI executado com sucesso!")


if __name__ == "__main__":
    main()
