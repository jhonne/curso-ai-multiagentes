#!/usr/bin/env python3
"""
Exemplo 3: Testes Unitários para Agentes CrewAI
Demonstra como criar e executar testes para validar o comportamento dos agentes
"""

import unittest
from unittest.mock import Mock, patch
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time
import json

load_dotenv()


class TesteAgente(unittest.TestCase):
    """Classe base para testes de agentes"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.agente_teste = Agent(
            role="Agente de Teste",
            goal="Executar testes específicos",
            backstory="Agente criado especificamente para testes unitários",
            verbose=False,
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,  # Baixa para consistência nos testes
                "max_tokens": 200,
            },
        )

    def test_criacao_agente(self):
        """Testa se o agente é criado corretamente"""
        self.assertIsNotNone(self.agente_teste)
        self.assertEqual(self.agente_teste.role, "Agente de Teste")
        self.assertEqual(self.agente_teste.goal, "Executar testes específicos")

    def test_configuracao_llm(self):
        """Testa se as configurações do LLM estão corretas"""
        config = self.agente_teste.llm_config
        self.assertEqual(config["model"], "gpt-3.5-turbo")
        self.assertEqual(config["temperature"], 0.1)
        self.assertEqual(config["max_tokens"], 200)


class TestePrompts(unittest.TestCase):
    """Testes específicos para validação de prompts"""

    def setUp(self):
        """Configuração inicial"""
        self.agente_analise = Agent(
            role="Analista de Sentimento",
            goal="Classificar sentimento de textos",
            backstory="""
            Você analisa textos e classifica o sentimento como:
            POSITIVO, NEGATIVO ou NEUTRO.
            Responda APENAS com uma dessas palavras.
            """,
            verbose=False,
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.0,  # Zero para máxima consistência
                "max_tokens": 10,
            },
        )

    def test_sentimento_positivo(self):
        """Testa classificação de sentimento positivo"""
        texto = "Adorei o produto! Superou todas as expectativas!"

        task = Task(
            description=f"Classifique o sentimento: {texto}",
            expected_output="POSITIVO, NEGATIVO ou NEUTRO",
            agent=self.agente_analise,
        )

        crew = Crew(agents=[self.agente_analise], tasks=[task], verbose=False)

        try:
            resultado = crew.kickoff()
            # Verifica se contém palavra-chave positiva
            self.assertIn("POSITIVO", str(resultado).upper())
        except Exception as e:
            self.fail(f"Teste falhou com erro: {e}")

    def test_sentimento_negativo(self):
        """Testa classificação de sentimento negativo"""
        texto = "Produto terrível! Não recomendo para ninguém!"

        task = Task(
            description=f"Classifique o sentimento: {texto}",
            expected_output="POSITIVO, NEGATIVO ou NEUTRO",
            agent=self.agente_analise,
        )

        crew = Crew(agents=[self.agente_analise], tasks=[task], verbose=False)

        try:
            resultado = crew.kickoff()
            self.assertIn("NEGATIVO", str(resultado).upper())
        except Exception as e:
            self.fail(f"Teste falhou com erro: {e}")


class TesteSistemaMonitoramento:
    """Sistema para monitorar performance dos agentes"""

    def __init__(self):
        self.metricas = {
            "execucoes_totais": 0,
            "sucessos": 0,
            "falhas": 0,
            "tempo_total": 0,
            "tokens_utilizados": 0,
        }

    def executar_teste_com_monitoramento(self, agente, task_description):
        """Executa teste e coleta métricas"""
        start_time = time.time()
        self.metricas["execucoes_totais"] += 1

        try:
            task = Task(
                description=task_description,
                expected_output="Resposta estruturada",
                agent=agente,
            )

            crew = Crew(agents=[agente], tasks=[task], verbose=False)
            resultado = crew.kickoff()

            # Simula contagem de tokens (estimativa)
            tokens_estimados = len(str(resultado).split()) * 1.3
            self.metricas["tokens_utilizados"] += tokens_estimados

            execution_time = time.time() - start_time
            self.metricas["tempo_total"] += execution_time
            self.metricas["sucessos"] += 1

            return {
                "sucesso": True,
                "resultado": resultado,
                "tempo": execution_time,
                "tokens": tokens_estimados,
            }

        except Exception as e:
            self.metricas["falhas"] += 1
            execution_time = time.time() - start_time
            self.metricas["tempo_total"] += execution_time

            return {
                "sucesso": False,
                "erro": str(e),
                "tempo": execution_time,
                "tokens": 0,
            }

    def gerar_relatorio(self):
        """Gera relatório de performance"""
        if self.metricas["execucoes_totais"] == 0:
            return "Nenhum teste executado"

        taxa_sucesso = (
            self.metricas["sucessos"] / self.metricas["execucoes_totais"]
        ) * 100
        tempo_medio = self.metricas["tempo_total"] / self.metricas["execucoes_totais"]

        return f"""
        📊 RELATÓRIO DE PERFORMANCE
        ===========================
        • Execuções totais: {self.metricas['execucoes_totais']}
        • Sucessos: {self.metricas['sucessos']}
        • Falhas: {self.metricas['falhas']}
        • Taxa de sucesso: {taxa_sucesso:.1f}%
        • Tempo médio: {tempo_medio:.2f}s
        • Tokens totais: {self.metricas['tokens_utilizados']:.0f}
        • Custo estimado: ${(self.metricas['tokens_utilizados'] * 0.002):.4f}
        """


def criar_suite_testes():
    """Cria uma suíte completa de testes para agentes"""

    print("🧪 CRIANDO SUÍTE DE TESTES")
    print("=" * 40)

    # Agente para testes
    agente_teste = Agent(
        role="Assistente de Análise",
        goal="Analisar textos e fornecer insights",
        backstory="""
        Você é um assistente especializado em análise de textos.
        Forneça sempre respostas concisas e estruturadas.
        """,
        verbose=False,
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.2, "max_tokens": 150},
    )

    # Sistema de monitoramento
    monitor = TesteSistemaMonitoramento()

    # Casos de teste
    casos_teste = [
        "Analise este feedback: 'Produto bom, entrega rápida'",
        "Resuma em uma frase: 'Cliente comprou 3 itens, pagou à vista'",
        "Classifique a prioridade: 'Sistema fora do ar há 2 horas'",
        "Extraia palavras-chave: 'Vendas aumentaram 20% no trimestre'",
        "Sugira uma ação: 'Muitas reclamações sobre atendimento'",
    ]

    print("🔄 Executando casos de teste...")

    resultados = []
    for i, caso in enumerate(casos_teste, 1):
        print(f"   Teste {i}/5: ", end="")
        resultado = monitor.executar_teste_com_monitoramento(agente_teste, caso)

        if resultado["sucesso"]:
            print(f"✅ ({resultado['tempo']:.1f}s)")
        else:
            print(f"❌ ({resultado['erro'][:30]}...)")

        resultados.append(resultado)

    # Gera relatório
    print(monitor.gerar_relatorio())

    return resultados


def demonstrar_debugging_verbose():
    """Demonstra uso do modo verbose para debugging"""

    print("\n🔍 DEMONSTRAÇÃO: DEBUGGING COM VERBOSE")
    print("=" * 50)

    agente_debug = Agent(
        role="Agente de Debug",
        goal="Demonstrar processo de raciocínio",
        backstory="""
        Você precisa explicar seu processo de raciocínio passo a passo.
        Seja detalhado sobre como chegou à conclusão.
        """,
        verbose=True,  # Ativa modo debug
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.5, "max_tokens": 300},
    )

    task = Task(
        description="""
        Analise esta situação e explique seu raciocínio:
        
        Uma loja online teve:
        - 1000 visitantes ontem
        - 50 vendas
        - Ticket médio de R$ 120
        
        A meta é 8% de conversão. A loja atingiu a meta?
        """,
        expected_output="Análise com cálculos e conclusão",
        agent=agente_debug,
    )

    crew = Crew(
        agents=[agente_debug], tasks=[task], verbose=True  # Mostra todo o processo
    )

    print("🔄 Executando com verbose=True...")
    print("(Você verá todo o processo de raciocínio do agente)")
    print("-" * 50)

    try:
        resultado = crew.kickoff()
        print(f"\n✅ Resultado final:\n{resultado}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def validar_qualidade_resposta():
    """Valida a qualidade das respostas dos agentes"""

    print("\n✅ VALIDAÇÃO DE QUALIDADE")
    print("=" * 35)

    def avaliar_resposta(resposta, criterios):
        """Avalia resposta baseada em critérios"""
        pontuacao = 0
        feedback = []

        for criterio, peso in criterios.items():
            if criterio == "tamanho" and 50 <= len(str(resposta)) <= 300:
                pontuacao += peso
                feedback.append("✅ Tamanho adequado")
            elif criterio == "estrutura" and (
                ":" in str(resposta) or "." in str(resposta)
            ):
                pontuacao += peso
                feedback.append("✅ Bem estruturada")
            elif criterio == "relevancia" and len(str(resposta).split()) >= 10:
                pontuacao += peso
                feedback.append("✅ Conteúdo relevante")

        return pontuacao, feedback

    # Critérios de qualidade
    criterios = {
        "tamanho": 30,  # 30% da nota
        "estrutura": 40,  # 40% da nota
        "relevancia": 30,  # 30% da nota
    }

    # Resposta de exemplo
    resposta_teste = """
    Análise da situação:
    • Taxa de conversão atual: 5% (50/1000)
    • Meta: 8%
    • Conclusão: Meta não atingida
    • Recomendação: Melhorar processo de venda
    """

    pontuacao, feedback = avaliar_resposta(resposta_teste, criterios)

    print(f"📊 Pontuação: {pontuacao}/100")
    print("📋 Feedback:")
    for item in feedback:
        print(f"   {item}")

    if pontuacao >= 80:
        print("🎉 Qualidade EXCELENTE!")
    elif pontuacao >= 60:
        print("👍 Qualidade BOA")
    else:
        print("⚠️ Qualidade precisa melhorar")


def main():
    """Função principal"""
    print("🚀 EXEMPLO 3: TESTES UNITÁRIOS PARA AGENTES")
    print("=" * 70)

    # Executa testes unitários básicos
    print("1️⃣ Executando testes unitários básicos...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteAgente)
    runner = unittest.TextTestRunner(verbosity=0)
    resultado = runner.run(suite)

    if resultado.wasSuccessful():
        print("✅ Todos os testes básicos passaram!")
    else:
        print("❌ Alguns testes falharam")

    # Executa suíte de testes completa
    print("\n2️⃣ Executando suíte de testes completa...")
    criar_suite_testes()

    # Demonstra debugging
    demonstrar_debugging_verbose()

    # Valida qualidade
    validar_qualidade_resposta()

    print("\n💡 DICAS PARA TESTES:")
    print("1. Use temperature=0 para testes que precisam de consistência")
    print("2. Limite max_tokens para testes mais rápidos")
    print("3. Use verbose=True apenas durante desenvolvimento")
    print("4. Monitore sempre tempo de execução e uso de tokens")
    print("5. Crie critérios objetivos para avaliar qualidade")
    print("\n📚 Próximo: Execute 04_monitoramento.py")


if __name__ == "__main__":
    main()
