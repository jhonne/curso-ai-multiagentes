#!/usr/bin/env python3
"""
Exercício 2: Configuração de Modelos
Pratique configuração de parâmetros OpenAI para diferentes cenários
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time

load_dotenv()


def exercicio_2a_configurar_por_cenario():
    """
    EXERCÍCIO 2A: Configure agentes para diferentes cenários

    TAREFA:
    1. Crie 3 agentes com configurações específicas:
       - Agente para brainstorming (alta criatividade)
       - Agente para análise financeira (precisão)
       - Agente para atendimento ao cliente (equilibrado)
    2. Teste cada um com tarefas apropriadas
    3. Compare os resultados
    """

    print("🏋️ EXERCÍCIO 2A: Configurações por Cenário")
    print("=" * 50)

    # TODO: Implemente os 3 agentes com configurações apropriadas

    # CENÁRIO 1: Brainstorming - precisa de criatividade
    agente_brainstorm = None  # TODO: Configure com temperature alta

    # CENÁRIO 2: Análise financeira - precisa de precisão
    agente_financeiro = None  # TODO: Configure com temperature baixa

    # CENÁRIO 3: Atendimento - precisa ser equilibrado
    agente_atendimento = None  # TODO: Configure balanceado

    # Tarefas de teste
    tarefas = [
        ("brainstorm", "Crie 5 ideias inovadoras para app de delivery"),
        ("financeiro", "Analise: Receita 100k, Custos 75k, Lucro 25k"),
        ("atendimento", "Responda: Cliente reclamando de entrega atrasada"),
    ]

    # TODO: Execute e compare resultados
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Use temperature 0.9+ para criativo, 0.1- para análise")


def exercicio_2b_sistema_fallback():
    """
    EXERCÍCIO 2B: Implemente sistema de fallback

    TAREFA:
    1. Crie uma função que tenta GPT-4 primeiro
    2. Se falhar, use GPT-3.5-turbo como fallback
    3. Se falhar novamente, use resposta padrão
    4. Registre qual método foi usado
    """

    print("\n🏋️ EXERCÍCIO 2B: Sistema de Fallback")
    print("=" * 40)

    def executar_com_fallback(prompt, config_primary, config_fallback):
        """
        TODO: Implemente sistema de fallback

        Args:
            prompt: Texto para processar
            config_primary: Configuração primária (GPT-4)
            config_fallback: Configuração de fallback (GPT-3.5)

        Returns:
            dict: {resultado: str, metodo_usado: str, sucesso: bool}
        """
        # TODO: Implementar lógica de fallback
        pass

    # TODO: Teste o sistema
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Use try/except para capturar falhas de API")


def exercicio_2c_otimizacao_custos():
    """
    EXERCÍCIO 2C: Otimização de custos

    TAREFA:
    1. Calcule custo de diferentes configurações
    2. Compare GPT-4 vs GPT-3.5-turbo para mesma tarefa
    3. Encontre configuração que balance qualidade e custo
    4. Implemente monitoramento de gastos
    """

    print("\n🏋️ EXERCÍCIO 2C: Otimização de Custos")
    print("=" * 45)

    # Preços por 1K tokens (valores de exemplo)
    precos = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    }

    def calcular_custo(modelo, tokens_input, tokens_output):
        """TODO: Implemente cálculo de custo"""
        # TODO: Calcular custo baseado nos preços
        pass

    def comparar_modelos(prompt, tokens_estimados_input, tokens_estimados_output):
        """TODO: Compare custos entre modelos"""
        # TODO: Calcular e comparar custos
        pass

    # TODO: Teste com diferentes cenários
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: GPT-4 é ~20x mais caro que GPT-3.5")


# ============================================================================
# SOLUÇÕES DE EXEMPLO
# ============================================================================


def solucao_exercicio_2a():
    """SOLUÇÃO do Exercício 2A"""

    print("✅ SOLUÇÃO 2A: Configurações por Cenário")
    print("=" * 50)

    # Agente para brainstorming - alta criatividade
    agente_brainstorm = Agent(
        role="Especialista em Brainstorming",
        goal="Gerar ideias criativas e inovadoras",
        backstory="Expert em pensamento criativo e inovação disruptiva",
        verbose=False,
        llm_config={
            "model": "gpt-4",
            "temperature": 0.9,  # Alta criatividade
            "max_tokens": 1500,  # Respostas mais elaboradas
            "top_p": 0.9,
            "frequency_penalty": 0.5,  # Evita repetições
        },
    )

    # Agente para análise financeira - alta precisão
    agente_financeiro = Agent(
        role="Analista Financeiro",
        goal="Analisar dados financeiros com precisão",
        backstory="Especialista em análise financeira rigorosa e precisa",
        verbose=False,
        llm_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,  # Baixa variabilidade
            "max_tokens": 800,  # Respostas concisas
            "top_p": 0.1,  # Focado e determinístico
            "frequency_penalty": 0.0,
        },
    )

    # Agente para atendimento - equilibrado
    agente_atendimento = Agent(
        role="Assistente de Atendimento",
        goal="Fornecer suporte amigável e eficiente",
        backstory="Especialista em atendimento ao cliente empático e eficaz",
        verbose=False,
        llm_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,  # Equilibrado
            "max_tokens": 400,  # Respostas diretas
            "top_p": 0.8,
            "frequency_penalty": 0.3,
        },
    )

    # Testa cada agente
    testes = [
        (
            agente_brainstorm,
            "Crie 5 ideias inovadoras para app de delivery",
            "Lista de ideias criativas",
        ),
        (
            agente_financeiro,
            "Analise: Receita 100k, Custos 75k, Lucro 25k. Está saudável?",
            "Análise financeira objetiva",
        ),
        (
            agente_atendimento,
            "Responda: Cliente reclamando de entrega atrasada",
            "Resposta empática e solucionadora",
        ),
    ]

    for i, (agente, tarefa, output) in enumerate(testes, 1):
        print(f"\n🤖 Teste {i}: {agente.role}")
        print(
            f"   Config: {agente.llm_config['model']}, temp={agente.llm_config['temperature']}"
        )

        task = Task(description=tarefa, expected_output=output, agent=agente)

        crew = Crew(agents=[agente], tasks=[task], verbose=False)

        try:
            start_time = time.time()
            resultado = crew.kickoff()
            tempo = time.time() - start_time

            print(f"   ⏱️ Tempo: {tempo:.2f}s")
            print(f"   📝 Resposta: {str(resultado)[:100]}...")
        except Exception as e:
            print(f"   ❌ Erro: {e}")


def solucao_exercicio_2b():
    """SOLUÇÃO do Exercício 2B"""

    print("\n✅ SOLUÇÃO 2B: Sistema de Fallback")
    print("=" * 40)

    def executar_com_fallback(descricao, output_esperado):
        """Sistema de fallback entre modelos"""

        configs = [
            {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500},  # Primário
            {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 500,
            },  # Fallback
        ]

        for i, config in enumerate(configs):
            try:
                print(f"   🔄 Tentativa {i+1}: {config['model']}")

                agente = Agent(
                    role="Agente com Fallback",
                    goal="Executar tarefa com sistema de fallback",
                    backstory="Agente resiliente com múltiplas opções de modelo",
                    verbose=False,
                    llm_config=config,
                )

                task = Task(
                    description=descricao, expected_output=output_esperado, agent=agente
                )

                crew = Crew(agents=[agente], tasks=[task], verbose=False)

                # Simula falha no primeiro modelo (para demonstração)
                if i == 0:
                    import random

                    if random.random() < 0.7:  # 70% chance de simular falha
                        raise Exception("Rate limit exceeded (simulado)")

                resultado = crew.kickoff()

                return {
                    "sucesso": True,
                    "resultado": resultado,
                    "modelo_usado": config["model"],
                    "tentativa": i + 1,
                }

            except Exception as e:
                print(f"   ❌ Falha: {str(e)[:50]}")
                if i == len(configs) - 1:  # Última tentativa
                    return {
                        "sucesso": False,
                        "resultado": "Desculpe, sistema temporariamente indisponível",
                        "modelo_usado": "resposta_padrao",
                        "tentativa": i + 1,
                        "erro": str(e),
                    }
                continue

    # Teste do sistema
    print("🧪 Testando sistema de fallback...")
    resultado = executar_com_fallback(
        "Resuma: Vendas cresceram 15% no trimestre", "Resumo executivo"
    )

    print(f"\n📊 Resultado:")
    print(f"   Sucesso: {resultado['sucesso']}")
    print(f"   Modelo usado: {resultado['modelo_usado']}")
    print(f"   Tentativa: {resultado['tentativa']}")
    if resultado["sucesso"]:
        print(f"   Resposta: {str(resultado['resultado'])[:80]}...")


def main():
    """Função principal"""
    print("🏋️ EXERCÍCIO 2: CONFIGURAÇÃO DE MODELOS")
    print("=" * 70)

    print("📋 EXERCÍCIOS PARA COMPLETAR:")
    print("2A. Configure agentes para diferentes cenários")
    print("2B. Implemente sistema de fallback")
    print("2C. Otimize custos comparando modelos")
    print()

    # Execute os exercícios (inicialmente vazios)
    exercicio_2a_configurar_por_cenario()
    exercicio_2b_sistema_fallback()
    exercicio_2c_otimizacao_custos()

    print("\n" + "=" * 70)
    print("🔍 QUER VER AS SOLUÇÕES? Descomente as funções abaixo:")
    print("# solucao_exercicio_2a()")
    print("# solucao_exercicio_2b()")

    # Descomente para ver as soluções:
    # solucao_exercicio_2a()
    # solucao_exercicio_2b()

    print("\n💰 TABELA DE CUSTOS (referência):")
    print("┌─────────────────┬─────────────┬──────────────┐")
    print("│ Modelo          │ Input/1K    │ Output/1K    │")
    print("├─────────────────┼─────────────┼──────────────┤")
    print("│ GPT-3.5-turbo   │ $0.0015     │ $0.002       │")
    print("│ GPT-4           │ $0.03       │ $0.06        │")
    print("└─────────────────┴─────────────┴──────────────┘")


if __name__ == "__main__":
    main()
