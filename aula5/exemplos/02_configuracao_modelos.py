#!/usr/bin/env python3
"""
Exemplo 2: Configuração Avançada de Modelos OpenAI
Demonstra como configurar diferentes parâmetros para diferentes tipos de agentes
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time
import json

load_dotenv()


class ConfiguradorModelos:
    """Classe para gerenciar configurações de modelos OpenAI"""

    @staticmethod
    def config_agente_criativo():
        """Configuração para agentes que precisam de criatividade"""
        return {
            "model": "gpt-4",
            "temperature": 0.9,  # Alta criatividade
            "max_tokens": 2000,  # Respostas mais longas
            "top_p": 0.9,  # Diversidade alta
            "frequency_penalty": 0.5,  # Evita repetições
            "presence_penalty": 0.6,  # Encoraja novos tópicos
        }

    @staticmethod
    def config_agente_analitico():
        """Configuração para agentes analíticos"""
        return {
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,  # Baixa variabilidade
            "max_tokens": 1000,  # Respostas concisas
            "top_p": 0.1,  # Focado e preciso
            "frequency_penalty": 0.0,  # Permite repetições técnicas
            "presence_penalty": 0.0,  # Mantém foco no tópico
        }

    @staticmethod
    def config_agente_conversacional():
        """Configuração para agentes de conversação"""
        return {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,  # Equilibrado
            "max_tokens": 500,  # Respostas médias
            "top_p": 0.8,  # Boa variedade
            "frequency_penalty": 0.3,  # Evita repetições moderadas
            "presence_penalty": 0.2,  # Ligeiramente variado
        }

    @staticmethod
    def config_com_fallback():
        """Configuração com sistema de fallback"""
        return {
            "primary": {"model": "gpt-4", "temperature": 0.7, "max_tokens": 1000},
            "fallback": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1000,
            },
        }


def demonstrar_configuracoes():
    """Demonstra diferentes configurações de modelos"""

    print("⚙️ CONFIGURAÇÕES POR TIPO DE AGENTE")
    print("=" * 50)

    configs = {
        "🎨 Agente Criativo": ConfiguradorModelos.config_agente_criativo(),
        "📊 Agente Analítico": ConfiguradorModelos.config_agente_analitico(),
        "💬 Agente Conversacional": ConfiguradorModelos.config_agente_conversacional(),
    }

    for tipo, config in configs.items():
        print(f"\n{tipo}:")
        for param, valor in config.items():
            if param == "temperature":
                if valor >= 0.8:
                    desc = "(alta criatividade)"
                elif valor <= 0.3:
                    desc = "(baixa variabilidade)"
                else:
                    desc = "(equilibrado)"
                print(f"  • {param}: {valor} {desc}")
            elif param == "max_tokens":
                if valor >= 1500:
                    desc = "(respostas longas)"
                elif valor <= 600:
                    desc = "(respostas curtas)"
                else:
                    desc = "(respostas médias)"
                print(f"  • {param}: {valor} {desc}")
            else:
                print(f"  • {param}: {valor}")


def criar_agentes_com_configs_diferentes():
    """Cria agentes com configurações específicas"""

    # Agente Criativo - para brainstorming
    agente_criativo = Agent(
        role="Especialista em Brainstorming",
        goal="Gerar ideias criativas e inovadoras",
        backstory="""
        Você é um expert em criatividade e inovação. Sua missão é 
        pensar fora da caixa e gerar ideias únicas e originais.
        Seja criativo, ousado e não tenha medo de sugerir coisas diferentes.
        """,
        verbose=True,
        llm_config=ConfiguradorModelos.config_agente_criativo(),
    )

    # Agente Analítico - para análise de dados
    agente_analitico = Agent(
        role="Analista de Dados",
        goal="Analisar dados de forma precisa e objetiva",
        backstory="""
        Você é um analista de dados rigoroso e metódico. Sua especialidade
        é extrair insights precisos e baseados em fatos dos dados.
        Seja objetivo, técnico e sempre forneça evidências para suas conclusões.
        """,
        verbose=True,
        llm_config=ConfiguradorModelos.config_agente_analitico(),
    )

    # Agente Conversacional - para atendimento
    agente_conversacional = Agent(
        role="Assistente de Atendimento",
        goal="Fornecer suporte amigável e eficiente aos usuários",
        backstory="""
        Você é um assistente virtual especializado em atendimento ao cliente.
        Sua missão é ajudar os usuários de forma clara, amigável e eficiente.
        Seja empático, prestativo e sempre mantenha um tom profissional.
        """,
        verbose=True,
        llm_config=ConfiguradorModelos.config_agente_conversacional(),
    )

    return agente_criativo, agente_analitico, agente_conversacional


def testar_comportamentos_diferentes():
    """Testa o mesmo prompt com agentes configurados diferentemente"""

    print("\n🧪 TESTE: MESMO PROMPT, CONFIGURAÇÕES DIFERENTES")
    print("=" * 60)

    # Prompt comum para todos os agentes
    prompt_teste = """
    Analise a seguinte situação de uma empresa de e-commerce:
    
    Dados: Vendas caíram 15% no último mês, mas o tráfego do site 
    aumentou 20%. O tempo de carregamento das páginas aumentou 3 segundos.
    
    Forneça sua análise e recomendações.
    """

    # Cria os agentes
    criativo, analitico, conversacional = criar_agentes_com_configs_diferentes()

    agentes = [
        ("🎨 Criativo", criativo),
        ("📊 Analítico", analitico),
        ("💬 Conversacional", conversacional),
    ]

    for nome, agente in agentes:
        print(f"\n{nome} analisando...")

        task = Task(
            description=prompt_teste,
            expected_output="Análise e recomendações baseadas no seu perfil",
            agent=agente,
        )

        crew = Crew(
            agents=[agente], tasks=[task], verbose=False  # Reduzido para clareza
        )

        try:
            start_time = time.time()
            result = crew.kickoff()
            execution_time = time.time() - start_time

            print(f"⏱️ Tempo: {execution_time:.2f}s")
            print(f"📋 Resposta ({len(str(result))} chars):")
            print(f"{str(result)[:200]}...")
            print("-" * 40)

        except Exception as e:
            print(f"❌ Erro: {e}")


class MonitorCustos:
    """Classe para monitorar custos de diferentes configurações"""

    def __init__(self):
        self.custos_por_modelo = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        }

    def calcular_custo(self, modelo, tokens_input, tokens_output):
        """Calcula custo estimado"""
        if modelo not in self.custos_por_modelo:
            return 0

        custos = self.custos_por_modelo[modelo]
        custo_input = (tokens_input / 1000) * custos["input"]
        custo_output = (tokens_output / 1000) * custos["output"]

        return custo_input + custo_output

    def comparar_custos(self):
        """Compara custos entre diferentes modelos"""
        print("\n💰 COMPARAÇÃO DE CUSTOS")
        print("=" * 40)

        # Simulação de uso típico
        cenarios = [
            ("Tarefa simples", 100, 50),
            ("Tarefa média", 500, 200),
            ("Tarefa complexa", 1500, 800),
        ]

        for cenario, tokens_in, tokens_out in cenarios:
            print(f"\n📋 {cenario}:")
            print(f"   Input: {tokens_in} tokens, Output: {tokens_out} tokens")

            for modelo in ["gpt-3.5-turbo", "gpt-4"]:
                custo = self.calcular_custo(modelo, tokens_in, tokens_out)
                print(f"   {modelo}: ${custo:.4f}")


def demonstrar_fallback():
    """Demonstra sistema de fallback entre modelos"""

    print("\n🔄 SISTEMA DE FALLBACK")
    print("=" * 30)

    def executar_com_fallback(prompt, config):
        """Simula execução com fallback"""
        try:
            # Tenta com modelo primário
            print(f"🔄 Tentando com {config['primary']['model']}...")

            # Simula falha (para demonstração)
            import random

            if random.random() < 0.3:  # 30% chance de falha
                raise Exception("Rate limit exceeded")

            print("✅ Sucesso com modelo primário")
            return f"Resposta do {config['primary']['model']}"

        except Exception as e:
            print(f"❌ Falha: {e}")
            print(f"🔄 Usando fallback: {config['fallback']['model']}")
            return f"Resposta do {config['fallback']['model']} (fallback)"

    config = ConfiguradorModelos.config_com_fallback()

    # Simula várias tentativas
    for i in range(3):
        print(f"\n--- Tentativa {i+1} ---")
        resultado = executar_com_fallback("Prompt de teste", config)
        print(f"📋 Resultado: {resultado}")


def main():
    """Função principal"""
    print("🚀 EXEMPLO 2: CONFIGURAÇÃO AVANÇADA DE MODELOS")
    print("=" * 70)

    # Demonstra configurações
    demonstrar_configuracoes()

    # Testa comportamentos diferentes
    testar_comportamentos_diferentes()

    # Monitora custos
    monitor = MonitorCustos()
    monitor.comparar_custos()

    # Demonstra fallback
    demonstrar_fallback()

    print("\n💡 DICAS IMPORTANTES:")
    print("1. Use temperature alta (0.8-0.9) para tarefas criativas")
    print("2. Use temperature baixa (0.1-0.3) para tarefas analíticas")
    print("3. Monitore custos: GPT-4 é ~20x mais caro que GPT-3.5")
    print("4. Implemente fallbacks para maior confiabilidade")
    print("5. Ajuste max_tokens baseado na necessidade real")
    print("\n📚 Próximo: Execute 03_testes_agentes.py")


if __name__ == "__main__":
    main()
