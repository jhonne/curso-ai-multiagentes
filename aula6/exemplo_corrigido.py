"""
Exemplo Corrigido - Como resolver o problema "I now can give a great answer"

Este exemplo demonstra a causa do problema e como corrigi-lo.
"""

import os
from crewai import Agent, Task, Crew, Process


def configurar_ambiente():
    """Configura o ambiente"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Configure OPENAI_API_KEY")
        return False
    
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
    return True


def exemplo_problema():
    """
    ❌ EXEMPLO COM PROBLEMA
    Este agente vai dar a resposta genérica "I now can give a great answer"
    """
    print("\n❌ EXEMPLO COM PROBLEMA:")
    print("=" * 50)
    
    # Agente com instruções vagas
    agente_problema = Agent(
        role="Assistente",
        goal="Ajudar o usuário",  # Muito vago
        backstory="Você é um assistente útil.",  # Muito genérico
        verbose=True,
    )
    
    # Tarefa com instruções vagas
    tarefa_problema = Task(
        description="Responda à pergunta do usuário sobre IA.",  # Muito vago
        expected_output="Uma resposta útil.",  # Muito genérico
        agent=agente_problema,
    )
    
    crew = Crew(
        agents=[agente_problema],
        tasks=[tarefa_problema],
        process=Process.sequential,
        verbose=True,
    )
    
    resultado = crew.kickoff()
    print(f"\n📝 Resultado: {resultado}")


def exemplo_solucao():
    """
    ✅ EXEMPLO COM SOLUÇÃO
    Este agente vai dar uma resposta específica e útil
    """
    print("\n✅ EXEMPLO COM SOLUÇÃO:")
    print("=" * 50)
    
    # Agente com instruções específicas
    agente_correto = Agent(
        role="Especialista em IA",
        goal="Explicar conceitos de IA de forma clara e específica",
        backstory="""
        Você é um especialista em inteligência artificial com 10 anos de experiência.
        
        IMPORTANTE: 
        - Sempre responda de forma específica e detalhada
        - Use exemplos práticos quando possível
        - Evite respostas genéricas
        - Foque no que foi perguntado especificamente
        """,
        verbose=True,
    )
    
    # Tarefa com instruções específicas
    tarefa_correta = Task(
        description="""
        Explique o que é inteligência artificial.
        
        Sua resposta deve incluir:
        1. Definição clara e simples de IA
        2. 2-3 exemplos práticos de uso da IA no dia a dia
        3. Uma diferença entre IA e programação tradicional
        4. Uma frase inspiradora sobre o futuro da IA
        
        Responda em português, de forma amigável e educativa.
        """,
        expected_output="""
        Explicação completa sobre IA contendo:
        - Definição clara em linguagem simples
        - Exemplos práticos e reais
        - Comparação com programação tradicional  
        - Perspectiva inspiradora sobre o futuro
        """,
        agent=agente_correto,
    )
    
    crew = Crew(
        agents=[agente_correto],
        tasks=[tarefa_correta],
        process=Process.sequential,
        verbose=True,
    )
    
    resultado = crew.kickoff()
    print(f"\n📝 Resultado: {resultado}")


def main():
    """Função principal"""
    print("🔧 DEMONSTRAÇÃO: Como resolver 'I now can give a great answer'")
    print("=" * 60)
    
    if not configurar_ambiente():
        return
    
    print("\n🎯 O problema acontece quando:")
    print("   • As instruções são muito vagas")
    print("   • O 'goal' do agente é genérico")
    print("   • A 'description' da tarefa é imprecisa")
    print("   • O 'expected_output' não é específico")
    
    print("\n💡 A solução é:")
    print("   • Instruções específicas e detalhadas")
    print("   • Goals claros e objetivos")
    print("   • Descriptions com formato exato")
    print("   • Expected_output bem definido")
    
    try:
        # Mostra o problema
        exemplo_problema()
        
        input("\n⏳ Pressione Enter para ver a solução...")
        
        # Mostra a solução
        exemplo_solucao()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("💡 Dica: Verifique se a OPENAI_API_KEY está configurada")


if __name__ == "__main__":
    main()