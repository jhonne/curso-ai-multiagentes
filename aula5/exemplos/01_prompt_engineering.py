#!/usr/bin/env python3
"""
Exemplo 1: Técnicas Avançadas de Prompt Engineering
Demonstra como otimizar prompts para diferentes cenários
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time

load_dotenv()


class PromptEngineer:
    """Classe para demonstrar técnicas de prompt engineering"""

    @staticmethod
    def prompt_basico():
        """Exemplo de prompt básico (não otimizado)"""
        return "Analise este texto e me dê feedback"

    @staticmethod
    def prompt_few_shot():
        """Técnica Few-Shot Learning"""
        return """
        Você é um especialista em análise de sentimento. 
        Analise o texto e classifique como POSITIVO, NEGATIVO ou NEUTRO.
        
        EXEMPLOS:
        Texto: "Adorei o produto, superou minhas expectativas!"
        Análise: POSITIVO - Cliente demonstra alta satisfação
        
        Texto: "O produto é ok, nada demais"
        Análise: NEUTRO - Satisfação moderada, sem entusiasmo
        
        Texto: "Produto terrível, não recomendo"
        Análise: NEGATIVO - Cliente insatisfeito
        
        Agora analise o seguinte texto:
        """

    @staticmethod
    def prompt_chain_of_thought():
        """Técnica Chain of Thought"""
        return """
        Você é um analista de dados especializado. Analise o feedback do cliente seguindo este processo:
        
        PASSO 1: Identifique as palavras-chave principais
        PASSO 2: Determine o tom emocional
        PASSO 3: Extraia pontos específicos mencionados
        PASSO 4: Classifique a satisfação (1-5)
        PASSO 5: Sugira ações baseadas na análise
        
        Texto para análise:
        """

    @staticmethod
    def prompt_otimizado_tokens():
        """Prompt otimizado para reduzir tokens"""
        return """
        Analise o feedback. Formato:
        Sentimento: [POSITIVO/NEGATIVO/NEUTRO]
        Nota: [1-5]
        Ação: [resumo em 10 palavras]
        
        Texto:
        """


def demonstrar_prompts():
    """Demonstra diferentes técnicas de prompt"""

    # Texto de exemplo para análise
    texto_exemplo = """
    Comprei este smartphone há uma semana. A qualidade da câmera é excelente,
    muito melhor que meu celular anterior. Porém, a bateria não dura nem um dia
    inteiro, o que é muito frustrante. O atendimento ao cliente foi prestativo
    quando entrei em contato. No geral, estou satisfeito mas esperava mais.
    """

    print("📝 DEMONSTRAÇÃO: TÉCNICAS DE PROMPT ENGINEERING")
    print("=" * 60)

    # Prompt básico
    print("\n❌ PROMPT BÁSICO:")
    print(PromptEngineer.prompt_basico())
    print("Problema: Muito vago, pode gerar respostas inconsistentes")

    # Few-shot learning
    print("\n✅ PROMPT FEW-SHOT:")
    print(PromptEngineer.prompt_few_shot()[:200] + "...")
    print("Vantagem: Fornece exemplos claros do formato esperado")

    # Chain of thought
    print("\n✅ PROMPT CHAIN-OF-THOUGHT:")
    print(PromptEngineer.prompt_chain_of_thought()[:200] + "...")
    print("Vantagem: Guia o raciocínio passo a passo")

    # Otimizado para tokens
    print("\n✅ PROMPT OTIMIZADO (TOKENS):")
    print(PromptEngineer.prompt_otimizado_tokens())
    print("Vantagem: Reduz custos mantendo qualidade")

    return texto_exemplo


def criar_agente_com_prompt_otimizado():
    """Cria um agente usando prompt otimizado"""

    prompt_otimizado = """
    Você é um Analista de Feedback especializado em e-commerce.
    
    OBJETIVO: Extrair insights acionáveis de feedback de clientes
    
    MÉTODO:
    1. Identifique aspectos mencionados (produto, entrega, atendimento)
    2. Avalie sentimento para cada aspecto (positivo/negativo/neutro)
    3. Priorize ações necessárias
    
    FORMATO DE RESPOSTA:
    • Resumo: [uma linha]
    • Aspectos: [produto: sentimento, entrega: sentimento, ...]
    • Prioridade: [alta/média/baixa]
    • Ação: [uma ação específica]
    
    Seja conciso e específico.
    """

    agente = Agent(
        role="Analista de Feedback",
        goal="Extrair insights acionáveis de feedback de clientes",
        backstory=prompt_otimizado,
        verbose=True,
        llm_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.3,  # Baixa para consistência
            "max_tokens": 300,  # Limitado para ser conciso
        },
    )

    return agente


def testar_agente_otimizado():
    """Testa o agente com prompt otimizado"""

    print("\n🤖 TESTANDO AGENTE COM PROMPT OTIMIZADO")
    print("=" * 50)

    # Feedback de exemplo
    feedback = """
    O produto chegou rapidamente e bem embalado. A qualidade é boa,
    mas o preço me pareceu um pouco alto. O atendimento por chat foi
    excelente, resolveram minha dúvida em 5 minutos. Recomendo!
    """

    agente = criar_agente_com_prompt_otimizado()

    task = Task(
        description=f"Analise este feedback de cliente: {feedback}",
        expected_output="Análise estruturada seguindo o formato definido",
        agent=agente,
    )

    crew = Crew(agents=[agente], tasks=[task], verbose=True)

    print("📊 Executando análise...")
    start_time = time.time()

    try:
        result = crew.kickoff()
        execution_time = time.time() - start_time

        print(f"\n✅ Análise concluída em {execution_time:.2f}s")
        print(f"📋 Resultado:\n{result}")

    except Exception as e:
        print(f"❌ Erro na execução: {e}")


def main():
    """Função principal"""
    print("🚀 EXEMPLO 1: TÉCNICAS AVANÇADAS DE PROMPT ENGINEERING")
    print("=" * 70)

    # Demonstra as técnicas
    texto = demonstrar_prompts()

    # Testa agente otimizado
    testar_agente_otimizado()

    print("\n💡 DICAS IMPORTANTES:")
    print("1. Use exemplos específicos (few-shot) para tarefas padronizadas")
    print("2. Estruture o raciocínio (chain-of-thought) para análises complexas")
    print("3. Limite tokens com formatos específicos para reduzir custos")
    print(
        "4. Teste diferentes temperatures para balancear criatividade vs consistência"
    )
    print("\n📚 Próximo: Execute 02_configuracao_modelos.py")


if __name__ == "__main__":
    main()
