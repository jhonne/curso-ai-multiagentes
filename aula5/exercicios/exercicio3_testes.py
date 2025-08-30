#!/usr/bin/env python3
"""
Exercício 3: Testes e Monitoramento
Pratique criação de testes unitários e sistemas de monitoramento
"""

import unittest
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time

load_dotenv()


class ExercicioTestes(unittest.TestCase):
    """
    EXERCÍCIO 3A: Crie testes unitários para agentes

    TAREFA:
    1. Complete os métodos de teste abaixo
    2. Crie pelo menos 3 casos de teste diferentes
    3. Teste configurações específicas de agentes
    4. Valide resultados esperados
    """

    def setUp(self):
        """Configuração inicial para testes"""
        # TODO: Crie um agente para testes
        self.agente_teste = None

    def test_configuracao_agente(self):
        """TODO: Teste se o agente foi configurado corretamente"""
        # TODO: Verificar role, goal, backstory
        self.fail("Teste não implementado")

    def test_resposta_sentimento_positivo(self):
        """TODO: Teste classificação de sentimento positivo"""
        # TODO: Usar feedback positivo e verificar classificação
        self.fail("Teste não implementado")

    def test_resposta_sentimento_negativo(self):
        """TODO: Teste classificação de sentimento negativo"""
        # TODO: Usar feedback negativo e verificar classificação
        self.fail("Teste não implementado")

    def test_tempo_resposta(self):
        """TODO: Teste se resposta é gerada em tempo aceitável"""
        # TODO: Verificar se execução leva menos de 30 segundos
        self.fail("Teste não implementado")


def exercicio_3b_sistema_monitoramento():
    """
    EXERCÍCIO 3B: Implemente sistema de monitoramento

    TAREFA:
    1. Crie classe para monitorar execuções de agentes
    2. Registre métricas: tempo, tokens, sucessos/falhas
    3. Gere relatórios de performance
    4. Implemente alertas para problemas
    """

    print("🏋️ EXERCÍCIO 3B: Sistema de Monitoramento")
    print("=" * 50)

    class MonitorAgente:
        """TODO: Implemente sistema de monitoramento"""

        def __init__(self):
            # TODO: Inicializar estruturas de dados para métricas
            pass

        def registrar_execucao(self, agente_id, tempo, tokens, sucesso):
            """TODO: Registrar métricas de uma execução"""
            pass

        def gerar_relatorio(self):
            """TODO: Gerar relatório de performance"""
            pass

        def verificar_alertas(self):
            """TODO: Verificar se há problemas que precisam de alerta"""
            pass

    # TODO: Teste o sistema de monitoramento
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Use dicionários para armazenar métricas por agente")


def exercicio_3c_cache_inteligente():
    """
    EXERCÍCIO 3C: Implemente cache para otimizar custos

    TAREFA:
    1. Crie sistema de cache que armazena respostas similares
    2. Implemente função de hash para prompts
    3. Adicione TTL (time to live) para entradas
    4. Monitore taxa de acerto do cache
    """

    print("\n🏋️ EXERCÍCIO 3C: Cache Inteligente")
    print("=" * 40)

    class CacheInteligente:
        """TODO: Implemente sistema de cache"""

        def __init__(self, ttl_segundos=3600):
            # TODO: Inicializar cache com TTL
            pass

        def get(self, prompt):
            """TODO: Buscar resposta no cache"""
            pass

        def set(self, prompt, resposta):
            """TODO: Armazenar resposta no cache"""
            pass

        def estatisticas(self):
            """TODO: Retornar estatísticas do cache"""
            pass

    # TODO: Teste o sistema de cache
    print("❌ EXERCÍCIO NÃO IMPLEMENTADO")
    print("💡 DICA: Use hash() para criar chaves únicas dos prompts")


# ============================================================================
# SOLUÇÕES DE EXEMPLO
# ============================================================================


class SolucaoTestes(unittest.TestCase):
    """SOLUÇÃO do Exercício 3A"""

    def setUp(self):
        """Configuração inicial para testes"""
        self.agente_teste = Agent(
            role="Classificador de Sentimento",
            goal="Classificar sentimento de feedback como POSITIVO, NEGATIVO ou NEUTRO",
            backstory="""
            Você é um especialista em análise de sentimento.
            Responda APENAS com: POSITIVO, NEGATIVO ou NEUTRO.
            """,
            verbose=False,
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.0,  # Zero para máxima consistência
                "max_tokens": 10,  # Apenas uma palavra
            },
        )

    def test_configuracao_agente(self):
        """Testa configuração do agente"""
        self.assertEqual(self.agente_teste.role, "Classificador de Sentimento")
        self.assertIn("sentimento", self.agente_teste.goal.lower())
        self.assertEqual(self.agente_teste.llm_config["temperature"], 0.0)

    def test_resposta_sentimento_positivo(self):
        """Testa classificação positiva"""
        feedback = "Produto excelente! Superou todas as expectativas!"

        task = Task(
            description=f"Classifique: {feedback}",
            expected_output="POSITIVO, NEGATIVO ou NEUTRO",
            agent=self.agente_teste,
        )

        crew = Crew(agents=[self.agente_teste], tasks=[task], verbose=False)

        try:
            resultado = crew.kickoff()
            self.assertIn("POSITIVO", str(resultado).upper())
        except Exception as e:
            self.fail(f"Erro na execução: {e}")

    def test_resposta_sentimento_negativo(self):
        """Testa classificação negativa"""
        feedback = "Produto terrível! Não funcionou nem um dia!"

        task = Task(
            description=f"Classifique: {feedback}",
            expected_output="POSITIVO, NEGATIVO ou NEUTRO",
            agent=self.agente_teste,
        )

        crew = Crew(agents=[self.agente_teste], tasks=[task], verbose=False)

        try:
            resultado = crew.kickoff()
            self.assertIn("NEGATIVO", str(resultado).upper())
        except Exception as e:
            self.fail(f"Erro na execução: {e}")

    def test_tempo_resposta(self):
        """Testa tempo de resposta"""
        feedback = "Produto ok, nada demais"

        task = Task(
            description=f"Classifique: {feedback}",
            expected_output="POSITIVO, NEGATIVO ou NEUTRO",
            agent=self.agente_teste,
        )

        crew = Crew(agents=[self.agente_teste], tasks=[task], verbose=False)

        start_time = time.time()
        try:
            crew.kickoff()
            tempo_execucao = time.time() - start_time
            self.assertLess(tempo_execucao, 30.0, "Resposta demorou mais que 30s")
        except Exception as e:
            self.fail(f"Erro na execução: {e}")


