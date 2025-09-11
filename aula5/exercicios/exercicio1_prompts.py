#!/usr/bin/env python3
"""
Exercício 1: Otimização de Prompts
Pratique técnicas avançadas de prompt engineering
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time

load_dotenv()

# TODO: Complete os exercícios abaixo


def exercicio_1_prompt_basico_vs_otimizado():
    """
    EXERCÍCIO 1A: Compare prompt básico com otimizado

    TAREFA:
    1. Crie um agente com prompt básico
    2. Crie outro agente com prompt otimizado usando few-shot learning
    3. Teste ambos com o mesmo input
    4. Compare os resultados

    INPUT DE TESTE: "Produto chegou com defeito, muito insatisfeito"
    """

    print("🏋️ EXERCÍCIO 1A: Prompt Básico vs Otimizado")
    print("=" * 50)

    # COMPLETE AQUI: Crie o agente com prompt básico
    agente_basico = None  # TODO: Implementar

    # COMPLETE AQUI: Crie o agente com prompt otimizado (few-shot)
    agente_otimizado = None  # TODO: Implementar

    # COMPLETE AQUI: Teste ambos os agentes
    input_teste = "Produto chegou com defeito, muito insatisfeito"

    # TODO: Execute e compare os resultados
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Use técnicas de few-shot learning no prompt otimizado")


def exercicio_1b_chain_of_thought():
    """
    EXERCÍCIO 1B: Implemente Chain-of-Thought prompting

    TAREFA:
    1. Crie um agente que usa chain-of-thought para análise
    2. O agente deve seguir estes passos:
       - Identificar problema principal
       - Listar aspectos afetados
       - Classificar severidade
       - Sugerir solução
    3. Teste com feedback complexo
    """

    print("\n🏋️ EXERCÍCIO 1B: Chain-of-Thought Prompting")
    print("=" * 50)

    # COMPLETE AQUI: Implemente o agente com chain-of-thought
    feedback_complexo = """
    Comprei este smartphone há duas semanas. A tela é linda e as fotos ficam
    ótimas, mas a bateria não dura nem 6 horas de uso normal. Além disso,
    o carregador que veio na caixa parou de funcionar ontem. Tentei entrar
    em contato com o suporte mas ninguém respondeu ainda. Estou pensando
    em devolver, mas gosto muito do design e das câmeras.
    """

    # TODO: Implemente o agente e teste
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Estruture o prompt com passos numerados claros")


def exercicio_1c_otimizacao_tokens():
    """
    EXERCÍCIO 1C: Otimize prompt para reduzir tokens

    TAREFA:
    1. Crie um prompt que gere respostas concisas mas informativas
    2. Use formato estruturado para reduzir verbosidade
    3. Limite max_tokens para 100
    4. Mantenha qualidade da resposta
    """

    print("\n🏋️ EXERCÍCIO 1C: Otimização para Reduzir Tokens")
    print("=" * 50)

    # COMPLETE AQUI: Crie agente otimizado para poucos tokens
    feedbacks = [
        "Produto excelente, recomendo muito!",
        "Entrega atrasou 1 semana, produto ok",
        "Péssimo atendimento, produto com defeito",
    ]

    # TODO: Teste com múltiplos feedbacks e conte tokens usados
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print(
        "💡 DICA: Use formato de resposta ultra-conciso como '★★★★☆ | Positivo | Ação: Melhorar entrega'"
    )


# ============================================================================
# SOLUÇÕES DE EXEMPLO (Descomente para ver as implementações)
# ============================================================================


def solucao_exercicio_1a():
    """SOLUÇÃO do Exercício 1A"""

    print("✅ SOLUÇÃO 1A: Prompt Básico vs Otimizado")
    print("=" * 50)

    # Agente com prompt básico
    agente_basico = Agent(
        role="Analisador de Feedback",
        goal="Analisar feedback de clientes",
        backstory="Analise o feedback e forneça uma resposta.",
        verbose=False,
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.3, "max_tokens": 200},
    )

    # Agente com prompt otimizado (few-shot)
    agente_otimizado = Agent(
        role="Especialista em Análise de Feedback",
        goal="Classificar feedback com precisão usando padrões aprendidos",
        backstory="""
        Você é um especialista em análise de feedback. Classifique seguindo estes exemplos:
        
        EXEMPLO 1:
        Feedback: "Produto ótimo, entrega rápida!"
        Análise: POSITIVO - Cliente satisfeito com produto e logística
        
        EXEMPLO 2:
        Feedback: "Produto ok, mas entrega demorou"
        Análise: NEUTRO - Produto satisfatório, problema na logística
        
        EXEMPLO 3:
        Feedback: "Produto com defeito, péssimo!"
        Análise: NEGATIVO - Problema de qualidade, cliente insatisfeito
        
        Formato: [POSITIVO/NEUTRO/NEGATIVO] - [Resumo da situação]
        """,
        verbose=False,
        llm_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,  # Mais baixa para consistência
            "max_tokens": 150,
        },
    )

    # Teste
    input_teste = "Produto chegou com defeito, muito insatisfeito"

    for nome, agente in [("BÁSICO", agente_basico), ("OTIMIZADO", agente_otimizado)]:
        print(f"\n🤖 Testando agente {nome}:")

        task = Task(
            description=f"Analise este feedback: {input_teste}",
            expected_output="Análise do sentimento e situação",
            agent=agente,
        )

        crew = Crew(agents=[agente], tasks=[task], verbose=False)

        try:
            start_time = time.time()
            resultado = crew.kickoff()
            tempo = time.time() - start_time

            print(f"   ⏱️ Tempo: {tempo:.2f}s")
            print(f"   📝 Resultado: {resultado}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")


def solucao_exercicio_1b():
    """SOLUÇÃO do Exercício 1B"""

    print("\n✅ SOLUÇÃO 1B: Chain-of-Thought")
    print("=" * 40)

    agente_cot = Agent(
        role="Analista Chain-of-Thought",
        goal="Analisar feedback seguindo processo estruturado",
        backstory="""
        Você analisa feedback seguindo exatamente estes passos:
        
        PASSO 1: Identifique o problema principal mencionado
        PASSO 2: Liste todos os aspectos afetados (produto, entrega, atendimento, etc.)
        PASSO 3: Classifique a severidade (BAIXA/MÉDIA/ALTA)
        PASSO 4: Sugira uma solução específica
        
        Sempre siga esta sequência numerada e seja específico em cada passo.
        """,
        verbose=False,
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.3, "max_tokens": 300},
    )

    feedback_complexo = """
    Comprei este smartphone há duas semanas. A tela é linda e as fotos ficam
    ótimas, mas a bateria não dura nem 6 horas de uso normal. Além disso,
    o carregador que veio na caixa parou de funcionar ontem. Tentei entrar
    em contato com o suporte mas ninguém respondeu ainda. Estou pensando
    em devolver, mas gosto muito do design e das câmeras.
    """

    task = Task(
        description=f"Analise este feedback complexo: {feedback_complexo}",
        expected_output="Análise estruturada seguindo os 4 passos",
        agent=agente_cot,
    )

    crew = Crew(agents=[agente_cot], tasks=[task], verbose=False)

    try:
        resultado = crew.kickoff()
        print(f"📝 Análise estruturada:\n{resultado}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def main():
    """Função principal"""
    print("🏋️ EXERCÍCIO 1: OTIMIZAÇÃO DE PROMPTS")
    print("=" * 70)

    print("📋 EXERCÍCIOS PARA COMPLETAR:")
    print("1A. Compare prompt básico vs otimizado")
    print("1B. Implemente chain-of-thought prompting")
    print("1C. Otimize prompt para reduzir tokens")
    print()

    # Execute os exercícios (inicialmente vazios)
    exercicio_1_prompt_basico_vs_otimizado()
    exercicio_1b_chain_of_thought()
    exercicio_1c_otimizacao_tokens()

    print("\n" + "=" * 70)
    print("🔍 QUER VER AS SOLUÇÕES? Descomente as funções abaixo:")
    print("# solucao_exercicio_1a()")
    print("# solucao_exercicio_1b()")

    # Descomente as linhas abaixo para ver as soluções:
    # solucao_exercicio_1a()
    # solucao_exercicio_1b()

    print("\n📚 RECURSOS PARA ESTUDO:")
    print("• Prompt Engineering Guide: https://www.promptingguide.ai/")
    print(
        "• OpenAI Best Practices: https://platform.openai.com/docs/guides/prompt-engineering"
    )
    print("• CrewAI Documentation: https://docs.crewai.com/")


if __name__ == "__main__":
    main()
