#!/usr/bin/env python3
"""
Template: Suite de Testes para Agentes CrewAI
Use este template para criar testes abrangentes para seus agentes
"""

import unittest
import time
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()


class SuiteTestesAgente(unittest.TestCase):
    """
    Suite completa de testes para agentes CrewAI

    Use este template copiando e adaptando para seus agentes específicos
    """

    @classmethod
    def setUpClass(cls):
        """Configuração inicial para toda a suite de testes"""
        cls.agente_padrao = cls._criar_agente_teste()
        cls.metricas_teste = {
            "total_testes": 0,
            "sucessos": 0,
            "falhas": 0,
            "tempo_total": 0,
        }

    @classmethod
    def _criar_agente_teste(cls):
        """Cria agente padrão para testes"""
        return Agent(
            role="Agente de Teste",
            goal="Executar tarefas de teste de forma consistente",
            backstory="""
            Você é um agente especializado em fornecer respostas
            consistentes e estruturadas para testes automatizados.
            Seja preciso e siga exatamente as instruções.
            """,
            verbose=False,
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,  # Baixa para consistência
                "max_tokens": 200,
            },
        )

    def setUp(self):
        """Configuração antes de cada teste"""
        self.start_time = time.time()
        self.__class__.metricas_teste["total_testes"] += 1

    def tearDown(self):
        """Limpeza após cada teste"""
        execution_time = time.time() - self.start_time
        self.__class__.metricas_teste["tempo_total"] += execution_time

        # Conta sucesso se o teste passou
        if not self._outcome.errors and not self._outcome.failures:
            self.__class__.metricas_teste["sucessos"] += 1
        else:
            self.__class__.metricas_teste["falhas"] += 1

    # ========================================================================
    # TESTES DE CONFIGURAÇÃO
    # ========================================================================

    def test_agente_criado_corretamente(self):
        """Testa se o agente foi criado com configurações corretas"""
        self.assertIsNotNone(self.agente_padrao)
        self.assertEqual(self.agente_padrao.role, "Agente de Teste")
        self.assertIsNotNone(self.agente_padrao.goal)
        self.assertIsNotNone(self.agente_padrao.backstory)

    def test_configuracao_llm(self):
        """Testa configurações do modelo LLM"""
        config = self.agente_padrao.llm_config
        self.assertIn("model", config)
        self.assertIn("temperature", config)
        self.assertIn("max_tokens", config)

        # Testa valores específicos
        self.assertEqual(config["temperature"], 0.1)
        self.assertEqual(config["max_tokens"], 200)

    # ========================================================================
    # TESTES DE FUNCIONALIDADE
    # ========================================================================

    def test_execucao_basica(self):
        """Testa execução básica de uma tarefa"""
        task = Task(
            description="Responda apenas: 'Teste executado com sucesso'",
            expected_output="Confirmação de teste",
            agent=self.agente_padrao,
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        resultado = crew.kickoff()
        self.assertIsNotNone(resultado)
        self.assertIn("sucesso", str(resultado).lower())

    def test_resposta_estruturada(self):
        """Testa se o agente consegue gerar respostas estruturadas"""
        task = Task(
            description="""
            Analise este feedback: 'Produto bom, entrega rápida'
            Responda no formato:
            Sentimento: [POSITIVO/NEGATIVO/NEUTRO]
            Aspectos: [lista de aspectos mencionados]
            """,
            expected_output="Análise estruturada do feedback",
            agent=self.agente_padrao,
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        resultado = crew.kickoff()
        resultado_str = str(resultado).upper()

        # Verifica estrutura da resposta
        self.assertIn("SENTIMENTO:", resultado_str)
        self.assertIn("ASPECTOS:", resultado_str)
        self.assertTrue(
            any(
                palavra in resultado_str
                for palavra in ["POSITIVO", "NEGATIVO", "NEUTRO"]
            )
        )

    def test_consistencia_respostas(self):
        """Testa consistência das respostas para o mesmo prompt"""
        prompt = "Classifique como POSITIVO ou NEGATIVO: 'Produto excelente!'"

        resultados = []
        for _ in range(3):  # Executa 3 vezes
            task = Task(
                description=prompt,
                expected_output="POSITIVO ou NEGATIVO",
                agent=self.agente_padrao,
            )

            crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

            resultado = crew.kickoff()
            resultados.append(str(resultado).upper())

        # Todas as respostas devem conter "POSITIVO"
        for resultado in resultados:
            self.assertIn("POSITIVO", resultado)

    # ========================================================================
    # TESTES DE PERFORMANCE
    # ========================================================================

    def test_tempo_resposta_aceitavel(self):
        """Testa se o tempo de resposta está dentro do aceitável"""
        task = Task(
            description="Responda 'OK' apenas",
            expected_output="Confirmação simples",
            agent=self.agente_padrao,
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        start_time = time.time()
        crew.kickoff()
        execution_time = time.time() - start_time

        # Deve responder em menos de 30 segundos
        self.assertLess(execution_time, 30.0, f"Resposta demorou {execution_time:.2f}s")

    def test_limite_tokens_respeitado(self):
        """Testa se o limite de tokens é respeitado"""
        task = Task(
            description="Escreva um texto longo sobre inteligência artificial",
            expected_output="Texto sobre IA",
            agent=self.agente_padrao,
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        resultado = crew.kickoff()

        # Estimativa simples: ~0.75 tokens por palavra
        palavras = len(str(resultado).split())
        tokens_estimados = palavras * 0.75

        # Deve respeitar o limite de 200 tokens (com margem)
        self.assertLess(
            tokens_estimados, 250, f"Resposta muito longa: ~{tokens_estimados} tokens"
        )

    # ========================================================================
    # TESTES DE ROBUSTEZ
    # ========================================================================

    def test_prompt_vazio(self):
        """Testa comportamento com prompt vazio"""
        task = Task(
            description="", expected_output="Resposta padrão", agent=self.agente_padrao
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        # Deve executar sem erro (mesmo que a resposta seja estranha)
        try:
            resultado = crew.kickoff()
            self.assertIsNotNone(resultado)
        except Exception as e:
            self.fail(f"Agente falhou com prompt vazio: {e}")

    def test_prompt_muito_longo(self):
        """Testa comportamento com prompt muito longo"""
        prompt_longo = "Analise este texto: " + "teste " * 1000  # ~1000 palavras

        task = Task(
            description=prompt_longo,
            expected_output="Análise do texto",
            agent=self.agente_padrao,
        )

        crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

        # Deve lidar com prompt longo sem falhar
        try:
            resultado = crew.kickoff()
            self.assertIsNotNone(resultado)
        except Exception as e:
            # Se falhar, deve ser por limite de tokens, não por erro interno
            self.assertIn("token", str(e).lower())

    # ========================================================================
    # TESTES ESPECÍFICOS POR DOMÍNIO
    # ========================================================================

    def test_analise_sentimento_positivo(self):
        """Testa análise de sentimento positivo"""
        feedbacks_positivos = [
            "Produto excelente! Recomendo muito!",
            "Serviço maravilhoso, equipe muito atenciosa",
            "Superou minhas expectativas em todos os aspectos",
        ]

        for feedback in feedbacks_positivos:
            with self.subTest(feedback=feedback):
                task = Task(
                    description=f"Classifique o sentimento: '{feedback}'. Responda apenas POSITIVO, NEGATIVO ou NEUTRO.",
                    expected_output="Classificação de sentimento",
                    agent=self.agente_padrao,
                )

                crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

                resultado = crew.kickoff()
                self.assertIn("POSITIVO", str(resultado).upper())

    def test_analise_sentimento_negativo(self):
        """Testa análise de sentimento negativo"""
        feedbacks_negativos = [
            "Produto terrível! Não funcionou nem um dia!",
            "Atendimento péssimo, muito insatisfeito",
            "Pior compra que já fiz, não recomendo",
        ]

        for feedback in feedbacks_negativos:
            with self.subTest(feedback=feedback):
                task = Task(
                    description=f"Classifique o sentimento: '{feedback}'. Responda apenas POSITIVO, NEGATIVO ou NEUTRO.",
                    expected_output="Classificação de sentimento",
                    agent=self.agente_padrao,
                )

                crew = Crew(agents=[self.agente_padrao], tasks=[task], verbose=False)

                resultado = crew.kickoff()
                self.assertIn("NEGATIVO", str(resultado).upper())

    @classmethod
    def tearDownClass(cls):
        """Relatório final após todos os testes"""
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print(f"{'='*60}")
        print(f"📈 Total de testes: {cls.metricas_teste['total_testes']}")
        print(f"✅ Sucessos: {cls.metricas_teste['sucessos']}")
        print(f"❌ Falhas: {cls.metricas_teste['falhas']}")
        print(f"⏱️ Tempo total: {cls.metricas_teste['tempo_total']:.2f}s")

        if cls.metricas_teste["total_testes"] > 0:
            taxa_sucesso = (
                cls.metricas_teste["sucessos"] / cls.metricas_teste["total_testes"]
            ) * 100
            tempo_medio = (
                cls.metricas_teste["tempo_total"] / cls.metricas_teste["total_testes"]
            )

            print(f"🎯 Taxa de sucesso: {taxa_sucesso:.1f}%")
            print(f"⚡ Tempo médio: {tempo_medio:.2f}s")

            if taxa_sucesso >= 90:
                print("🎉 EXCELENTE! Agente muito confiável!")
            elif taxa_sucesso >= 70:
                print("👍 BOM! Agente funcional com pequenos problemas")
            else:
                print("⚠️ ATENÇÃO! Agente precisa de melhorias")


class TestesRapidos(unittest.TestCase):
    """Suite de testes rápidos para desenvolvimento"""

    def setUp(self):
        self.agente = Agent(
            role="Teste Rápido",
            goal="Respostas rápidas para testes",
            backstory="Agente otimizado para testes rápidos",
            verbose=False,
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.0,
                "max_tokens": 50,  # Bem limitado para velocidade
            },
        )

    def test_resposta_simples(self):
        """Teste rápido de resposta simples"""
        task = Task(
            description="Responda apenas 'OK'",
            expected_output="Confirmação",
            agent=self.agente,
        )

        crew = Crew(agents=[self.agente], tasks=[task], verbose=False)
        resultado = crew.kickoff()

        self.assertIn("OK", str(resultado).upper())


def executar_suite_completa():
    """Executa suite completa de testes"""
    print("🚀 EXECUTANDO SUITE COMPLETA DE TESTES")
    print("=" * 70)

    # Carrega todas as classes de teste
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(SuiteTestesAgente))
    suite.addTests(loader.loadTestsFromTestCase(TestesRapidos))

    # Executa com relatório detalhado
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    return resultado


def executar_testes_rapidos():
    """Executa apenas testes rápidos para desenvolvimento"""
    print("⚡ EXECUTANDO TESTES RÁPIDOS")
    print("=" * 40)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestesRapidos)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    return resultado


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rapido":
        # Executa apenas testes rápidos
        executar_testes_rapidos()
    else:
        # Executa suite completa
        executar_suite_completa()

    print("\n💡 DICAS DE USO:")
    print("• python suite_testes.py         # Suite completa")
    print("• python suite_testes.py rapido  # Apenas testes rápidos")
    print("• Adapte os testes para seus agentes específicos")
    print("• Use subTest() para testes com múltiplos casos")
    print("• Monitore tempo de execução para otimização")
