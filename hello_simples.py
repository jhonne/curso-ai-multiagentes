"""
Hello CrewAI - Versão Simplificada
Exemplo mais básico para entender os conceitos fundamentais
"""

import os
from crewai import Agent, Task, Crew

def hello_crewai_simples():
    """
    Exemplo mais simples possível do CrewAI
    """
    
    # 1. Criar um agente
    agente_saudacao = Agent(
        role="Saudador Brasileiro",
        goal="Dizer olá de forma amigável em português brasileiro",
        backstory="Você é muito amigável, brasileiro e adora cumprimentar pessoas em português.",
        verbose=True
    )
    
    # 2. Criar uma tarefa
    tarefa_saudar = Task(
        description="Diga 'Olá! Bem-vindo ao CrewAI!' de forma criativa EM PORTUGUÊS BRASILEIRO",
        expected_output="Uma saudação amigável obrigatoriamente em português brasileiro",
        agent=agente_saudacao
    )
    
    # 3. Criar um crew
    meu_crew = Crew(
        agents=[agente_saudacao],
        tasks=[tarefa_saudar]
    )
    
    # 4. Executar
    resultado = meu_crew.kickoff()
    
    return resultado

if __name__ == "__main__":
    print("=== HELLO CREWAI SIMPLES ===")
    
    # Verificar se tem a chave da OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Configure OPENAI_API_KEY antes de executar!")
        print("Exemplo: set OPENAI_API_KEY=sua_chave")
    else:
        resultado = hello_crewai_simples()
        print(f"\n🎉 Resultado: {resultado}")
