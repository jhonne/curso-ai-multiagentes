#!/usr/bin/env python3
"""
Template: Agente Otimizado
Use este template como base para criar seus próprios agentes otimizados
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import time
import json
from datetime import datetime

load_dotenv()


class AgenteOtimizadoTemplate:
    """
    Template para criar agentes com configurações otimizadas

    Use este template copiando e modificando as configurações
    para seus casos específicos.
    """

    def __init__(self, role, goal, backstory, tipo_agente="balanced"):
        """
        Inicializa o agente com configurações baseadas no tipo

        Args:
            role: Papel do agente
            goal: Objetivo do agente
            backstory: História de fundo do agente
            tipo_agente: "creative", "analytical", "conversational", "balanced"
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tipo_agente = tipo_agente

        # Configurações por tipo
        self.configs = {
            "creative": {
                "model": "gpt-4",
                "temperature": 0.9,
                "max_tokens": 2000,
                "top_p": 0.9,
            },
            "analytical": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 1000,
                "top_p": 0.1,
            },
            "conversational": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 0.8,
            },
            "balanced": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.5,
                "max_tokens": 800,
                "top_p": 0.7,
            },
        }

        # Métricas de performance
        self.metricas = {
            "execucoes": 0,
            "sucessos": 0,
            "tempo_total": 0,
            "tokens_usados": 0,
        }

    def criar_prompt_otimizado(self, contexto_especifico=""):
        """
        Cria prompt otimizado baseado no tipo de agente

        Args:
            contexto_especifico: Contexto adicional específico para a tarefa

        Returns:
            str: Prompt otimizado
        """

        # Base comum para todos os prompts
        prompt_base = f"""
        Você é um {self.role} especializado.
        
        OBJETIVO: {self.goal}
        
        CONTEXTO: {self.backstory}
        """

        # Instruções específicas por tipo
        if self.tipo_agente == "creative":
            instrucoes = """
            INSTRUÇÕES:
            - Seja criativo e inovador em suas respostas
            - Explore múltiplas perspectivas e possibilidades
            - Use analogias e exemplos criativos
            - Não tenha medo de sugerir ideias ousadas
            """
        elif self.tipo_agente == "analytical":
            instrucoes = """
            INSTRUÇÕES:
            - Seja preciso e baseado em fatos
            - Use dados e evidências para sustentar suas conclusões
            - Estruture suas respostas de forma lógica
            - Evite especulações desnecessárias
            """
        elif self.tipo_agente == "conversational":
            instrucoes = """
            INSTRUÇÕES:
            - Mantenha um tom amigável e profissional
            - Seja claro e direto em suas respostas
            - Use linguagem acessível
            - Demonstre empatia quando apropriado
            """
        else:  # balanced
            instrucoes = """
            INSTRUÇÕES:
            - Balance criatividade com precisão
            - Seja estruturado mas flexível
            - Use tom profissional mas acessível
            - Forneça exemplos práticos quando relevante
            """

        # Contexto específico da tarefa
        if contexto_especifico:
            contexto_task = f"""
            
            CONTEXTO ESPECÍFICO:
            {contexto_especifico}
            """
        else:
            contexto_task = ""

        # Formato de resposta
        formato = """
        
        FORMATO DE RESPOSTA:
        - Use estrutura clara com pontos ou numeração
        - Mantenha respostas concisas mas completas
        - Termine com uma conclusão ou recomendação
        """

        return prompt_base + instrucoes + contexto_task + formato

    def criar_agente(self, tools=None, verbose=False):
        """
        Cria o agente CrewAI com as configurações otimizadas

        Args:
            tools: Lista de ferramentas para o agente
            verbose: Se deve mostrar logs detalhados

        Returns:
            Agent: Agente CrewAI configurado
        """
        config = self.configs[self.tipo_agente]

        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=tools or [],
            verbose=verbose,
            allow_delegation=False,
            llm_config=config,
        )

    def executar_com_monitoramento(
        self, description, expected_output, tools=None, verbose=False
    ):
        """
        Executa uma tarefa com monitoramento de performance

        Args:
            description: Descrição da tarefa
            expected_output: Saída esperada
            tools: Ferramentas para o agente
            verbose: Logs detalhados

        Returns:
            dict: Resultado com métricas
        """
        start_time = time.time()
        self.metricas["execucoes"] += 1

        try:
            # Cria agente e tarefa
            agente = self.criar_agente(tools, verbose)

            task = Task(
                description=description, expected_output=expected_output, agent=agente
            )

            crew = Crew(agents=[agente], tasks=[task], verbose=verbose)

            # Executa
            resultado = crew.kickoff()

            # Calcula métricas
            tempo_execucao = time.time() - start_time
            tokens_estimados = len(description.split()) + len(str(resultado).split())

            # Atualiza métricas
            self.metricas["sucessos"] += 1
            self.metricas["tempo_total"] += tempo_execucao
            self.metricas["tokens_usados"] += tokens_estimados

            return {
                "sucesso": True,
                "resultado": resultado,
                "tempo_execucao": tempo_execucao,
                "tokens_estimados": tokens_estimados,
                "config_usada": self.configs[self.tipo_agente],
            }

        except Exception as e:
            tempo_execucao = time.time() - start_time
            self.metricas["tempo_total"] += tempo_execucao

            return {
                "sucesso": False,
                "erro": str(e),
                "tempo_execucao": tempo_execucao,
                "tokens_estimados": 0,
                "config_usada": self.configs[self.tipo_agente],
            }

    def relatorio_performance(self):
        """
        Gera relatório de performance do agente

        Returns:
            str: Relatório formatado
        """
        if self.metricas["execucoes"] == 0:
            return "Nenhuma execução registrada"

        taxa_sucesso = (self.metricas["sucessos"] / self.metricas["execucoes"]) * 100
        tempo_medio = self.metricas["tempo_total"] / self.metricas["execucoes"]
        custo_estimado = self.metricas["tokens_usados"] * 0.002

        return f"""
📊 RELATÓRIO DE PERFORMANCE - {self.role}
{'='*50}
🎯 Tipo: {self.tipo_agente}
📈 Execuções: {self.metricas["execucoes"]}
✅ Taxa de sucesso: {taxa_sucesso:.1f}%
⏱️ Tempo médio: {tempo_medio:.2f}s
🔤 Tokens usados: {self.metricas["tokens_usados"]}
💰 Custo estimado: ${custo_estimado:.4f}
⚙️ Modelo: {self.configs[self.tipo_agente]["model"]}
🌡️ Temperature: {self.configs[self.tipo_agente]["temperature"]}
        """


