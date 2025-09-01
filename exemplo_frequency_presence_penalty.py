#!/usr/bin/env python3
"""
Exemplo Prático: Frequency Penalty vs Presence Penalty
Demonstra como usar esses parâmetros em diferentes tipos de agentes CrewAI
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import time
import json

load_dotenv()


class ParametrizadorPenalties:
    """Classe para gerenciar configurações de frequency e presence penalties"""

    def __init__(self):
        self.configuracoes_predefinidas = {
            "analitico": {
                "description": "Para análises técnicas e relatórios precisos",
                "frequency_penalty": 0.2,  # Reduz repetição moderadamente
                "presence_penalty": 0.1,  # Mantém foco no tópico
                "temperature": 0.2,
                "model": "gpt-4o-mini",
            },
            "criativo": {
                "description": "Para brainstorming e geração de ideias",
                "frequency_penalty": 0.6,  # Evita repetições significativamente
                "presence_penalty": 0.8,  # Força exploração de novos tópicos
                "temperature": 0.8,
                "model": "gpt-4o",
            },
            "tecnico": {
                "description": "Para documentação técnica específica",
                "frequency_penalty": 0.1,  # Permite repetir termos técnicos
                "presence_penalty": 0.0,  # Mantém foco técnico rigoroso
                "temperature": 0.1,
                "model": "gpt-4o-mini",
            },
            "educacional": {
                "description": "Para conteúdo educativo e explicativo",
                "frequency_penalty": 0.4,  # Boa variação de vocabulário
                "presence_penalty": 0.4,  # Explora diferentes aspectos
                "temperature": 0.6,
                "model": "gpt-4o-mini",
            },
            "conversacional": {
                "description": "Para chatbots e atendimento",
                "frequency_penalty": 0.3,  # Evita respostas robóticas
                "presence_penalty": 0.2,  # Mantém foco no problema
                "temperature": 0.7,
                "model": "gpt-4o-mini",
            },
        }

    def criar_llm(self, perfil: str) -> ChatOpenAI:
        """Cria LLM com configuração específica de penalties"""

        if perfil not in self.configuracoes_predefinidas:
            raise ValueError(
                f"Perfil '{perfil}' não encontrado. Disponíveis: {list(self.configuracoes_predefinidas.keys())}"
            )

        config = self.configuracoes_predefinidas[perfil]

        print(f"🔧 Configurando LLM para perfil '{perfil}':")
        print(f"   📊 Frequency Penalty: {config['frequency_penalty']}")
        print(f"   🌟 Presence Penalty: {config['presence_penalty']}")
        print(f"   🌡️ Temperature: {config['temperature']}")
        print(f"   🤖 Model: {config['model']}")
        print(f"   💭 Descrição: {config['description']}")

        return ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            model_kwargs={
                "frequency_penalty": config["frequency_penalty"],
                "presence_penalty": config["presence_penalty"],
            },
        )

    def listar_configuracoes(self):
        """Lista todas as configurações disponíveis"""
        print("\n📋 CONFIGURAÇÕES DISPONÍVEIS:")
        print("=" * 50)

        for perfil, config in self.configuracoes_predefinidas.items():
            print(f"\n🎯 {perfil.upper()}:")
            print(f"   {config['description']}")
            print(
                f"   Frequency: {config['frequency_penalty']} | Presence: {config['presence_penalty']}"
            )


class ExperimentoPenalties:
    """Classe para conduzir experimentos comparativos"""

    def __init__(self):
        self.parametrizador = ParametrizadorPenalties()
        self.resultados = {}

    def criar_agente_com_perfil(
        self, perfil: str, role: str, goal: str, backstory: str
    ) -> Agent:
        """Cria agente com perfil específico de penalties"""

        llm = self.parametrizador.criar_llm(perfil)

        return Agent(role=role, goal=goal, backstory=backstory, llm=llm, verbose=True)

    def comparar_abordagens(self, prompt_teste: str):
        """Compara diferentes abordagens para o mesmo prompt"""

        print("\n🔬 EXPERIMENTO: COMPARAÇÃO DE PENALTIES")
        print("=" * 60)
        print(f"📝 Prompt de teste: {prompt_teste[:100]}...")

        # Perfis para comparação
        perfis_teste = ["analitico", "criativo", "tecnico"]

        for perfil in perfis_teste:
            print(f"\n--- Testando perfil: {perfil.upper()} ---")

            agente = self.criar_agente_com_perfil(
                perfil=perfil,
                role=f"Especialista {perfil.title()}",
                goal=f"Responder de forma {perfil}",
                backstory=f"Expert com abordagem {perfil} para resolução de problemas",
            )

            task = Task(
                description=prompt_teste,
                expected_output=f"Resposta em estilo {perfil}, máximo 200 palavras",
                agent=agente,
            )

            crew = Crew(agents=[agente], tasks=[task], verbose=False)

            try:
                start_time = time.time()
                resultado = crew.kickoff()
                execution_time = time.time() - start_time

                # Análise básica do resultado
                texto = str(resultado)
                palavras = texto.split()
                palavras_unicas = len(set(palavra.lower() for palavra in palavras))
                diversidade = palavras_unicas / len(palavras) if palavras else 0

                self.resultados[perfil] = {
                    "texto": texto,
                    "tempo_execucao": execution_time,
                    "total_palavras": len(palavras),
                    "palavras_unicas": palavras_unicas,
                    "diversidade_vocabular": diversidade,
                    "tamanho_resposta": len(texto),
                }

                print(f"✅ Concluído em {execution_time:.2f}s")
                print(f"📊 Diversidade vocabular: {diversidade:.2f}")
                print(f"📝 Resposta ({len(texto)} chars):")
                print(f"{texto[:150]}...\n")

            except Exception as e:
                print(f"❌ Erro: {e}")
                self.resultados[perfil] = {"erro": str(e)}

    def gerar_relatorio_comparativo(self):
        """Gera relatório comparativo dos resultados"""

        print("\n📊 RELATÓRIO COMPARATIVO")
        print("=" * 50)

        if not self.resultados:
            print("❌ Nenhum resultado para comparar")
            return

        print(
            f"{'Perfil':<15} {'Diversidade':<12} {'Palavras':<10} {'Tempo(s)':<8} {'Tamanho':<8}"
        )
        print("-" * 60)

        for perfil, dados in self.resultados.items():
            if "erro" not in dados:
                print(
                    f"{perfil:<15} {dados['diversidade_vocabular']:<12.3f} "
                    f"{dados['total_palavras']:<10} {dados['tempo_execucao']:<8.2f} "
                    f"{dados['tamanho_resposta']:<8}"
                )

        # Análise qualitativa
        print("\n🔍 ANÁLISE QUALITATIVA:")

        if (
            "analitico" in self.resultados
            and "erro" not in self.resultados["analitico"]
        ):
            print(
                f"📊 Perfil Analítico: Diversidade {self.resultados['analitico']['diversidade_vocabular']:.3f}"
            )
            print("   → Esperado: Baixa diversidade, foco em precisão técnica")

        if "criativo" in self.resultados and "erro" not in self.resultados["criativo"]:
            print(
                f"🎨 Perfil Criativo: Diversidade {self.resultados['criativo']['diversidade_vocabular']:.3f}"
            )
            print("   → Esperado: Alta diversidade, exploração de novos conceitos")

        if "tecnico" in self.resultados and "erro" not in self.resultados["tecnico"]:
            print(
                f"🔧 Perfil Técnico: Diversidade {self.resultados['tecnico']['diversidade_vocabular']:.3f}"
            )
            print("   → Esperado: Baixa diversidade, repetição de termos técnicos")


def exemplo_analise_mercado():
    """Exemplo: Análise de mercado com diferentes abordagens"""

    print("🏢 EXEMPLO: ANÁLISE DE MERCADO")
    print("=" * 40)

    parametrizador = ParametrizadorPenalties()

    # Agente com foco analítico (baixo presence penalty)
    agente_focado = parametrizador.criar_llm("analitico")

    # Agente exploratório (alto presence penalty)
    agente_explorador = parametrizador.criar_llm("criativo")

    prompt = """
    Analise o mercado de carros elétricos no Brasil em 2025:
    - Principais players
    - Desafios atuais
    - Oportunidades futuras
    """

    print(f"\n📝 Prompt: {prompt}")
    print("\n🔍 Comparando abordagens...")

    # Simulação de resposta (exemplo conceitual)
    print("\n📊 RESULTADO ANALÍTICO (Frequency: 0.2, Presence: 0.1):")
    print("Focado em dados específicos, pode repetir termos técnicos importantes")

    print("\n🌟 RESULTADO EXPLORATÓRIO (Frequency: 0.6, Presence: 0.8):")
    print("Explora múltiplos aspectos, introduz novos tópicos e perspectivas")


def exemplo_conteudo_educacional():
    """Exemplo: Criação de conteúdo educacional"""

    print("\n📚 EXEMPLO: CONTEÚDO EDUCACIONAL")
    print("=" * 40)

    parametrizador = ParametrizadorPenalties()

    # Agente educacional balanceado
    agente_educador = Agent(
        role="Professor de Tecnologia",
        goal="Explicar conceitos técnicos de forma clara e didática",
        backstory="Professor experiente em explicar tecnologia de forma acessível",
        llm=parametrizador.criar_llm("educacional"),
    )

    tarefa_explicacao = Task(
        description="""
        Explique o que é Machine Learning para alguém que nunca ouviu falar do assunto.
        Use analogias e exemplos práticos. Mantenha a explicação acessível mas informativa.
        """,
        expected_output="Explicação didática de Machine Learning em linguagem simples",
        agent=agente_educador,
    )

    print("🎯 Configuração Educacional:")
    print("   Frequency Penalty: 0.4 (varia vocabulário)")
    print("   Presence Penalty: 0.4 (explora diferentes aspectos)")
    print("   → Resultado esperado: Explicação rica e variada")


def exemplo_brainstorming():
    """Exemplo: Sessão de brainstorming criativo"""

    print("\n💡 EXEMPLO: BRAINSTORMING CRIATIVO")
    print("=" * 40)

    parametrizador = ParametrizadorPenalties()

    # Agente para brainstorming com penalties altos
    agente_criativo = Agent(
        role="Especialista em Inovação",
        goal="Gerar ideias inovadoras e fora da caixa",
        backstory="Expert em pensamento criativo e soluções disruptivas",
        llm=parametrizador.criar_llm("criativo"),
    )

    tarefa_ideias = Task(
        description="""
        Gere 5 ideias inovadoras para reduzir o desperdício de alimentos em restaurantes.
        Pense em soluções tecnológicas, processos ou parcerias criativas.
        """,
        expected_output="Lista de 5 ideias criativas e inovadoras",
        agent=agente_criativo,
    )

    print("🎨 Configuração Criativa:")
    print("   Frequency Penalty: 0.6 (evita repetir ideias)")
    print("   Presence Penalty: 0.8 (força novos conceitos)")
    print("   → Resultado esperado: Ideias diversas e inovadoras")


def demonstrar_impacto_penalties():
    """Demonstra o impacto visual dos penalties"""

    print("\n🎭 DEMONSTRAÇÃO: IMPACTO DOS PENALTIES")
    print("=" * 50)

    exemplos = {
        "Sem penalties (0.0, 0.0)": {
            "texto": "O produto é bom. O produto tem qualidade. O produto é recomendado. O produto vale a pena.",
            "analise": "Repetição excessiva, pouca variação",
        },
        "Com frequency penalty (0.5, 0.0)": {
            "texto": "O produto é bom. O item tem qualidade. A mercadoria é recomendada. A aquisição vale a pena.",
            "analise": "Variação de sinônimos, menos repetição",
        },
        "Com presence penalty (0.0, 0.8)": {
            "texto": "O produto é bom. A experiência do usuário importa. Design e funcionalidade são cruciais. Investimento inteligente.",
            "analise": "Introduz novos tópicos e conceitos",
        },
        "Com ambos penalties (0.5, 0.6)": {
            "texto": "O produto é excelente. Experiência do usuário excepcional. Design inovador e funcionalidade superior. Investimento estratégico inteligente.",
            "analise": "Combina variação e exploração de novos conceitos",
        },
    }

    for config, dados in exemplos.items():
        print(f"\n{config}:")
        print(f"   📝 Exemplo: {dados['texto']}")
        print(f"   🔍 Análise: {dados['analise']}")


def executar_experimento_completo():
    """Executa experimento completo comparativo"""

    print("🧪 EXPERIMENTO COMPLETO: PENALTIES EM AÇÃO")
    print("=" * 60)

    experimento = ExperimentoPenalties()

    prompt_teste = """
    Como a inteligência artificial pode transformar a educação nos próximos 5 anos?
    Considere aspectos tecnológicos, pedagógicos e sociais.
    """

    # Lista configurações disponíveis
    experimento.parametrizador.listar_configuracoes()

    # Executa comparação
    experimento.comparar_abordagens(prompt_teste)

    # Gera relatório
    experimento.gerar_relatorio_comparativo()


def main():
    """Função principal"""

    # Verifica API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Configure a OPENAI_API_KEY no arquivo .env")
        print("💡 Execute: uv run configurar-crewai")
        return

    print("🎯 FREQUENCY PENALTY vs PRESENCE PENALTY")
    print("Exemplos Práticos com CrewAI")
    print("=" * 70)

    # Menu de exemplos
    print("\n📋 EXEMPLOS DISPONÍVEIS:")
    print("1. 🏢 Análise de Mercado")
    print("2. 📚 Conteúdo Educacional")
    print("3. 💡 Brainstorming Criativo")
    print("4. 🎭 Demonstração Visual de Impacto")
    print("5. 🧪 Experimento Completo")

    try:
        escolha = input("\n👆 Escolha um exemplo (1-5): ").strip()

        if escolha == "1":
            exemplo_analise_mercado()
        elif escolha == "2":
            exemplo_conteudo_educacional()
        elif escolha == "3":
            exemplo_brainstorming()
        elif escolha == "4":
            demonstrar_impacto_penalties()
        elif escolha == "5":
            executar_experimento_completo()
        else:
            print("❌ Opção inválida. Executando demonstração de impacto...")
            demonstrar_impacto_penalties()

    except KeyboardInterrupt:
        print("\n👋 Exemplo interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        # Fallback para demonstração básica
        demonstrar_impacto_penalties()

    print("\n💡 RESUMO DOS PARÂMETROS:")
    print("🔄 Frequency Penalty: Reduz repetição baseada em frequência")
    print("🌟 Presence Penalty: Incentiva novos tópicos evitando termos já usados")
    print("⚖️ Use ambos de forma balanceada conforme o contexto!")

    print("\n📚 Leia a documentação completa em:")
    print("   docs/GUIA_FREQUENCY_PRESENCE_PENALTY.md")


if __name__ == "__main__":
    main()
