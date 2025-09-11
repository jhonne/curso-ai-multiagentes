#!/usr/bin/env python3
"""
Exemplo 4: Sistema de Monitoramento e Métricas
Demonstra como implementar monitoramento de performance, custos e qualidade
"""

import time
import json
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()


class MonitorPerformance:
    """Sistema completo de monitoramento de agentes"""

    def __init__(self):
        self.metricas = defaultdict(list)
        self.inicio_sessao = datetime.now()
        self.cache_respostas = {}
        self.alertas = []

    def registrar_execucao(
        self, agente_id, tempo_execucao, tokens_usados, sucesso=True, erro=None
    ):
        """Registra métricas de uma execução"""
        registro = {
            "timestamp": datetime.now(),
            "agente_id": agente_id,
            "tempo_execucao": tempo_execucao,
            "tokens_usados": tokens_usados,
            "sucesso": sucesso,
            "erro": erro,
        }

        self.metricas[agente_id].append(registro)

        # Verifica se precisa gerar alertas
        self._verificar_alertas(agente_id, registro)

    def _verificar_alertas(self, agente_id, registro):
        """Verifica se deve gerar alertas baseado nas métricas"""

        # Alerta por tempo de execução alto
        if registro["tempo_execucao"] > 30:  # 30 segundos
            self.alertas.append(
                {
                    "tipo": "TEMPO_ALTO",
                    "agente": agente_id,
                    "valor": registro["tempo_execucao"],
                    "timestamp": datetime.now(),
                }
            )

        # Alerta por uso alto de tokens
        if registro["tokens_usados"] > 2000:
            self.alertas.append(
                {
                    "tipo": "TOKENS_ALTO",
                    "agente": agente_id,
                    "valor": registro["tokens_usados"],
                    "timestamp": datetime.now(),
                }
            )

        # Alerta por falha
        if not registro["sucesso"]:
            self.alertas.append(
                {
                    "tipo": "FALHA",
                    "agente": agente_id,
                    "erro": registro["erro"],
                    "timestamp": datetime.now(),
                }
            )

    def calcular_estatisticas(self, agente_id=None):
        """Calcula estatísticas das execuções"""

        if agente_id:
            dados = self.metricas[agente_id]
        else:
            # Todos os agentes
            dados = []
            for agente_dados in self.metricas.values():
                dados.extend(agente_dados)

        if not dados:
            return None

        tempos = [d["tempo_execucao"] for d in dados]
        tokens = [d["tokens_usados"] for d in dados]
        sucessos = [d["sucesso"] for d in dados]

        return {
            "total_execucoes": len(dados),
            "taxa_sucesso": sum(sucessos) / len(sucessos) * 100,
            "tempo_medio": sum(tempos) / len(tempos),
            "tempo_max": max(tempos),
            "tempo_min": min(tempos),
            "tokens_total": sum(tokens),
            "tokens_medio": sum(tokens) / len(tokens),
            "custo_estimado": sum(tokens) * 0.002,  # GPT-3.5-turbo pricing
        }

    def gerar_relatorio_completo(self):
        """Gera relatório completo do sistema"""

        relatorio = []
        relatorio.append("📊 RELATÓRIO DE MONITORAMENTO")
        relatorio.append("=" * 50)
        relatorio.append(
            f"🕐 Período: {self.inicio_sessao.strftime('%H:%M:%S')} "
            f"até {datetime.now().strftime('%H:%M:%S')}"
        )

        # Estatísticas gerais
        stats_gerais = self.calcular_estatisticas()
        if stats_gerais:
            relatorio.append(f"\n📈 ESTATÍSTICAS GERAIS:")
            relatorio.append(
                f"   • Total de execuções: {stats_gerais['total_execucoes']}"
            )
            relatorio.append(
                f"   • Taxa de sucesso: {stats_gerais['taxa_sucesso']:.1f}%"
            )
            relatorio.append(f"   • Tempo médio: {stats_gerais['tempo_medio']:.2f}s")
            relatorio.append(
                f"   • Tokens utilizados: {stats_gerais['tokens_total']:.0f}"
            )
            relatorio.append(
                f"   • Custo estimado: ${stats_gerais['custo_estimado']:.4f}"
            )

        # Estatísticas por agente
        relatorio.append(f"\n🤖 POR AGENTE:")
        for agente_id in self.metricas.keys():
            stats = self.calcular_estatisticas(agente_id)
            relatorio.append(f"   {agente_id}:")
            relatorio.append(f"      Execuções: {stats['total_execucoes']}")
            relatorio.append(f"      Sucesso: {stats['taxa_sucesso']:.1f}%")
            relatorio.append(f"      Tempo médio: {stats['tempo_medio']:.2f}s")

        # Alertas
        if self.alertas:
            relatorio.append(f"\n⚠️ ALERTAS ({len(self.alertas)}):")
            for alerta in self.alertas[-5:]:  # Últimos 5 alertas
                tipo = alerta["tipo"]
                timestamp = alerta["timestamp"].strftime("%H:%M:%S")
                relatorio.append(
                    f"   {timestamp} - {tipo}: {alerta.get('valor', 'N/A')}"
                )
        else:
            relatorio.append(f"\n✅ Nenhum alerta gerado")

        return "\n".join(relatorio)