def exemplo_uso_template():
    """Demonstra como usar o template"""

    print("📋 EXEMPLO: USANDO O TEMPLATE DE AGENTE OTIMIZADO")
    print("=" * 60)

    # Cria agente analítico
    agente_analise = AgenteOtimizadoTemplate(
        role="Analista de Vendas",
        goal="Analisar dados de vendas e identificar tendências",
        backstory="""
        Você é um especialista em análise de dados de vendas com 10 anos
        de experiência. Sua especialidade é identificar padrões e tendências
        que ajudam empresas a tomar decisões estratégicas.
        """,
        tipo_agente="analytical",
    )

    # Cria agente criativo
    agente_marketing = AgenteOtimizadoTemplate(
        role="Especialista em Marketing",
        goal="Criar campanhas de marketing inovadoras",
        backstory="""
        Você é um expert em marketing criativo com experiência em campanhas
        virais e engagement de audiência. Sua missão é criar ideias que
        conectem com o público de forma autêntica e memorável.
        """,
        tipo_agente="creative",
    )

    # Testa os agentes
    agentes_teste = [
        (
            agente_analise,
            "Analise estas vendas: Q1: 100k, Q2: 120k, Q3: 95k, Q4: 140k",
            "Análise de tendências e recomendações",
        ),
        (
            agente_marketing,
            "Crie uma campanha para lançamento de app de fitness",
            "Conceito criativo de campanha",
        ),
    ]

    for agente, descricao, output in agentes_teste:
        print(f"\n🤖 Testando: {agente.role}")
        resultado = agente.executar_com_monitoramento(descricao, output)

        if resultado["sucesso"]:
            print(f"✅ Sucesso em {resultado['tempo_execucao']:.2f}s")
            print(f"📝 Resposta: {str(resultado['resultado'])[:100]}...")
        else:
            print(f"❌ Erro: {resultado['erro']}")

        # Mostra relatório
        print(agente.relatorio_performance())


def comparar_tipos_agentes():
    """Compara diferentes tipos de agentes na mesma tarefa"""

    print("\n🔬 COMPARAÇÃO: TIPOS DE AGENTES NA MESMA TAREFA")
    print("=" * 55)

    # Tarefa comum
    tarefa = "Analise o feedback: 'Produto bom mas caro, entrega rápida'"
    output_esperado = "Análise estruturada do feedback"

    # Cria agentes de diferentes tipos
    tipos = ["analytical", "creative", "conversational", "balanced"]

    for tipo in tipos:
        agente = AgenteOtimizadoTemplate(
            role=f"Analista {tipo.title()}",
            goal="Analisar feedback de clientes",
            backstory="Especialista em análise de feedback",
            tipo_agente=tipo,
        )

        print(f"\n🎯 Tipo: {tipo.upper()}")
        resultado = agente.executar_com_monitoramento(tarefa, output_esperado)

        if resultado["sucesso"]:
            config = resultado["config_usada"]
            print(f"   ⚙️ Config: {config['model']}, temp={config['temperature']}")
            print(f"   ⏱️ Tempo: {resultado['tempo_execucao']:.2f}s")
            print(f"   📝 Preview: {str(resultado['resultado'])[:80]}...")
        else:
            print(f"   ❌ Erro: {resultado['erro']}")


def main():
    """Função principal"""
    print("🚀 TEMPLATE: AGENTE OTIMIZADO")
    print("=" * 70)

    print("📖 COMO USAR ESTE TEMPLATE:")
    print("1. Copie a classe AgenteOtimizadoTemplate")
    print("2. Modifique as configurações conforme sua necessidade")
    print("3. Use os métodos de monitoramento para acompanhar performance")
    print("4. Ajuste parâmetros baseado nos resultados")

    # Exemplos práticos
    exemplo_uso_template()
    comparar_tipos_agentes()

    print("\n💡 DICAS PARA PERSONALIZAÇÃO:")
    print("• Ajuste temperature baseado na tarefa")
    print("• Use max_tokens apropriado para controlar custos")
    print("• Monitore sempre performance e custos")
    print("• Teste diferentes configurações para encontrar a ideal")

    print("\n✅ Template pronto para uso!")


if __name__ == "__main__":
    main()
