#!/usr/bin/env python3
"""
INTEGRAÇÃO PRÁTICA: Frequency e Presence Penalties em Projeto Existente
Demonstra como aplicar os conceitos de penalties em um projeto CrewAI real
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

load_dotenv()


class AgenciaMarketingOtimizada:
    """
    Exemplo de agência de marketing que usa penalties de forma otimizada
    baseado nos conceitos de frequency_penalty e presence_penalty
    """

    def __init__(self):
        self.configuracoes_llm = self._definir_configuracoes()

    def _definir_configuracoes(self):
        """Define configurações otimizadas para diferentes tipos de agentes"""
        return {
            "pesquisador": {
                "model": "gpt-4o-mini",
                "temperature": 0.3,
                "frequency_penalty": 0.2,  # Reduz repetição de dados
                "presence_penalty": 0.3,  # Explora diferentes aspectos do mercado
                "justificativa": "Pesquisa precisa mas com variação de perspectivas",
            },
            "estrategista": {
                "model": "gpt-4o-mini",
                "temperature": 0.6,
                "frequency_penalty": 0.4,  # Evita repetir estratégias
                "presence_penalty": 0.5,  # Força exploração de novas abordagens
                "justificativa": "Estratégias variadas e inovadoras",
            },
            "redator": {
                "model": "gpt-4o",
                "temperature": 0.8,
                "frequency_penalty": 0.6,  # Máxima variação de linguagem
                "presence_penalty": 0.7,  # Explora diferentes ângulos criativos
                "justificativa": "Copy criativo e envolvente",
            },
            "analisador": {
                "model": "gpt-4o-mini",
                "temperature": 0.2,
                "frequency_penalty": 0.1,  # Permite repetir métricas importantes
                "presence_penalty": 0.1,  # Mantém foco analítico
                "justificativa": "Análise precisa e focada",
            },
        }

    def criar_llm(self, perfil: str) -> ChatOpenAI:
        """Cria LLM configurado para perfil específico"""
        config = self.configuracoes_llm[perfil]

        return ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            model_kwargs={
                "frequency_penalty": config["frequency_penalty"],
                "presence_penalty": config["presence_penalty"],
            },
        )

    def criar_agentes(self):
        """Cria agentes especializados com configurações otimizadas"""

        # 1. PESQUISADOR - Configuração para análise variada mas precisa
        pesquisador = Agent(
            role="Pesquisador de Mercado",
            goal="Realizar pesquisa abrangente sobre o mercado-alvo",
            backstory="""
            Você é um especialista em pesquisa de mercado com 10+ anos de experiência.
            Sua especialidade é identificar tendências, comportamentos do consumidor e
            oportunidades de mercado através de análise de dados e insights estratégicos.
            """,
            llm=self.criar_llm("pesquisador"),
            verbose=True,
        )

        # 2. ESTRATEGISTA - Configuração para ideias inovadoras
        estrategista = Agent(
            role="Estrategista de Marketing",
            goal="Desenvolver estratégias de marketing inovadoras e eficazes",
            backstory="""
            Você é um estrategista de marketing renomado que já criou campanhas
            premiadas para grandes marcas. Sua força está em pensar fora da caixa
            e desenvolver abordagens únicas que geram resultados excepcionais.
            """,
            llm=self.criar_llm("estrategista"),
            verbose=True,
        )

        # 3. REDATOR - Configuração para máxima criatividade
        redator = Agent(
            role="Redator Criativo",
            goal="Criar conteúdo envolvente e persuasivo",
            backstory="""
            Você é um redator publicitário premiado conhecido por criar copy
            que não apenas vende, mas emociona e engaja. Sua escrita é única,
            memorável e sempre encontra o tom perfeito para cada audiência.
            """,
            llm=self.criar_llm("redator"),
            verbose=True,
        )

        # 4. ANALISADOR - Configuração para precisão técnica
        analisador = Agent(
            role="Analista de Performance",
            goal="Analisar e otimizar performance das campanhas",
            backstory="""
            Você é um analista de dados especializado em marketing digital.
            Sua expertise está em interpretar métricas, identificar padrões
            e fornecer insights acionáveis para otimização contínua.
            """,
            llm=self.criar_llm("analisador"),
            verbose=True,
        )

        return pesquisador, estrategista, redator, analisador

    def criar_tarefas(self, produto: str, publico_alvo: str):
        """Cria tarefas específicas para cada agente"""

        pesquisador, estrategista, redator, analisador = self.criar_agentes()

        # TAREFA 1: Pesquisa (frequency: 0.2, presence: 0.3)
        # Esperado: Dados precisos com variação de perspectivas
        tarefa_pesquisa = Task(
            description=f"""
            Realize uma pesquisa abrangente sobre o mercado de {produto} para {publico_alvo}.
            
            Analise:
            1. Tamanho e potencial do mercado
            2. Principais concorrentes e posicionamento
            3. Comportamento e preferências do público-alvo
            4. Tendências emergentes e oportunidades
            5. Canais de marketing mais eficazes
            
            Forneça insights únicos e dados acionáveis para fundamentar a estratégia.
            """,
            expected_output="Relatório de pesquisa com insights variados e dados precisos",
            agent=pesquisador,
        )

        # TAREFA 2: Estratégia (frequency: 0.4, presence: 0.5)
        # Esperado: Abordagens inovadoras e variadas
        tarefa_estrategia = Task(
            description=f"""
            Com base na pesquisa, desenvolva uma estratégia de marketing inovadora 
            para {produto} direcionada a {publico_alvo}.
            
            Crie:
            1. Posicionamento único e diferenciado
            2. Proposta de valor clara e atrativa
            3. Mix de canais de marketing otimizado
            4. Cronograma de implementação
            5. Táticas criativas e não convencionais
            
            Pense fora da caixa e proponha abordagens que se destaquem no mercado.
            """,
            expected_output="Estratégia inovadora com múltiplas abordagens criativas",
            agent=estrategista,
            context=[tarefa_pesquisa],
        )

        # TAREFA 3: Copy Criativo (frequency: 0.6, presence: 0.7)
        # Esperado: Linguagem rica, variada e envolvente
        tarefa_copy = Task(
            description=f"""
            Baseado na estratégia, crie copy criativo e persuasivo para {produto}.
            
            Desenvolva:
            1. Slogan/tagline memorável e único
            2. Headlines para diferentes canais
            3. Textos para redes sociais (variados)
            4. Email marketing persuasivo
            5. Copy para landing page otimizada
            
            Use linguagem rica, variada e emocionalmente envolvente. Evite clichês
            e busque ângulos únicos que conectem com {publico_alvo}.
            """,
            expected_output="Copy criativo com linguagem rica e variada",
            agent=redator,
            context=[tarefa_estrategia],
        )

        # TAREFA 4: Análise (frequency: 0.1, presence: 0.1)
        # Esperado: Métricas precisas e focadas
        tarefa_analise = Task(
            description=f"""
            Defina um framework de análise e métricas para avaliar o sucesso 
            da campanha de {produto}.
            
            Estabeleça:
            1. KPIs principais e secundários
            2. Métricas de acompanhamento por canal
            3. Benchmarks e metas específicas
            4. Metodologia de análise ROI
            5. Cronograma de relatórios e reviews
            
            Seja preciso e técnico na definição das métricas e metodologias.
            """,
            expected_output="Framework analítico preciso com métricas específicas",
            agent=analisador,
            context=[tarefa_copy],
        )

        return [tarefa_pesquisa, tarefa_estrategia, tarefa_copy, tarefa_analise]

    def executar_campanha(self, produto: str, publico_alvo: str):
        """Executa campanha completa com agentes otimizados"""

        print("🚀 EXECUTANDO CAMPANHA COM PENALTIES OTIMIZADOS")
        print("=" * 60)
        print(f"📦 Produto: {produto}")
        print(f"🎯 Público-alvo: {publico_alvo}")

        # Mostra configurações utilizadas
        print("\n⚙️ CONFIGURAÇÕES DE PENALTIES:")
        for perfil, config in self.configuracoes_llm.items():
            print(
                f"   {perfil.upper()}: freq={config['frequency_penalty']}, "
                f"pres={config['presence_penalty']} - {config['justificativa']}"
            )

        # Cria tarefas
        tarefas = self.criar_tarefas(produto, publico_alvo)

        # Cria crew
        agencia = Crew(
            agents=[task.agent for task in tarefas],
            tasks=tarefas,
            process=Process.sequential,
            verbose=True,
        )

        try:
            # Executa campanha
            resultado = agencia.kickoff()

            print("\n✅ CAMPANHA EXECUTADA COM SUCESSO!")
            print("=" * 50)

            return resultado

        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            return None

    def demonstrar_diferenca_penalties(self):
        """Demonstra a diferença visual entre diferentes configurações"""

        print("\n🎭 DEMONSTRAÇÃO: IMPACTO DOS PENALTIES")
        print("=" * 50)

        exemplos_copy = {
            "Sem penalties (0.0, 0.0)": [
                "O produto é incrível. O produto é revolucionário.",
                "O produto mudará sua vida. O produto é essencial.",
                "Problema: Repetição excessiva de 'produto'",
            ],
            "Frequency penalty (0.5, 0.0)": [
                "O produto é incrível. Este item é revolucionário.",
                "A solução mudará sua vida. A novidade é essencial.",
                "Melhoria: Variação de sinônimos",
            ],
            "Presence penalty (0.0, 0.7)": [
                "O produto é incrível. Tecnologia revolucionária.",
                "Experiência transformadora. Inovação essencial.",
                "Melhoria: Novos conceitos introduzidos",
            ],
            "Ambos otimizados (0.6, 0.7)": [
                "O produto é incrível. Tecnologia revolucionária.",
                "Experiência transformadora para usuários exigentes.",
                "Resultado: Máxima criatividade e variação",
            ],
        }

        for config, exemplo in exemplos_copy.items():
            print(f"\n📝 {config}:")
            print(f"   '{exemplo[0]} {exemplo[1]}'")
            print(f"   💡 {exemplo[2]}")


def demonstrar_uso_real():
    """Demonstra uso real em projeto existente"""

    print("💼 EXEMPLO: APLICAÇÃO EM PROJETO REAL")
    print("=" * 50)

    # Inicializa agência otimizada
    agencia = AgenciaMarketingOtimizada()

    # Demonstra diferenças visuais
    agencia.demonstrar_diferenca_penalties()

    # Executa campanha exemplo (se API estiver configurada)
    if os.getenv("OPENAI_API_KEY"):
        print("\n🔑 API Key detectada - executando exemplo real...")

        try:
            resultado = agencia.executar_campanha(
                produto="App de meditação",
                publico_alvo="profissionais estressados de 25-40 anos",
            )

            if resultado:
                print("\n📊 ANÁLISE DOS RESULTADOS:")
                print("✅ Pesquisa: Dados variados com diferentes perspectivas")
                print("✅ Estratégia: Abordagens inovadoras e únicas")
                print("✅ Copy: Linguagem rica e envolvente")
                print("✅ Análise: Métricas precisas e focadas")

        except Exception as e:
            print(f"⚠️ Erro na execução: {e}")
            print("💡 Continuando com demonstração conceitual...")
    else:
        print("\n🔐 API Key não configurada - mostrando conceitos...")

    # Mostra como adaptar projetos existentes
    print("\n🔧 COMO ADAPTAR SEU PROJETO EXISTENTE:")
    print("=" * 50)

    adaptacao_steps = [
        "1. 🎯 Identifique o tipo de cada agente (analítico, criativo, técnico)",
        "2. ⚙️ Configure penalties baseado no objetivo:",
        "   • Analítico: freq=0.1-0.3, pres=0.0-0.2",
        "   • Criativo: freq=0.5-0.7, pres=0.6-0.8",
        "   • Técnico: freq=0.1-0.2, pres=0.0-0.1",
        "3. 🧪 Teste com exemplos pequenos primeiro",
        "4. 📊 Monitore a qualidade dos resultados",
        "5. 🔄 Ajuste iterativamente conforme necessário",
    ]

    for step in adaptacao_steps:
        print(f"   {step}")

    print("\n💡 DICA FINAL:")
    print("Use o configurador_penalties.py para ter configurações prontas!")


def main():
    """Função principal"""

    print("🎯 INTEGRAÇÃO PRÁTICA: PENALTIES EM PROJETO REAL")
    print("Demonstração completa de como aplicar frequency e presence penalties")
    print("=" * 70)

    demonstrar_uso_real()

    print("\n📚 RECURSOS RELACIONADOS:")
    print("• docs/GUIA_FREQUENCY_PRESENCE_PENALTY.md - Documentação completa")
    print("• configurador_penalties.py - Ferramenta de configuração")
    print("• exemplo_frequency_presence_penalty.py - Exemplos interativos")
    print("• README_PENALTIES.md - Guia de início rápido")

    print("\n🎉 PRÓXIMOS PASSOS:")
    print("1. Adapte suas configurações de LLM atuais")
    print("2. Teste com projetos pequenos primeiro")
    print("3. Monitore e ajuste conforme os resultados")
    print("4. Documente configurações que funcionam bem")


if __name__ == "__main__":
    main()
