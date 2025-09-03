"""
Aula 6 - Orquestrador do Sistema

Este arquivo contém a lógica principal que coordena todos os agentes
e gerencia o fluxo da conversa.

O orquestrador é o "cérebro" do sistema que:
- Recebe mensagens do usuário
- Coordena os agentes
- Gerencia o estado da conversa
- Retorna respostas organizadas
"""

from crewai import Crew, Process
from agentes import criar_todos_agentes
from tarefas import criar_tarefas_completas


class OrquestradorChatbot:
    """
    Classe principal que orquestra todo o sistema de chatbot multi-agente

    Responsabilidades:
    - Gerenciar agentes
    - Coordenar tarefas
    - Processar mensagens
    - Manter estado (futuro)
    """

    def __init__(self, verbose=True):
        """
        Inicializa o orquestrador com todos os agentes necessários

        Args:
            verbose: Se True, mostra detalhes da execução
        """
        self.verbose = verbose
        self.agentes = criar_todos_agentes()
        self.historico_conversa = []

        print("🤖 Orquestrador inicializado com sucesso!")
        print(f"   Agentes carregados: {list(self.agentes.keys())}")

    def processar_mensagem(self, mensagem_usuario):
        """
        Processa uma mensagem do usuário através de todos os agentes

        Fluxo:
        1. Cria tarefas baseadas na mensagem
        2. Monta o crew com agentes e tarefas
        3. Executa o processamento sequencial
        4. Retorna o resultado final

        Args:
            mensagem_usuario (str): A mensagem que o usuário enviou

        Returns:
            str: Resposta final processada por todos os agentes
        """

        if self.verbose:
            print(f"\n💬 Processando: '{mensagem_usuario}'")
            print("-" * 50)

        try:
            # Passo 1: Criar tarefas baseadas na mensagem
            tarefas = criar_tarefas_completas(mensagem_usuario, self.agentes)

            if self.verbose:
                print(f"📝 {len(tarefas)} tarefas criadas")

            # Passo 2: Montar o crew
            crew = Crew(
                agents=list(self.agentes.values()),
                tasks=tarefas,
                process=Process.sequential,
                verbose=self.verbose,
            )

            # Passo 3: Executar processamento
            if self.verbose:
                print("🚀 Iniciando processamento...")

            resultado = crew.kickoff()

            # Passo 4: Salvar no histórico
            self._salvar_no_historico(mensagem_usuario, resultado)

            if self.verbose:
                print("✅ Processamento concluído!")

            return resultado

        except Exception as e:
            erro_msg = f"❌ Erro ao processar mensagem: {str(e)}"
            if self.verbose:
                print(erro_msg)
            return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"

    def _salvar_no_historico(self, mensagem, resposta):
        """
        Salva a interação no histórico da conversa

        Args:
            mensagem (str): Mensagem do usuário
            resposta (str): Resposta do sistema
        """
        self.historico_conversa.append(
            {
                "usuario": mensagem,
                "sistema": resposta,
                "timestamp": self._obter_timestamp(),
            }
        )

        # Limita histórico para evitar usar muita memória
        if len(self.historico_conversa) > 10:
            self.historico_conversa = self.historico_conversa[-10:]

    def obter_historico(self):
        """
        Retorna o histórico da conversa

        Returns:
            list: Lista de interações
        """
        return self.historico_conversa.copy()

    def limpar_historico(self):
        """
        Limpa o histórico da conversa
        """
        self.historico_conversa = []
        if self.verbose:
            print("🗑️ Histórico limpo")

    def _obter_timestamp(self):
        """
        Retorna timestamp atual

        Returns:
            str: Timestamp formatado
        """
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def estatisticas(self):
        """
        Retorna estatísticas da conversa

        Returns:
            dict: Estatísticas básicas
        """
        return {
            "total_interacoes": len(self.historico_conversa),
            "agentes_ativos": len(self.agentes),
            "ultimo_timestamp": (
                self.historico_conversa[-1]["timestamp"]
                if self.historico_conversa
                else None
            ),
        }


def demonstracao_orquestrador():
    """
    Demonstração do orquestrador com exemplos práticos
    """

    print("🎭 DEMONSTRAÇÃO DO ORQUESTRADOR")
    print("=" * 50)
    print("Vamos ver como o orquestrador coordena os agentes!")
    print()

    # Criar orquestrador
    orquestrador = OrquestradorChatbot(verbose=True)

    # Exemplos de teste
    exemplos = [
        "O que é machine learning?",
        "Como posso começar a programar em Python?",
        "Qual a diferença entre IA e algoritmos tradicionais?",
    ]

    # Processar cada exemplo
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n🔸 EXEMPLO {i}")
        print("=" * 30)

        resposta = orquestrador.processar_mensagem(exemplo)

        print(f"\n✅ RESPOSTA FINAL:")
        print(f"{resposta}")

        if i < len(exemplos):
            input("\n⏳ Pressione Enter para próximo exemplo...")

    # Mostrar estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    stats = orquestrador.estatisticas()
    for chave, valor in stats.items():
        print(f"   {chave}: {valor}")


def modo_conversa_interativa():
    """
    Modo de conversa interativa com o orquestrador
    """

    print("\n💬 MODO CONVERSA INTERATIVA")
    print("=" * 40)
    print("Agora você pode conversar com o sistema!")
    print("Comandos especiais:")
    print("  'historico' - ver histórico da conversa")
    print("  'stats' - ver estatísticas")
    print("  'limpar' - limpar histórico")
    print("  'sair' - terminar conversa")
    print()

    orquestrador = OrquestradorChatbot(verbose=False)

    while True:
        mensagem = input("💭 Você: ").strip()

        # Comandos especiais
        if mensagem.lower() == "sair":
            print("👋 Conversa encerrada!")
            break
        elif mensagem.lower() == "historico":
            historico = orquestrador.obter_historico()
            print("\n📜 Histórico da conversa:")
            for i, item in enumerate(historico, 1):
                print(f"  {i}. Você: {item['usuario']}")
                print(f"     Bot: {item['sistema'][:100]}...")
                print(f"     ({item['timestamp']})")
            print()
            continue
        elif mensagem.lower() == "stats":
            stats = orquestrador.estatisticas()
            print("\n📊 Estatísticas:")
            for chave, valor in stats.items():
                print(f"   {chave}: {valor}")
            print()
            continue
        elif mensagem.lower() == "limpar":
            orquestrador.limpar_historico()
            continue
        elif not mensagem:
            print("⚠️ Por favor, digite uma mensagem válida")
            continue

        # Processar mensagem normal
        print("\n🤖 Processando...")
        resposta = orquestrador.processar_mensagem(mensagem)
        print(f"🤖 Bot: {resposta}\n")


if __name__ == "__main__":
    print("🎭 AULA 6 - ORQUESTRADOR DO CHATBOT")
    print("=" * 50)
    print()
    print("Escolha uma opção:")
    print("1 - Demonstração com exemplos")
    print("2 - Modo conversa interativa")
    print()

    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == "1":
        demonstracao_orquestrador()
    elif opcao == "2":
        modo_conversa_interativa()
    else:
        print("❌ Opção inválida. Execute novamente e escolha 1 ou 2.")