class CacheInteligente:
    """Sistema de cache para otimizar custos"""

    def __init__(self, ttl_segundos=3600):  # 1 hora de TTL
        self.cache = {}
        self.ttl = ttl_segundos
        self.hits = 0
        self.misses = 0

    def _gerar_chave(self, prompt, config):
        """Gera chave única para o cache"""
        config_str = json.dumps(config, sort_keys=True)
        return hash(f"{prompt.strip().lower()}{config_str}")

    def _is_expired(self, entrada):
        """Verifica se entrada do cache expirou"""
        return (datetime.now() - entrada["timestamp"]).seconds > self.ttl

    def get(self, prompt, config):
        """Busca no cache"""
        chave = self._gerar_chave(prompt, config)

        if chave in self.cache and not self._is_expired(self.cache[chave]):
            self.hits += 1
            return self.cache[chave]["resposta"]
        else:
            self.misses += 1
            return None

    def set(self, prompt, config, resposta):
        """Armazena no cache"""
        chave = self._gerar_chave(prompt, config)
        self.cache[chave] = {"resposta": resposta, "timestamp": datetime.now()}

    def limpar_expirados(self):
        """Remove entradas expiradas"""
        chaves_expiradas = []
        for chave, entrada in self.cache.items():
            if self._is_expired(entrada):
                chaves_expiradas.append(chave)

        for chave in chaves_expiradas:
            del self.cache[chave]

    def estatisticas(self):
        """Retorna estatísticas do cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "entradas_cache": len(self.cache),
            "economia_estimada": f"${(self.hits * 100 * 0.002):.2f}",  # Estimativa
        }


class AgenteMonitorado:
    """Wrapper para agentes com monitoramento automático"""

    def __init__(
        self, role, goal, backstory, monitor, cache=None, agente_id=None, **llm_config
    ):
        self.agente_id = agente_id or f"agente_{int(time.time())}"
        self.monitor = monitor
        self.cache = cache

        self.agente = Agent(
            role=role, goal=goal, backstory=backstory, verbose=False, **llm_config
        )

    def executar_task(self, description, expected_output):
        """Executa task com monitoramento"""

        # Verifica cache primeiro
        if self.cache:
            config = self.agente.llm_config or {}
            resposta_cache = self.cache.get(description, config)
            if resposta_cache:
                print(f"✅ Cache HIT para {self.agente_id}")
                return resposta_cache

        # Executa task
        start_time = time.time()
        sucesso = True
        erro = None
        tokens_estimados = 0

        try:
            task = Task(
                description=description,
                expected_output=expected_output,
                agent=self.agente,
            )

            crew = Crew(agents=[self.agente], tasks=[task], verbose=False)

            resultado = crew.kickoff()

            # Estima tokens (aproximação)
            tokens_estimados = len(description.split()) + len(str(resultado).split())

            # Armazena no cache
            if self.cache:
                config = self.agente.llm_config or {}
                self.cache.set(description, config, resultado)

        except Exception as e:
            sucesso = False
            erro = str(e)
            resultado = None

        # Registra métricas
        tempo_execucao = time.time() - start_time
        self.monitor.registrar_execucao(
            self.agente_id, tempo_execucao, tokens_estimados, sucesso, erro
        )

        if not sucesso:
            raise Exception(erro)

        return resultado


def demonstrar_sistema_completo():
    """Demonstra sistema completo de monitoramento"""

    print("🚀 DEMONSTRAÇÃO: SISTEMA COMPLETO DE MONITORAMENTO")
    print("=" * 60)

    # Inicializa sistemas
    monitor = MonitorPerformance()
    cache = CacheInteligente(ttl_segundos=300)  # 5 minutos

    # Cria agentes monitorados
    agentes = [
        AgenteMonitorado(
            role="Analista de Feedback",
            goal="Analisar feedback de clientes",
            backstory="Especialista em análise de sentimento",
            monitor=monitor,
            cache=cache,
            agente_id="analista_feedback",
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.3,
                "max_tokens": 200,
            },
        ),
        AgenteMonitorado(
            role="Gerador de Respostas",
            goal="Criar respostas para clientes",
            backstory="Especialista em comunicação com clientes",
            monitor=monitor,
            cache=cache,
            agente_id="gerador_respostas",
            llm_config={
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 150,
            },
        ),
    ]

    # Tarefas de teste
    tarefas = [
        ("Analise: 'Produto bom, entrega demorou'", "Análise de sentimento"),
        ("Crie resposta para reclamação de entrega", "Resposta profissional"),
        (
            "Analise: 'Produto bom, entrega demorou'",
            "Análise de sentimento",
        ),  # Repetida para cache
        ("Classifique prioridade: 'Sistema fora do ar'", "Classificação de prioridade"),
        ("Analise: 'Atendimento excelente!'", "Análise de sentimento"),
    ]

    print("🔄 Executando tarefas com monitoramento...")

    # Executa tarefas
    for i, (descricao, output_esperado) in enumerate(tarefas):
        agente = agentes[i % len(agentes)]
        print(f"\n   Task {i+1}: {agente.agente_id}")

        try:
            resultado = agente.executar_task(descricao, output_esperado)
            print(f"      ✅ Concluída: {str(resultado)[:50]}...")
        except Exception as e:
            print(f"      ❌ Falha: {str(e)[:50]}...")

    # Gera relatórios
    print("\n" + monitor.gerar_relatorio_completo())

    # Estatísticas do cache
    stats_cache = cache.estatisticas()
    print(f"\n💾 ESTATÍSTICAS DO CACHE:")
    print(f"   • Hit rate: {stats_cache['hit_rate']:.1f}%")
    print(f"   • Economia estimada: {stats_cache['economia_estimada']}")
    print(f"   • Entradas ativas: {stats_cache['entradas_cache']}")


def demonstrar_alertas_tempo_real():
    """Demonstra sistema de alertas em tempo real"""

    print("\n⚠️ DEMONSTRAÇÃO: ALERTAS EM TEMPO REAL")
    print("=" * 45)

    monitor = MonitorPerformance()

    # Simula execuções que geram alertas
    simulacoes = [
        ("agente_normal", 5.0, 500, True, None),  # Normal
        ("agente_lento", 35.0, 800, True, None),  # Tempo alto
        ("agente_gastao", 10.0, 2500, True, None),  # Tokens alto
        ("agente_problema", 15.0, 300, False, "API Error"),  # Falha
    ]

    for agente_id, tempo, tokens, sucesso, erro in simulacoes:
        monitor.registrar_execucao(agente_id, tempo, tokens, sucesso, erro)
        print(f"   Registrado: {agente_id} ({tempo}s, {tokens} tokens)")

    # Mostra alertas gerados
    if monitor.alertas:
        print(f"\n🚨 {len(monitor.alertas)} alertas gerados:")
        for alerta in monitor.alertas:
            tipo = alerta["tipo"]
            agente = alerta["agente"]
            timestamp = alerta["timestamp"].strftime("%H:%M:%S")
            print(f"   {timestamp} - {tipo}: {agente}")

    return monitor


def main():
    """Função principal"""
    print("🚀 EXEMPLO 4: SISTEMA DE MONITORAMENTO E MÉTRICAS")
    print("=" * 70)

    # Demonstra sistema completo
    demonstrar_sistema_completo()

    # Demonstra alertas
    monitor = demonstrar_alertas_tempo_real()

    print("\n💡 BENEFÍCIOS DO MONITORAMENTO:")
    print("1. 📊 Visibilidade completa do desempenho dos agentes")
    print("2. 💰 Controle de custos com tracking de tokens")
    print("3. ⚡ Otimização através de cache inteligente")
    print("4. 🚨 Alertas proativos para problemas")
    print("5. 📈 Dados para melhoria contínua")

    print("\n🎯 MÉTRICAS IMPORTANTES A MONITORAR:")
    print("• Tempo de execução por agente")
    print("• Taxa de sucesso das execuções")
    print("• Uso de tokens e custos")
    print("• Eficácia do cache")
    print("• Padrões de falhas")

    print("\n✅ Aula 5 concluída!")
    print("📚 Próximo: Aula 6 - Orquestração e integração do sistema")


if __name__ == "__main__":
    main()