def solucao_exercicio_3b():
    """SOLUÇÃO do Exercício 3B"""

    print("✅ SOLUÇÃO 3B: Sistema de Monitoramento")
    print("=" * 50)

    from collections import defaultdict
    from datetime import datetime

    class MonitorAgente:
        """Sistema completo de monitoramento"""

        def __init__(self):
            self.metricas = defaultdict(list)
            self.alertas = []
            self.inicio = datetime.now()

        def registrar_execucao(self, agente_id, tempo, tokens, sucesso, erro=None):
            """Registra métricas de execução"""
            registro = {
                "timestamp": datetime.now(),
                "tempo": tempo,
                "tokens": tokens,
                "sucesso": sucesso,
                "erro": erro,
            }

            self.metricas[agente_id].append(registro)

            # Verifica alertas
            if tempo > 30:
                self.alertas.append(f"⚠️ {agente_id}: Tempo alto ({tempo:.1f}s)")
            if tokens > 2000:
                self.alertas.append(f"⚠️ {agente_id}: Muitos tokens ({tokens})")
            if not sucesso:
                self.alertas.append(f"🚨 {agente_id}: Falha - {erro}")

        def gerar_relatorio(self):
            """Gera relatório completo"""
            relatorio = []
            relatorio.append("📊 RELATÓRIO DE MONITORAMENTO")
            relatorio.append("=" * 40)

            for agente_id, registros in self.metricas.items():
                if not registros:
                    continue

                sucessos = sum(1 for r in registros if r["sucesso"])
                tempos = [r["tempo"] for r in registros]
                tokens = [r["tokens"] for r in registros]

                relatorio.append(f"\n🤖 {agente_id}:")
                relatorio.append(f"   Execuções: {len(registros)}")
                relatorio.append(
                    f"   Sucessos: {sucessos}/{len(registros)} ({sucessos/len(registros)*100:.1f}%)"
                )
                relatorio.append(f"   Tempo médio: {sum(tempos)/len(tempos):.2f}s")
                relatorio.append(f"   Tokens total: {sum(tokens)}")
                relatorio.append(f"   Custo estimado: ${sum(tokens) * 0.002:.4f}")

            if self.alertas:
                relatorio.append(f"\n🚨 ALERTAS ({len(self.alertas)}):")
                for alerta in self.alertas[-5:]:  # Últimos 5
                    relatorio.append(f"   {alerta}")

            return "\n".join(relatorio)

    # Demonstração
    monitor = MonitorAgente()

    # Simula algumas execuções
    execucoes = [
        ("agente_rapido", 2.5, 150, True, None),
        ("agente_lento", 35.0, 800, True, None),  # Gera alerta de tempo
        ("agente_gastao", 5.0, 2500, True, None),  # Gera alerta de tokens
        ("agente_problema", 10.0, 300, False, "API Error"),  # Gera alerta de falha
    ]

    for agente_id, tempo, tokens, sucesso, erro in execucoes:
        monitor.registrar_execucao(agente_id, tempo, tokens, sucesso, erro)

    print(monitor.gerar_relatorio())


def main():
    """Função principal"""
    print("🏋️ EXERCÍCIO 3: TESTES E MONITORAMENTO")
    print("=" * 70)

    print("📋 EXERCÍCIOS PARA COMPLETAR:")
    print("3A. Crie testes unitários para agentes")
    print("3B. Implemente sistema de monitoramento")
    print("3C. Crie cache inteligente para otimização")
    print()

    # Executa testes (inicialmente falham)
    print("🧪 Executando testes de exercício (vão falhar até serem implementados):")
    suite = unittest.TestLoader().loadTestsFromTestCase(ExercicioTestes)
    runner = unittest.TextTestRunner(verbosity=1)
    resultado = runner.run(suite)

    # Exercícios de monitoramento
    exercicio_3b_sistema_monitoramento()
    exercicio_3c_cache_inteligente()

    print("\n" + "=" * 70)
    print("🔍 QUER VER AS SOLUÇÕES? Execute:")
    print("python -m unittest __main__.SolucaoTestes -v  # Para testes")
    print("# solucao_exercicio_3b()  # Para monitoramento")

    # Descomente para ver soluções:
    # print("\n" + "="*50)
    # solucao_exercicio_3b()

    print("\n🎯 MÉTRICAS IMPORTANTES PARA MONITORAR:")
    print("• ⏱️ Tempo de execução por agente")
    print("• 🔤 Uso de tokens e custos associados")
    print("• ✅ Taxa de sucesso das execuções")
    print("• 🚨 Padrões de falhas e erros")
    print("• 📈 Tendências de performance ao longo do tempo")

    print("\n💡 BENEFÍCIOS DO MONITORAMENTO:")
    print("• Identificação proativa de problemas")
    print("• Otimização de custos com tokens")
    print("• Melhoria contínua da performance")
    print("• Dados para tomada de decisões")


if __name__ == "__main__":
    main()
